import socket
import threading

peers = {}

def read_peer_settings():
    try:

        with open('../peer_settings.txt', 'r') as file:

            current_line = file.readline().strip()

            while current_line != '':

                # split currnet line by spaces 
                peer_ID, ip_addr, server_port = current_line.split(" ")

                # add peer settings to peers list
                peers[peer_ID] = (ip_addr, int(server_port), False )
                # read next line
                current_line = file.readline().strip()

    except IOError:
        print("File not found.")
    except Exception:
        print("Unexpected error occurred while reading the file.")


def thread_connected_cleint(cleint):
    while True:
        try:
            pass
        except Exception as e:
            print("Error reading from client:", str(e))
            cleint.close()
            break
   


def connect_to_peer(peer):
    if peer in peers:
        ip_addr, server_port, isConnected = peers[peer]

        if isConnected == False :
            try:
                client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                client_socket.connect((ip_addr, server_port))
                print(f"Connected to peer {peer} at {ip_addr}:{server_port} \n")
                t = threading.Thread(target=thread_connected_cleint, args=(client_socket,))
                t.start()
                peers[peer] = (ip_addr, server_port, True) #change to is connected

            except socket.error as e:
                print(f"Failed to connect to peer {peer} at {ip_addr}:{server_port}. Error: {str(e)} \n")
                client_socket.close()
        else:
            print(f"Already connected to peer {peer} at {ip_addr}:{server_port} \n")
    else:
        print(f"Peer {peer} does not exist")

def main():
    read_peer_settings()
    while True:

        user_input = input("\n Input your command for {peer_ID}: ")
        try:
            command, parameters = user_input.split(" ", 1)

            if command not in ["#FILELIST", "#UPLOAD", "#DOWNLOAD"]:
                print("Invalid command. Supported commands are: #FILELIST, #UPLOAD, #DOWNLOAD")

            elif command == "#FILELIST":
                peers = parameters.split(" ")
                print(peers)
                for peer in peers:
                    connect_to_peer(peer)

            elif command == "#UPLOAD":
                filename, peers = parameters.split(" ", 1)
                pass

            elif command == "#DOWNLOAD":
                filename, peers = parameters.split(" ", 1)

                pass

            else:
                print("Invalid parameters for command.")

                print("good command")
        except ValueError:
            print("Invalid command format. Please use command followed by parameters.")
        except Exception as e:
            print("An error occurred:", str(e))


if __name__ == "__main__":
    main()
print(peers)



# server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# server.bind(('localhost', 8232))
# server.connect((ip_address, server_port))