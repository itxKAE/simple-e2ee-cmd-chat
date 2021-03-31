# client.py v0.4
# Description:  A simple e2ee command line chat application. This is the client which will listen for incoming messages.
#               Features: RSA Encryption, Message Padding
# Changelog:    v0.1: Base Chat Listener/Sender
#               v0.2: Added RSA Key Generation & Exchange
#               v0.3: Added Encryption & Decryption
#               v0.4: Added Padding

from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP

import binascii
import socket, threading
import time

# Public/Private Key Generation
keys = RSA.generate(3072)
pubKey = keys.publickey()
pubStr = pubKey.exportKey("PEM")
pubStr = pubStr.decode('utf-8')


# User input for server's address and port 
host_no = input("Enter server IP address: ")
port_no = int(input("Enter desired port number: "))

# Username
# if-else will check if whitespace are present in input, if present, replace whitespace with null
ADDR = (host_no, port_no)
name = input("Enter your name: ")
if " " in name:
    name = name.replace(" ", "")

# sender()
# Description:  1. Sends a initial message to Server telling that its connected
#               2. Constantly checks for input, if available, encrypt the message using encrypt(message) before sending out
def sender():
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    #client_socket.connect(('127.0.0.1', 6969))
    client_socket.connect(ADDR)
    
    message = client_socket.recv(1024).decode('ascii')
    if message == 'NAME':
        client_socket.send(name.encode('ascii'))

    while True:
        message = '{}: {}'.format(name, input(''))
        message = encrypt(message)
        message = binascii.hexlify(message).decode('utf-8')
        client_socket.send(message.encode('ascii'))

# listener()
# Description:  Client will constantly listen to received messages and perform the following:
#               1. if message == 'NAME':    Check if a reply is received from the server, if yes, tells the server that the listener has been connected
#               2. if "entered" in message: Check if someone has entered the room
#                                           Yes:    Checks if its a listener, if no, performs key exchange
#                                           No:     Checks if its a system message, if no, decrypts the message before printing it
#               3. elif "BEING PUBLIC KEY": Checks if a key-exchange request is received, if yes, perform key-checks before storing the key in peer_key[]
def listener():
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    #client_socket.connect(('127.0.0.1', 6969))
    client_socket.connect(ADDR)
    
    while True:
        try:
            message = client_socket.recv(1024).decode('ascii')
            if message == 'NAME':
                nameR = name + "'s Listener"
                client_socket.send(nameR.encode('ascii'))
            else:
                if "entered" in message:
                    if not name in message:
                        if not "Listener" in message:
                            print(message)
                            print("System: Initialising...")
                            message = key_exchange(message)
                            time.sleep(3)
                            client_socket.send(message.encode('ascii'))
                            print("System: Complete!")
                elif "BEGIN PUBLIC KEY" in message:
                    if not name in message:
                        print("System: Initialising...")
                        message = key_check(message)
                        if "YES" in message:
                            client_socket.send(message.encode('ascii'))
                        print("System: Complete!")
                else:
                    if not "Connection Success." in message:
                        message = message.encode('utf-8')
                        message = binascii.unhexlify(message)
                        print(decrypt(message))
                    else:
                        print("System: " + message)
        except Exception as e:
            # The following are for error handling
            #print(e)
            #print("Error. Bye.")
            #client_socket.close()
            #break
            pass

# Key Storage
peer_list = []
peer_key = []

# key_exchange()
# Description:  Performs Key Exchange. Checks if the name is present, if yes, sends a message back telling the target that the current client has its public key and will not require an exchange.
#               Will still send out personal public key.
# Args: message > System message that indicates who entered
def key_exchange(message):
    present = 0

    if not peer_list:
        message = '{} {} NO'.format(name, pubStr)
    else:
        for peer in peer_list:
            if peer in message:
                present = 1
                break
        if present == 1:
            message = '{} {} YES'.format(name, pubStr)
        else:
            message = '{} {} NO'.format(name, pubStr)
    return message

# key_check()
# Description:  Performs key storage. Checks if the target requires this client's public key, if yes, sends personal public key.
# Args: message > Received message that contains the target's name, public key and whether a key exchange is required
def key_check(message):
    sender = message.split()[0]
    key = message.split()[1] + " " + message.split()[2] + " " + message.split()[3] + "\n" + message.split()[4] + "\n" + message.split()[5] + "\n" + message.split()[6] + "\n" + message.split()[7] + "\n" + message.split()[8] + "\n" + message.split()[9] + "\n" + message.split()[10] + "\n" + message.split()[11] + "\n" + message.split()[12] + "\n" + message.split()[13] + " " + message.split()[14] + " " + message.split()[15]
    status = message.split()[16]
    
    peer_list.append(sender)
    peer_key.append(key)

    if "NO" in status:
        return '{} {} YES'.format(name, pubStr)
    else:
        return "NO"

# encrypt()
# Description:  Pads the message using pad() before encrypting the message with personal private key.
# Args: message > Input string
def encrypt(message):
    peerKey = RSA.importKey(peer_key[0])
    encryptor = PKCS1_OAEP.new(peerKey)
    message = pad(message)
    return encryptor.encrypt(message.encode('utf-8'))

# decrypt()
# Description:  Decrypts the received message and unpad it before returning
# Args: message > Received message from target
def decrypt(message):
    decryptor = PKCS1_OAEP.new(keys)
    message = decryptor.decrypt(message).decode('utf-8')
    return unpad(message)

# pad()
# Description:  Pads the input with two strings, one at the front and the other at the end. These will be used for tampering checks.
# Args: message > Input string
def pad(message):
    return "=what=is=nice=" + message + "=apple=pie="

# unpad()
# Description:  Unpads the decrypted message and return the original message. If two predefined substrings are not present, informs the user that message has been tampered.
# Args: message > Decrypted message
def unpad(message):
    if "=what=is=nice=" in message:
        if "=apple=pie=" in message:
            message = message.replace("=what=is=nice=", "")
            message = message.replace("=apple=pie=", "")
            return message
        else:
            return "System: Message is tempered!\nSystem: Received message: " + message
    else:
        return "System: Message is tempered!\nSystem: Received message: " + message

# Threading to allow separation of client's sender and receiver
send_thread = threading.Thread(target=sender)
send_thread.start()
receive_thread = threading.Thread(target=listener)
receive_thread.start()