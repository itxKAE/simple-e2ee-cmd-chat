import socket, threading

server_ip = '127.0.0.1'
port = 6969

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((server_ip, port))
server_socket.listen()

client_list = []
client_name = []

def broadcast(message):
    for client in client_list:
        client.send(message)

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

def server_main():
    while True:
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

server_main()