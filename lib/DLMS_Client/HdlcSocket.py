import socket
import serial

# create a socket object
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# bind the socket to a public host and port
server_address = ('localhost', 12345)
server_socket.bind(server_address)

# listen for incoming connections
server_socket.listen(1)

print('Echo server is up and running!')

while True:
    # wait for a connection
    print('Waiting for a client connection...')
    client_socket, client_address = server_socket.accept()
    print('Accepted a client connection from', client_address)

    # receive data from the client and echo it back
    while True:
        data = client_socket.recv(1024)
        if not data:
            break
        print('Received data from', client_address, ':', data)
        buffer = [0x7e, 0xa0, 0x0a, 0x21, 0x00, 0x02, 0x00, 0x21, 0x31, 0xea, 0xb5, 0x7e]
        buffer = bytes(buffer)
        # client_socket.sendall(data)
        client_socket.sendall(buffer)

    # close the client socket
    print('Closing the client connection with', client_address)
    client_socket.close()