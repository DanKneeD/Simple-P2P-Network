import socket
import threading
import os

threads = {}



#fetching file list
def filelist():
    try:
        return os.listdir("./served_files")
    except Exception as e:
        print('An error occurred while fetching file list', str(e))
        return []





class serverThread(threading.Thread):
    def __init__(self, client):
        print("initlizing server")
        threading.Thread.__init__(self)
        self.client = client


    def run(self):
        print("Starting new server thread, run")
        connectionSocket, addr = self.client

        while True:
            try:
                print("decoding message from socket")
                message = connectionSocket.recv(1024).decode()


                print(f'Received message from {connectionSocket}: {message}')

                if message not in ["#FILELIST", "#UPLOAD", "#DOWNLOAD"]:
                    print("Invalid command. Supported commands are: #FILELIST, #UPLOAD, #DOWNLOAD")
                    connectionSocket.send("Invalid command. Supported commands are: #FILELIST, #UPLOAD, #DOWNLOAD".encode())

                elif message == "#FILELIST":
                    files = filelist()
                    connectionSocket.send(", ".join(files).encode()) 

            except Exception as e:
                print('An error occurred during communication', str(e))
                break
            finally:
                print("closing connection")
                connectionSocket.close()  



class mainThread():

    def server_run():
       
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        server.bind(('localhost', 5001))

        print("main thread listening")
        server.listen()
        while True:
            try:

                # connection_socket, address = server.accept()
                # print(f'Connection from {address} established. Connection ID: {id(connection_socket)} and connection socket: {connection_socket}')
                # newthread = serverThread(connection_socket, address)
                # newthread.start()

                # threads[id(connection_socket)] = newthread
                # print(f'Thread {id(connection_socket)} started.')
                client = server.accept()
                t = serverThread(client)
                t.start()
            except Exception as e:
                print('An error occurred during connection', str(e))


print('Server is listening...')
mainThread.server_run()