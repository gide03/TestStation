# import socket

# # create a socket object
# client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# # connect to the server
# server_address = ('localhost', 12345)
# client_socket.connect(server_address)

# # send data to the server and receive the echoed data
# while True:
#     message = input('Enter a message to send to the server: ')
#     client_socket.sendall(message.encode())
#     data = client_socket.recv(1024)
#     print('Received echoed data:', data.decode())

#     # ask the user if they want to send more data
#     choice = input('Do you want to send more data? (y/n): ')
#     if choice.lower() != 'y':
#         break

# # close the socket
# client_socket.close()


import socket


class TPC_HDLC:
    RECV_BUFFER = 1024

    def __init__(self, address, port) -> None:
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_address = (address, port)
    
    def open(self):
        self.socket.connect(self.server_address)
    
    def close(self):
        self.socket.close()

    def write(self, buffer:bytes, timeout:int=10) -> bool:
        print(f'Write buffer {buffer}')
        self.socket.sendall(buffer.encode())

    def read(self) -> bytes:
        data = self.socket.recv(self.RECV_BUFFER)
        print(f'Receive data from socket: {data}')
        return data