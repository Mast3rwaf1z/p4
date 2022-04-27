from socket import *
import cv2
import threading

HOST = ''
PORT = 8889
BUFFER_SIZE = 1024

def display_image_thread(filepath):
    x = cv2.imread(filepath)
    cv2.imshow(filepath, x)
    cv2.waitKey()

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
    file = open("photos/"+name, "wb")
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
    threads = []
    while True:
        c,a = s.accept()
        print('* Connection received from {}'.format(a))
        name = recv_name(c)
        recv_image(c, name)
        thread = threading.Thread(target=display_image_thread, args=('photos/'+name, ))
        threads.append(thread)
        thread.start()
    for x in threads:
        x.join()
    socket.close()

if __name__ == "__main__":
    receiver()
