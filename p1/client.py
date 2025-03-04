import socket
import threading
import os

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

                # print(f"200 Connected to peer {peer_id} at {ip_addr}:{server_port} \n")

                #create thread
                thread = PeerThread(peer_id, client_socket)
                # t = threading.Thread(target=con, args=(client_socket,))
                thread.start()


                peers_dict[peer_id] = (ip_addr, server_port, thread) #change to is connected
                return True


            except socket.error as e:
                print(f"Client({peer_id}): 250 TCP connection to server {peer_id} failed")
                client_socket.close()
                return False
            
        else:
            return True

    else:
       print(f"Client({peer_id}): 250 Peer does not exist")
       return False


class PeerThread(threading.Thread):
    def __init__(self, peer_id, client_socket):
        threading.Thread.__init__(self)
        self.peer_id = peer_id
        self.client_socket = client_socket

    def filelist(self):
        print(f"Client({self.peer_id}): #FILELIST")

        # send filelist request to peer server
        self.client_socket.send("#FILELIST".encode())

        response = self.client_socket.recv(1024)
        
        print(response.decode())

        pass

    def upload(self, filename):

        files = os.listdir("./served_files")

        if filename in files:

            #get size and file
            file_size = os.path.getsize(f"./served_files/{filename}")
            file = open(f"./served_files/{filename}", "rb")


            # send upload request
            request = f"#UPLOAD {filename} bytes {file_size}"
            self.client_socket.send(request.encode())
            print(f"Client({self.peer_id}): {request}")

            #get reply
            reply = self.client_socket.recv(1024).decode()
            print(reply)
            parts = reply.split(" ")
            status_code = int(parts[2])
            print(status_code)
            

            if status_code == 330:
                chunk_num = 0

                while True:
                    chunk = file.read(100) #read 100 bytes
                  
                    if not chunk:
                        break
                        
                    chunk_num += 1

                    request = f"#UPLOAD {filename} chunk {chunk_num} {chunk}"
                    print(f"Client({self.peer_id}): {request}")

                    reply = self.client_socket.recv(1024).decode()

                    print("\n")

            
        
        pass

    def download(self, filename):
        print(f"downloading {filename} from peer {self.peer_id}")
        pass






def main():

    # get peers 
    read_peer_settings()

    while True:

        user_input = input("\nInput your command: ")
        try:
            command, parameters = user_input.split(" ", 1)

            if command not in ["#FILELIST", "#UPLOAD", "#DOWNLOAD", "u"]:
                print("Invalid command. Supported commands are: #FILELIST, #UPLOAD, #DOWNLOAD")

            elif command == "#FILELIST":
                inputed_peers = parameters.split(" ")

                # multithreading the peers
                for peer_id in inputed_peers:
                    if connect_to_peer(peer_id):
                        thread = peers_dict[peer_id][2]
                        thread.filelist()


            elif command == "u":




                if connect_to_peer("p1"):
                    thread = peers_dict["p1"][2]
                    thread.upload("f3.txt")

                #                 filename, inputed_peers = parameters.split(" ", 1)
                # inputed_peers = inputed_peers.split(" ")
               
                # for peer_id in inputed_peers:
                #     if connect_to_peer(peer_id):
                #         thread = peers_dict[peer_id][2]
                #         thread.upload(filename)


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

