from .parser import parse
from .exceptions import SNSinteractionException, SNSserverException
from .records import SNSrecord
from .objects import SNSinteraction, SNScontent
from .utils import SNS_PORT, BUFFER_SIZE

import socket
import re

#TODO: encrypt the whole request with the private key of the user first, to ensure integrity and authenticity. 
#Since the public key is already known to the server, this does not require any extra steps either.
def request(type, action, content=None, port=SNS_PORT, **headers):
    for key, value in headers.items():
        try:
            headers[key] = str(value)
        except IndexError:
            raise SNSinteractionException(str(headers), "One of the interaction headers could not be parsed to a string")

    interaction = parse(str(SNSinteraction(type, action, headers, content)))

    if 'From' not in interaction.headers:
        raise SNSinteractionException(str(interaction), "The interaction is missing From header, causing the interaction not to be sent")

    if interaction.headers['From'].count('@') > 1:
        raise SNSinteractionException(str(interaction), "The From header contains too many @ characters (max. 1 per address header), causing that the address cannot be determined")

    if 'To' not in interaction.headers:
        raise SNSinteractionException(str(interaction), "The interaction is missing To header, causing the interaction not to be sent")

    if interaction.headers['To'].count('@') > 1:
        raise SNSinteractionException(str(interaction), "The To header contains too many @ characters (max. 1 per address header), causing that the address cannot be determined")

    address = interaction.headers['From'].split('@')[1]

    conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    conn.connect((address, SNS_PORT))

    conn.sendall(str(interaction).encode('utf-8'))

    data = b''

    while True:
        temp_data = conn.recv(BUFFER_SIZE)
        data += temp_data
        if (len(temp_data) < BUFFER_SIZE): break
        time.sleep(0.1)

    conn.close()

    interaction_blobs = re.split(r"(?:\r?\n){2,}", data.decode('utf-8'))

    interactions = []
    for interaction_blob in interaction_blobs:
        try:
            interactions.append(parse(interaction_blob))
        except:
            if len(interactions) > 0:
                interactions[-1].content.append(interaction_blob)
            else:
                raise SNSserverException()
    
    return interactions

def user(action, to, from_=None, content=None, **headers):
    encrypted_content = content

    headers['From'] = 'user:' + SNSrecord().this_user.identifier if from_ is None else from_
    headers['To'] = to

    interaction_object = request('USER', action, encrypted_content, **headers)
    
    return interaction_object

def group(action, to, from_=None, content=None, **headers):
    encrypted_content = content

    headers['From'] = 'user:' + SNSrecord().this_user.identifier if from_ is None else from_
    headers['To'] = to

    interaction_object = request('GROUP', action, encrypted_content, **headers)
    
    return interaction_object

def post(action, to, from_=None, content=None, **headers):
    encrypted_content = content

    headers['From'] = 'user:' + SNSrecord().this_user.identifier if from_ is None else from_
    headers['To'] = to

    interaction_object = request('POST', action, encrypted_content, **headers)
    
    return interaction_object

def reaction(action, to, from_=None, content=None, **headers):
    encrypted_content = content

    headers['From'] = 'user:' + SNSrecord().this_user.identifier if from_ is None else from_
    headers['To'] = to

    interaction_object = request('REACTION', action, encrypted_content, **headers)
    
    return interaction_object