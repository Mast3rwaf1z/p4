from socket import *
import cv2
import sys
import subprocess

HOST = ''
PORT = 8889
BUFFER_SIZE = 1024

def openImage(path):
    imageViewerFromCommandLine = {'linux':'xdg-open',
                                  'win32':'explorer',
                                  'darwin':'open'}[sys.platform]
    subprocess.run([imageViewerFromCommandLine, path])

def create_server():
    s = socket(AF_INET,SOCK_STREAM)
    s.bind((HOST, PORT))
    s.listen(1)
    return s

def recv_name(socket):
    data = socket.recv(32)
    for i in data:
        if(i == 35):
            name = data[:data.index(i)]
            data = data[data.index(i)+1:]
    return name.decode("utf-8"), data

def recv_image(socket, name, data_initial):
    file = open("photos/"+name, "wb")
    file.write(data_initial)
    while True:
        data = socket.recv(BUFFER_SIZE)
        while data:
            file.write(data)
            data = socket.recv(BUFFER_SIZE)
        break
    file.close()
    print("{} saved".format(name))

def receiver():
    s = create_server()
    while True:
        c,a = s.accept()
        print('* Connection received from {}'.format(a))
        name, data = recv_name(c)
        recv_image(c, name, data)
        openImage('photos/'+name)
        c.close()
        c,a = s.accept()
        coordinates = c.recv(1024)
        print(f'Coordinates of fire: {coordinates.decode()}')
        c.close()
    s.close()

if __name__ == "__main__":
    receiver()
