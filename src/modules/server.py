from socket import *

HOST = ''
PORT = 8889
BUFFER_SIZE = 1024

def create_server():
    s = socket(AF_INET,SOCK_STREAM)
    s.bind((HOST, PORT))
    s.listen(1)
    return s

def recv_name(socket):
    data = socket.recv(128)
    name = data.decode('utf-8')
    socket.send(b"Name Received")
    return name

def recv_image(socket, name):
    file = open(name, "wb")
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
        name = recv_name(c)
        recv_image(c, name)
    socket.close()

if __name__ == "__main__":
    receiver()