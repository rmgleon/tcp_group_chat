import threading
import socket

host = '127.0.0.1' # Localhost
port = 44332
server_name = 'Test Server Name'

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((host, port))
server.listen()

clients = []
nicknames = []

def broadcast(message):
    for client in clients:
        client.send(message)


def handle(client):
    while True:
        try: # to take data from our clients 
            message = client.recv(1024)
            broadcast(message)
        except: # cut them if it fails 
            index = clients.index(client)
            clients.remove(client)
            client.close()

            nickname = nicknames[index]
            broadcast(f"\n{nickname} left the chat".encode('utf-8'))
            nicknames.remove(nickname)
            break

def receive():
    while True:
        # Always accept clients 
        client, address = server.accept()
        print(f"Connected with [str{address}]")

        # Ask client for nickname and recieve it
        client.send("NICK".encode('utf-8'))
        nickname = client.recv(1024).decode('utf-8')
        nicknames.append(nickname)
        clients.append(client)

        # Inform everyone of the new client
        print(f"Nickname of client is {nickname}")
        broadcast(f"\n{nickname} joined".encode('utf-8'))
        client.send(f"Connected to {server_name} succesfully".encode('utf-8'))

        # Assign a thread to the client
        thread = threading.Thread(target=handle, args=(client,))
        thread.start()

print("Server ready...")
receive()