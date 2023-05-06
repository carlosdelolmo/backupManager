import socket
import sys


def req(message):
    host = socket.gethostname()
    port = (
        5020
    )
    client_socket = socket.socket()
    client_socket.connect((host, port))
    encodedMessage = message.encode()
    client_socket.send(str(len(encodedMessage)).encode())
    client_socket.recv(128)
    client_socket.send(encodedMessage)
    client_socket.recv(128).decode()
    client_socket.close()


if __name__ == "__main__":
    if len(sys.argv) == 2:
        message = sys.argv[1]
        req(message)
