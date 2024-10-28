from client import Client
import threading
import sys
import time

ip = "127.0.0.1"
port = 44332
nickname = input("Nickname: ")
client = Client(ip, port, nickname)

def handle_receive():
    while True:
        incoming_message = client.receive()
        print(incoming_message)

def handle_write():
    while True:
        message = f'{nickname}: {input("")}'
        sys.stdout.write('\033[F\033[K')  # Move cursor up and clear line
        sys.stdout.flush()
        client.write(message)


# Runs receive in one thread
recieve_thread = threading.Thread(target=handle_receive)
recieve_thread.start()

# And write on another, such that it can read and write at once
write_thread = threading.Thread(target=handle_write)
write_thread.start()