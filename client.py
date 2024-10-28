import socket
    
# Takes in an ip, port and nickname, joins server.
# Read messages with receive
# Write messages with write
class Client:
    def __init__(self, ip:str, port:int, nickname:str):
        self.nickname = nickname
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.connect((ip, port))
        
    # Recieves a message from server and returns it
    # Needs to be in its own thread so this and write aren't in conflict
    def receive(self):
        try:
            message = self.socket.recv(1024).decode('utf-8')
            if message == 'NICK':
                self.socket.send(self.nickname.encode('utf-8'))
            else:
                return(message)
        except:
            print("Error! The recieve method of client went wrong")
            self.socket.close()
            return 'FAILED_TO_CONNECT' # This is really easy to spoof


    # Sends a message to the server
    # This will continiously send out the same message over and over
    # if used improperly
    def write(self, message):
        self.socket.send(message.encode('utf-8'))