import socket
import threading
import os

threads = []
server_id = os.path.basename(os.getcwd()) 



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
        self.connectionSocket , self.addr = client
        self.isServing = False


    def run(self):
        print("Starting new server thread, run")

        while True:
            try:
                request = self.connectionSocket.recv(1024).decode()


                if request == "#FILELIST":
                    files = filelist()
                    files = ' '.join(files) #making correct format
                    response = f"Server {server_id} : 200 Files served: {files}"
                    self.connectionSocket.send(response.encode()) 

                elif request.startswith("#UPLOAD"):
                    self.upload(request)

            except Exception as e:
                print(f'Server {server_id}: An error occurred during communication', str(e))
                self.connectionSocket.close()
                break
        print(f'WHILE TRUE HAS ENDED \n \n')

    def upload(self, request):

        if self.isServing:
            response = f"250 Currently receiving file filename"
            self.connectionSocket.send(response.encode())
            self.isServing = False
            return
        
        self.isServing = True


        parts = request.split(' ')
        filename = parts[1]
        total_file_size = int(parts[3])

        file_path = os.path.join("./served_files", filename)
        if os.path.exists(file_path):
            response = f"250 File {filename} already exists"
            self.connectionSocket.send(response.encode())
            self.isServing = False
            return


        # send confirmation
        response = f"Server({server_id}): 330 Ready to receive file {filename}"
        self.connectionSocket.send(response.encode())
        print("sent ack")

        with open(f"./served_files/{filename}", 'w') as f:
            current_file_size = 0
            while True:

                data = self.connectionSocket.recv(1024).decode()
                
                #no data
                if not data:
                    print("Client disconnected")
                    break
                
                # recive success response
                if data.find(f"File {filename} upload success") != -1:

                    #check if file same size 
                    if total_file_size != current_file_size:
                        response = f"Server({server_id}): 250 File {filename} incorrect size"
                    else:
                        response = f"Server({server_id}): 200 File {filename} received"

                    self.connectionSocket.send(response.encode())
                    break

                #split recived metadata
                split_data = data.split(" ", 4)
                data = split_data[4] #actual data
                chunk_i = split_data[3] #chunk number

                current_file_size += len(data)

                #write to file
                f.write(data)

                #acklnowledge 
                response = f"Server({server_id}): 200 File {filename} chunk {chunk_i} received"
                print(response)
                self.connectionSocket.send(response.encode())

        self.isServing = False
        print(f"given size {total_file_size} vs final size {current_file_size}")
        print("closing file")

    def download(self, request):
        parts = request.split(' ')
        if len(parts) == 2: 
            filename = parts[1]
            file_path = os.path.join("./served_files", filename)
            if os.path.exists(file_path):
                file_size = os.path.getsize(file_path)
                response = f"330 Ready to send file {filename} bytes {file_size}"
                self.connectionSocket.send(response.encode())
            else:
                response = f"250 Not serving file {filename}"
                self.connectionSocket.send(response.encode())

        elif len(parts) == 4:
            filename = parts[1]
            chunk_i = int(parts[3])
            file_path = os.path.join("./served_files", filename)
            if os.path.exists(file_path):
                with open(file_path, 'rb') as f:
                    f.seek(chunk_i * 100)  # Assuming chunk size is 100 bytes
                    chunk_data = f.read(100)
                    response = f"200 File {filename} chunk {chunk_i} {chunk_data.decode()}"
                    self.connectionSocket.send(response.encode())
            else:
                response = f"250 Not serving file {filename}"
                self.connectionSocket.send(response.encode())


class mainThread():

    def server_run():
       
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        server.bind(('localhost', 5044))

 
        server.listen()
        try:
            while True:
                try:

                    client = server.accept()
                    t = serverThread(client)
                    t.start()

                except Exception as e:
                    print('An error occurred during connection', str(e))
        except:
            print("closing server")
            server.close()
                


print('Server is listening...')
mainThread.server_run()