from socket import *
import os

SERVER_IP = "127.0.0.1"
SERVER_PORT = 8889
BUFFER_SIZE = 1024

def connectToServer():
    s = socket(AF_INET,SOCK_STREAM)
    s.connect((SERVER_IP, SERVER_PORT))
    return s

def send_image(socket, image_location):
    file = open(image_location, "rb")
    data = file.read(1024)
    while(data):
        socket.send(data)
        data = file.read(1024)
    socket.close()

def send_name(socket, image_location):
    file_name = os.path.basename(image_location)
    socket.send(file_name.encode())
    socket.recv(512)

def send(image_path):
    socket = connectToServer()
    send_name(socket, image_path)
    send_image(socket, image_path)

if __name__ == "__main__":
    send("../images/smallfire.jpg")
