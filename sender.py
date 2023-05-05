import socket
import sys
import os


def req(message):
    host = socket.gethostname()  # as both code is running on same pc
    port = 5020  # socket server port numberclient_socket = socket.socket()  # instantiate
    client_socket = socket.socket()  # instantiate
    client_socket.connect((host, port))  # connect to the server
    client_socket.send(message.encode())
    data = client_socket.recv(4096).decode()  # receive response
    client_socket.close()  # close the connection

if __name__ == '__main__':
    if len(sys.argv) == 2:
        message = sys.argv[1]
        req(message)
