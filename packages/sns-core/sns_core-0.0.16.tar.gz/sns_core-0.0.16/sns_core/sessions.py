import socket
import threading
import time
import sys
import signal
import re

from .parser import parse
from .records import SNSrecord
from .exceptions import SNSinteractionException
from .objects import SNSinteraction
from .utils import SingletonMeta, SNS_PORT, BUFFER_SIZE

def signal_handler(signal, frame):
    SNSsession().stop_session_thread = True
    sys.exit(0)

signal.signal(signal.SIGINT, signal_handler)

class SNSsession(metaclass=SingletonMeta):

    def __init__(self):
        self.session_thread = None
        self.session_socket = None
        self.stop_session_thread = True

        self.interactions = []
        self.callbacks = {}

    def start_session(self, address, port=SNS_PORT):
        if self.session_thread is None or not self.session_thread.is_alive():
            self.session_thread = threading.Thread(target=self.__session_thread_func, args=(address, port))
            self.session_thread.start()

    def __session_thread_func(self, address, port=SNS_PORT):
        try:
            self.session_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.session_socket.connect((address, port))

            create_session_interaction = SNSinteraction("USER", "session", {
                'From': 'user:' + SNSrecord().this_user.identifier,
                'To': 'server:' + SNSrecord().this_user.identifier.split('@')[-1]
            })

            self.session_socket.sendall(str(create_session_interaction).encode('utf-8'))

            self.stop_session_thread = False
            while not self.stop_session_thread:
                data = b''

                while True:
                    temp_data = self.session_socket.recv(BUFFER_SIZE)
                    self.receiving_messages = True
                    data += temp_data

                    interaction_blobs = re.split(b'(?:\r?\n){2,}', data)

                    self.append_interaction_blobs(interaction_blobs[:-1])

                    data = interaction_blobs[-1]

                    if len(temp_data) < BUFFER_SIZE: 
                        self.receiving_messages = False
                        break

                    time.sleep(0.1)

                try:
                    self.append_interaction_blobs(re.split(b'(?:\r?\n){2,}', data))
                except SNSinteractionException:
                    print('W: Received interaction not complete')

                self.check_interaction_callbacks()

                time.sleep(0.1)

            self.session_socket.close()
            self.session_socket = None
        except socket.error:
            print("W: Socket error")

        self.stop_session_thread = False

    def append_interaction_blobs(self, interaction_blobs):
        for interaction_blob in interaction_blobs:
            if len(interaction_blob) == 0:
                continue

            try:
                self.interactions.append(parse(interaction_blob.decode('utf-8')))
            except:
                if len(self.interactions) > 0:
                    self.interactions[-1].content.append(interaction_blob.decode('utf-8'))
                else:
                    raise SNSinteractionException(interaction_blob)

    def add_interaction_callback(self, callback_function, type="*", action="*", header_filters={}):
        self.callbacks[type, action] = [header_filters, callback_function]

    def check_interaction_callbacks(self):
        for interaction in self.interactions:
            header_filters = {}
            callback_function = None

            if (interaction.type, interaction.action) in self.callbacks:
                header_filters, callback_function = self.callbacks[interaction.type, interaction.action]
            elif (interaction.type, "*") in self.callbacks:
                header_filters, callback_function = self.callbacks[interaction.type, "*"]
            elif ("*", interaction.action) in self.callbacks:
                header_filters, callback_function = self.callbacks["*", interaction.action]
            elif ("*", "*") in self.callbacks:
                header_filters, callback_function = self.callbacks["*", "*"]
            else:
                print("W: No callback for this interaction, skipping..", interaction.type, interaction.action)
                continue

            for filter_key, filter_value in header_filters.items():
                if filter_key not in interaction.headers or filter_value != interaction.headers[filter_key]:
                    print("W: Interaction does not contain filter headers, skipping..", interaction.type, interaction.action)
                    continue

            callback_function(interaction)

            self.interactions.remove(interaction)

    def close_session(self):
        if not self.session_thread is None and self.session_thread.is_alive():
            self.stop_session_thread = True

            while self.stop_session_thread:
                time.sleep(0.1)

            self.session_thread = None

    def __del__(self):
        self.close_session()
        