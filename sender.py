import socket
import sys


def client_program():
    host = socket.gethostname()  # as both code is running on same pc
    port = 5020  # socket server port number

    message = input(" -> ")  # take input

    while message.lower().strip() != 'bye':
        client_socket = socket.socket()  # instantiate
        client_socket.connect((host, port))  # connect to the server
        client_socket.send(message.encode())  # send message
        data = client_socket.recv(1024).decode()  # receive response
        message = input(" -> ")  # again take input
        client_socket.close()  # close the connection

def req(message):
    host = socket.gethostname()  # as both code is running on same pc
    port = 5020  # socket server port numberclient_socket = socket.socket()  # instantiate
    client_socket = socket.socket()  # instantiate
    client_socket.connect((host, port))  # connect to the server
    # print(message.encode())
    client_socket.send(message.encode())
    data = client_socket.recv(4096).decode()  # receive response
    # print('Received from server: ' + data)  # show in terminal
    client_socket.close()  # close the connection

if __name__ == '__main__':
    # schedule.every().minutes.at(":00").do(req, 'Es la hora!')
    # schedule.every(5).seconds.do(req, 'Es el segundo!')
    # client_program()
    if len(sys.argv) == 2:
        message = sys.argv[1]
        req(message)
    # while True:
    #     schedule.run_pending()
    #    time.sleep(1)  # wait one sec
