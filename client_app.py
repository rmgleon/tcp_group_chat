from client import Client
import threading
import sys
import time

ip = "127.0.0.1"
port = 44332
nickname = input("Nickname: ")
client = Client(ip, port, nickname)

# worker loops rely on this to be unset. Set when the client disconects (types "EXIT")
stop_event = threading.Event()

def handle_receive():
    while not stop_event.is_set():
        incoming_message = client.receive()
        if incoming_message == 'FAILED_TO_CONNECT':
            print("Server cannot be reached")
            break
        print(incoming_message)

def handle_write():
    while not stop_event.is_set():
        message = input("")
        sys.stdout.write('\033[F\033[K')  # Move cursor up and clear line
        sys.stdout.flush()
        full_message = f'{nickname}: {message}'

        if message == 'EXIT':
            stop_event.set()

        client.write(full_message)

# Runs receive in one thread
recieve_thread = threading.Thread(target=handle_receive)
recieve_thread.start()

# And write on another, such that it can read and write at once
write_thread = threading.Thread(target=handle_write)
write_thread.start()
