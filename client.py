from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP

import binascii
import socket, threading
import time

keys = RSA.generate(3072)
pubKey = keys.publickey()
pubStr = pubKey.exportKey("PEM")
pubStr = pubStr.decode('utf-8')

name = input("Enter your name: ")

def sender():
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect(('127.0.0.1', 6969))

    message = client_socket.recv(1024).decode('ascii')
    if message == 'NAME':
        client_socket.send(name.encode('ascii'))

    while True:
        message = '{}: {}'.format(name, input(''))
        message = encrypt(message)
        message = binascii.hexlify(message).decode('utf-8')
        client_socket.send(message.encode('ascii'))

def listener():
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect(('127.0.0.1', 6969))

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
                            print("Initialising...")
                            message = key_exchange(message)
                            time.sleep(3)
                            client_socket.send(message.encode('ascii'))
                            print("Complete!")
                elif "BEGIN PUBLIC KEY" in message:
                    if not name in message:
                        message = key_check(message)
                        if "YES" in message:
                            client_socket.send(message.encode('ascii'))
                else:
                    if not "Connection Success." in message:
                        message = message.encode('utf-8')
                        message = binascii.unhexlify(message)
                        print(decrypt(message))
                    else:
                        print(message)
        except Exception as e:
            #print(e)
            #print("Error. Bye.")
            #client_socket.close()
            #break
            pass

peer_list = []
peer_key = []

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

def encrypt(message):
    peerKey = RSA.importKey(peer_key[0])
    encryptor = PKCS1_OAEP.new(peerKey)
    return encryptor.encrypt(message.encode('utf-8'))

def decrypt(message):
    decryptor = PKCS1_OAEP.new(keys)
    return decryptor.decrypt(message).decode('utf-8')

send_thread = threading.Thread(target=sender)
send_thread.start()
receive_thread = threading.Thread(target=listener)
receive_thread.start()