import socket

peers = {}

def read_peer_settings():

  
    try:

        with open('../peer_settings.txt', 'r') as file:

            current_line = file.readline().strip()

            while current_line != '':

                # split currnet line by spaces 
                peer_ID, ip_addr, server_port = current_line.split(" ")

                # add peer settings to peers list
                peers[peer_ID] = (ip_addr, int(server_port) )
                print("ran")
                # read next line
                current_line = file.readline().strip()

    except IOError:
        print("File not found.")
    except Exception:
        print("Unexpected error occurred while reading the file.")



def connect_to_peers():
    for peer_ID, (ip_addr, server_port) in peers.items():
        try:
            client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            client_socket.connect((ip_addr, server_port))
            print(f"Connected to peer {peer_ID} at {ip_addr}:{server_port}")
        except socket.error as e:
            print(f"Failed to connect to peer {peer_ID} at {ip_addr}:{server_port}. Error: {str(e)}")
            client_socket.close()


read_peer_settings()
connect_to_peers()

print(peers)



# server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# server.bind(('localhost', 8232))
# server.connect((ip_address, server_port))