import socket
import sys
import errno

HEADER_LENGTH = 10

IP = "127.0.0.1"
PORT = 35584
my_username = input("Username: ")  # get username

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((IP, PORT))  # create sockets and bind to ip and port

client_socket.setblocking(False)

# Create Header
username = my_username.encode('utf-8')
username_header = f"{len(username):<{HEADER_LENGTH}}".encode('utf-8')
client_socket.send(username_header + username)


while True:
    message = input(f'{my_username} > ')
    if message == '/q':  # if user enters /q, they are disconnected
        sys.exit()
    if message:  # we only attempt to send a message if there is content
        message = message.encode('utf-8')
        message_header = f"{len(message):<{HEADER_LENGTH}}".encode('utf-8')
        client_socket.send(message_header + message)
    try:
        while True:
            username_header = client_socket.recv(HEADER_LENGTH)
            if not len(username_header):  # if there was no data then we disconnect
                print('Connection closed by the server')
                sys.exit()

            # message and header are formatted in order to be delivered
            username_length = int(username_header.decode('utf-8').strip())
            username = client_socket.recv(username_length).decode('utf-8')

            message_header = client_socket.recv(HEADER_LENGTH)
            message_length = int(message_header.decode('utf-8').strip())
            message = client_socket.recv(message_length).decode('utf-8')

            print(f'{username} > {message}')  # message is output to the screen


    except IOError as e:

        # check for specific errors, if it is again or wouldblock we continue, else we exit and indicate something wrong
        if e.errno != errno.EAGAIN and e.errno != errno.EWOULDBLOCK:
            print('Reading error: {}'.format(str(e)))
            sys.exit()


    except Exception as e:

        # check for any other errors that may need us to disconnect
        print('Reading error: '.format(str(e)))
        sys.exit()

