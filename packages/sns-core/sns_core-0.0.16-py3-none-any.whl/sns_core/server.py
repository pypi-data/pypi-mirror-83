import socket
import threading
import time
import re
import sys, signal

from .parser import parse
from .objects import SNSinteraction
from .exceptions import SNSserverException
from .utils import SNS_PORT, SNS_HOST, BUFFER_SIZE

def signal_handler(signal, frame):
    SNSsession.stop_server_thread = True
    sys.exit(0)

signal.signal(signal.SIGINT, signal_handler)

class SNSserver(object):

    components = {}

    server_thread = None
    conn_threads = []
    stop_server_thread = False
    sessions = {}

    def __init__(self, type=None, action=None):
        self.type = type
        self.action = action

        if self.type is None:
            self.type = "*"

        if self.action is None:
            self.action = "*"

    def __call__(self, func):
        if not isinstance(self.type, list):
            self.type = [self.type]

        if not isinstance(self.action, list):
            self.action = [self.action]

        for type in self.type:
            for action in self.action:
                self.components[type, action] = func

    @staticmethod
    def start_server(address=SNS_HOST, port=SNS_PORT):
        if SNSserver.server_thread is None or not SNSserver.server_thread.is_alive():
            SNSserver.server_thread = threading.Thread(target=SNSserver.server_thread_func, args=(address, port))
            SNSserver.server_thread.start()

    @staticmethod
    def server_thread_func(address=SNS_HOST, port=SNS_PORT):
        print("Starting on:", address, port)
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.bind((address, port))
        s.listen(1)

        print("Server has started..")

        while not SNSserver.stop_server_thread:
            conn, addr = s.accept()

            conn_thread = threading.Thread(target=SNSserver.connection_handler, args=(conn, addr))
            conn_thread.start()
            
            SNSserver.conn_threads.append(conn_thread)

        s.close()

        SNSserver.stop_server_thread = False

    @staticmethod
    def connection_handler(conn, addr):
        with conn:
            print('Connected with', addr)
            conn.settimeout(2)
            while not SNSserver.stop_server_thread:
                try:
                    data = b''

                    while True:
                        temp_data = conn.recv(BUFFER_SIZE)
                        data += temp_data
                        if (len(temp_data) < BUFFER_SIZE): break
                        time.sleep(0.05)

                    if len(data) == 0:
                        break

                    interaction_blobs = re.split(r"(?:\r?\n){2,}", data.decode('utf-8').strip())

                    interactions = []
                    for interaction_blob in interaction_blobs:
                        try:
                            interactions.append(parse(interaction_blob))
                        except:
                            if len(interactions) > 0:
                                interactions[-1].content.append(interaction_blob)
                            else:
                                raise SNSserverException()

                    print(addr, "Received interaction:")
                    print(interactions)

                    responses = []

                    for interaction_object in interactions:
                        session_response = None
                        if (interaction_object.type, interaction_object.action) == ("USER", "session"):
                            conn.settimeout(None)
                            SNSserver.sessions[interaction_object.headers['From'].split(':')[-1]] = conn
                            session_response = SNSinteraction("STATUS", 202, {'From':interaction_object.headers['To'], 'To':interaction_object.headers['From']})

                        response = None
                        if (interaction_object.type, interaction_object.action) in SNSserver.components:
                            response = SNSserver.components[interaction_object.type, interaction_object.action](interaction_object)
                        elif (interaction_object.type, "*") in SNSserver.components:
                            response = SNSserver.components[interaction_object.type, "*"](interaction_object)
                        elif ("*", interaction_object.action) in SNSserver.components:
                            response = SNSserver.components["*", interaction_object.action](interaction_object)
                        elif ("*", "*") in SNSserver.components:
                            response = SNSserver.components["*", "*"](interaction_object)
                        
                        if response is None:
                            if session_response is None:
                                print(addr, "Interaction component not found")
                                response = SNSinteraction("STATUS", 404, {'From':interaction_object.headers['To'], 'To':interaction_object.headers['From']})
                            else:
                                response = session_response

                        if isinstance(response, list):
                            responses += response
                        else:
                            responses.append(response)

                    print(addr, "Constructed response:")
                    if len(responses) == 0:
                        response = SNSinteraction("STATUS", 401, {'From':interaction_object.headers['To'], 'To':interaction_object.headers['From']})
                        print(response.type, response.action)
                        print('From: ' + response.headers['From'] + ' To: ' + response.headers['To'])
                        conn.sendall(str(response).encode('utf-8'))
                    elif len(responses) == 1:
                        response = responses[0]
                        print(response.type, response.action)
                        print('From: ' + response.headers['From'] + ' To: ' + response.headers['To'])
                        conn.sendall(str(response).encode('utf-8'))
                    else:
                        print('\n'.join([item.type + ' ' + item.action + '\nFrom: ' + item.headers['From'] + ' To: ' + item.headers['To'] for item in responses]))
                        conn.sendall(''.join([str(item) for item in responses]).encode('utf-8'))

                except socket.error as e:
                    print(e)
                    print("W: Something was wrong with the socket connection, further investigation is needed if this issue persists")
                    break
                except SNSserverException as e:
                    print(e)
                    print("W: A server exception occured, meaning something went wrong with loading in or sending a request")
                    break

        for key in list(SNSserver.sessions):
            if SNSserver.sessions[key] == conn:
                del SNSserver.sessions[key]

        conn.close()
        print("Disconnected from", addr)

    @staticmethod
    def send_session_interactions(interactions):
        for interaction in interactions:
            try:
                conn = SNSserver.sessions[interaction.get('To', '').split(':')[-1]]
                conn.sendall(str(interaction).encode('utf-8'))
            except KeyError:
                continue

    @staticmethod
    def close_server():
        SNSserver.stop_server_thread = True

        while SNSserver.stop_server_thread:
            time.sleep(0.1)

        SNSserver.server_thread = None