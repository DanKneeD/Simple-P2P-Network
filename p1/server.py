import socket

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

server.bind(('localhost', 5001))

server.listen()

print('Server is listening...')
while True:
    connection_socket, address = server.accept()
    print(f'Connection from {address} established. Connection ID: {id(connection_socket)} and connection socket: {connection_socket}')
