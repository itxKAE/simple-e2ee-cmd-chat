# server.py v0.1
# Description:  A simple e2ee command line chat application. This is the server which will perform message exchanges.
# Changelog:    v0.1: Base Chat Server

import socket, threading

# Server Details
#server_ip = '127.0.0.1'
#port = 6969
server_ip = socket.gethostbyname(socket.gethostname())
port = int(input("Enter port number of the server: "))

# Socket Operations
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((server_ip, port))
server_socket.listen()

# Client Storage
client_list = []
client_name = []

# broadcast()
# Description:  Sends out the message to connected clients
# Args: message > Received message
def broadcast(message):
    for client in client_list:
        client.send(message)

# event_handler()
# Description:  Performs client connection checks and prints out its status.
# Args: client  > Server's Listener
def event_handler(client):                                         
    while True:
        try:
            message = client.recv(1024)
            broadcast(message)
        except:
            index = client_list.index(client)
            client_list.remove(client)
            client.close()
            name = client_name[index]
            broadcast("{} left.".format(name).encode('ascii'))
            print("{} disconnected.".format(name))       
            client_name.remove(name)
            break

# server_main()
# Description:  Handles system message printing/broadcasting for connectivity checks.
def server_main():
    while True:
        print("Server session initiated. ")
        print("Server IP address is " + server_ip + " with the port number of " + str(port) + ".")
        print("Checking for client connections.......")
        client, address = server_socket.accept()
        print("{} connected.".format(str(address)))       
        client.send('NAME'.encode('ascii'))
        name = client.recv(1024).decode('ascii')
        client_name.append(name)
        client_list.append(client)
        print("Client Name: {}".format(name))
        broadcast("{} entered.".format(name).encode('ascii'))
        client.send('Connection Success.'.encode('ascii'))
        thread = threading.Thread(target=event_handler, args=(client,))
        thread.start()

# Run
server_main()