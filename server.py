import socket
import select

HEADER_LENGTH = 10

IP = "127.0.0.1"
PORT = 35584


server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((IP, PORT))  # Set the ip and port number and create socket

server_socket.listen()


sockets_list = [server_socket]
clients = {}  # keeps track of clients

print(f'Listening for connections on {IP}:{PORT}...')  # confirmation server is running

def receive_message(client_socket):

    try:
        message_header = client_socket.recv(HEADER_LENGTH)

        if not len(message_header):  # if the len of the header is 0 we know there is nothing to return
            return False

        message_length = int(message_header.decode('utf-8').strip())

        return {'header': message_header, 'data': client_socket.recv(message_length)}

    except:

        return False

while True:
    # initialize lists so we can keep track of what sockets are connecting
    read_sockets, writing_sockets, exception_sockets = select.select(sockets_list, [], sockets_list)

    for x in read_sockets:

        if x == server_socket:
            # if x is equal to server_socket then we know a new socket is attempting to connect
            client_socket, client_address = server_socket.accept()
            user = receive_message(client_socket)

            sockets_list.append(client_socket)  # new user is appended list of users with user name

            clients[client_socket] = user

            print('Accepted new connection from {}:{}, username: {}'.format(*client_address, user['data'].decode('utf-8')))

        else:
            message = receive_message(x)
            if message is False:  # check message exists before continuing
                print('Closed connection from: {}'.format(clients[x]['data'].decode('utf-8')))

                sockets_list.remove(x)
                del clients[x]
                continue

            user = clients[x]
            # print username and message data sent
            print(f'Received message from {user["data"].decode("utf-8")}: {message["data"].decode("utf-8")}')

            # We send the message to all clients that are not the original sender of the message
            for client_socket in clients:
                if client_socket != x:
                    client_socket.send(user['header'] + user['data'] + message['header'] + message['data'])
