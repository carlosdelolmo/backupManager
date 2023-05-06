import socket
import sys
import os


def req(message):
    host = socket.gethostname()
    port = (
        5020
    )
    client_socket = socket.socket()
    client_socket.connect((host, port))
    client_socket.send(message.encode())
    data = client_socket.recv(4096).decode()
    client_socket.close()


if __name__ == "__main__":
    if len(sys.argv) == 2:
        message = sys.argv[1]
        req(message)
