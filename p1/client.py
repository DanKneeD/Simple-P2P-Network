import socket
import threading

#ip_address, server_port, thread
peers_dict = {}


def read_peer_settings():
    try:

        with open('../peer_settings.txt', 'r') as file:

            current_line = file.readline().strip()

            while current_line != '':

                # split currnet line by spaces 
                peer_id, ip_addr, server_port = current_line.split(" ")

                # add peer settings to peers list
                peers_dict[peer_id] = (ip_addr, int(server_port), None)
                # read next line
                current_line = file.readline().strip()

    except IOError:
        print("File not found.")
    except Exception as e:
        print(f"Unexpected error occurred while reading the file.{e}")



#creating socket and thread connection
def connect_to_peer(peer_id):

    # check if peer ID exists
    if peer_id in peers_dict:

        ip_addr, server_port, thread = peers_dict[peer_id]

        #create thread if does not exist
        if thread == None :
            try:
                #create socket connection
                client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                client_socket.connect((ip_addr, server_port))

                print(f"200 Connected to peer {peer_id} at {ip_addr}:{server_port} \n")

                #create thread
                thread = PeerThread(peer_id, client_socket)
                # t = threading.Thread(target=con, args=(client_socket,))
                thread.start()


                peers_dict[peer_id] = (ip_addr, server_port, thread) #change to is connected

            except socket.error as e:
                print(f"250 Failed to connect to peer {peer_id} at {ip_addr}:{server_port}. Error: {str(e)} \n")
                client_socket.close()

    else:
       print(f"Peer {peer_id} does not exist")


class PeerThread(threading.Thread):
    def __init__(self, peer_id, client_socket):
        threading.Thread.__init__(self)
        self.peer_id = peer_id
        self.client_socket = client_socket
        print("Thread started")

    def filelist(self):
        print(f"Client({self.peer_id}): #FILELIST")

        # send filelist request to peer server
        self.client_socket.send("#FILELIST".encode())

        response = self.client_socket.recv(1024)
        
        print(f"Server {self.peer_id}: 200 Files served: {response.decode()}")

        pass

    def upload(self, filename):
        print(f"uploading {filename} to peer {self.peer_id}")
        pass

    def download(self, filename):
        print(f"downloading {filename} from peer {self.peer_id}")
        pass






def main():

    # get peers 
    read_peer_settings()

    while True:

        user_input = input("\n Input your command: ")
        try:
            command, parameters = user_input.split(" ", 1)

            if command not in ["#FILELIST", "#UPLOAD", "#DOWNLOAD"]:
                print("Invalid command. Supported commands are: #FILELIST, #UPLOAD, #DOWNLOAD")

            elif command == "#FILELIST":
                peer_ids = parameters.split(" ")
                print("temp, peers entered:", peer_ids)

                # multithreading the peers
                for peer_id in peer_ids:
                    connect_to_peer(peer_id)
                    ip_addr, server_port, thread = peers_dict[peer_id]
                    thread.filelist()


            elif command == "#UPLOAD":
                filename, inputed_peers = parameters.split(" ", 1)
                pass

            elif command == "#DOWNLOAD":
                filename, inputed_peers = parameters.split(" ", 1)

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

print("temp peers dirc:", peers_dict)

