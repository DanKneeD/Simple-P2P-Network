import socket

server_port = 5001
ip_address = 'localhost'

peers = {}

def read_peer_settings():

    #open file and read first line
    file = open('../peer_settings.txt', 'r')
    current_line = file.readline()
    counter = 0

    while current_line.strip() != '':

        # split currnet line by spaces 
        peer_ID, ip_addr, server_port = current_line.strip().split(" ")
        print(f"Peer ID: {peer_ID}, IP Address: {ip_addr}, Server Port: {server_port} \n" )

        # add peer settings to peers list
        peers[counter] = (peer_ID, ip_addr, int(server_port))
        counter += 1

        # read next line
        current_line = file.readline()




read_peer_settings()
print(peers)



# server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# server.bind(('localhost', 8232))
# server.connect((ip_address, server_port))