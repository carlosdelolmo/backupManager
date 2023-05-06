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
    encodedMessage = message.encode()
    client_socket.send(len(encodedMessage))
    print("enviado: " + str(len(encodedMessage)))
    client_socket.recv(128)
    print("recibido ack")
    client_socket.send(encodedMessage)
    print("enviado: " + str(encodedMessage))
    client_socket.recv(128).decode()
    print("recibido ack2")
    client_socket.close()


if __name__ == "__main__":
    if len(sys.argv) == 2:
        message = sys.argv[1]
        req(message)
