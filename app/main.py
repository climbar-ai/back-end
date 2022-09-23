# References:
# 1. https://stackoverflow.com/questions/46964007/python-socket-connection-between-raspberry-pi-s
# 2. https://stackoverflow.com/questions/56194446/send-big-file-over-socket
# 3. https://stackoverflow.com/questions/55839932/sending-encrypted-data-through-socket-and-decrypting-doesnt-work/55840341#55840341
# 4. https://medium.datadriveninvestor.com/connecting-the-microsoft-hololens-and-raspberry-pi3b-58665032964c
# 5. https://nikhilroxtomar.medium.com/file-transfer-using-tcp-socket-in-python3-idiot-developer-c5cf3899819c


import os
import socket
import threading

IP = '0.0.0.0'
PORT = 8081
BUFFER_SIZE = 1024
FORMAT = "utf-8"
HOLD_CONFIGS_DIR = '/share/hold-configurations'

def start_server(host='', port=PORT):
    global sock_server
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind((host, port))
    s.listen()

    print("host: {}".format(host))
    print("port: {}".format(port))
   
    while True:
        sock_server, sockname = s.accept()
        print("Connection found -> sock_server: {}, sockname: {}".format(sock_server, sockname))
        break


def receiveTCP(sock):
    message = sock.recv(BUFFER_SIZE).decode(FORMAT)
    return message


def stopAlarm(sock):
    print("'stop alarm' recieved")
    sock.send("alarm stopped".encode(FORMAT))
    pass


def startAlarm(sock):
    print("'start alarm' recieved")
    sock.send("alarm started".encode(FORMAT))
    pass

def closeSock(sock):
    print("'close sock' recieved")
    sock.send("closed socket".encode(FORMAT))
    sock.close()

    # restart server to listen for new connections
    start_server(IP, PORT)


def receiveFilename(sock):
    # receive filename
    filename = sock.recv(BUFFER_SIZE).decode(FORMAT)
    print("[RECV] Receiving the filename: {}".format(filename))
    return filename


def receiveFile(sock):
    # let client know server is ready to receive
    sock.send("ready".encode(FORMAT));

    # receive filename from client
    filename = receiveFilename(sock)
    
    # send confirmation of receipt
    sock.send("ready".encode(FORMAT))

    # receive file data from client
    print("[RECV] Receiving the file data.")
    filepath = os.path.join(HOLD_CONFIGS_DIR, filename)
    with open(filepath,'wb') as file:
        while True:
            # read chunk of flie
            recvfile = sock.recv(BUFFER_SIZE) # don't decode here since file.write wants a bytes-like object instead of string
            if not recvfile or recvfile.decode(FORMAT) == "done": # break if the port is closed or client signals they are done
                break
            file.write(recvfile)
            
            # send confirmation of receipt
            sock.send("ready".encode(FORMAT))
    print("[RECV] File has been received: {}".format(filename))


def sendFile(sock):
    # receive filename from client
    filename = receiveFilename(sock)

    # send the filename to client
    sock.sendall(filename.encode(FORMAT))

    # send the file to client
    filepath = os.path.join(HOLD_CONFIGS_DIR, filename)
    with sock, open(filepath,'rb') as f:
        data = f.read()
        sock.sendall(data)
    print("[RECV] File has been sent {}".format(filename))   


class Waiter(threading.Thread):
    def __init__(self, **kwargs):
        super(Waiter, self).__init__(**kwargs)

    def run(self):
        global sock_server
        while True:
            try:
                message = receiveTCP(sock_server)
            except Exception:
                pass
            else:
                print("message: {}".format(message))
                if message != '':
                    if message == 'stopAlarm':
                        stopAlarm(sock_server)
                    elif message == 'startAlarm':
                        startAlarm(sock_server)
                    elif message == 'closeSock':
                        closeSock(sock_server)
                    elif message == 'receiveFile':
                        receiveFile(sock_server)
                    elif message == 'sendFile':
                        sendFile(sock_server)
                    sock_server.send("ready".encode(FORMAT))

if __name__ == '__main__':  
    ## we expect, as a hand-shake agreement, that there is a .yml config file in top level of lib/configs directory
    #config_dir = os.path.join('.')
    #yaml_path = os.path.join(config_dir, 'main.yml')
    #with open(yaml_path, "r") as stream:
    #    config = yaml.load(stream)

    sock_server = None
    start_server(IP, PORT) # pass the host and the port as parameters
    Waiter().start() #start the thread which will wait for messages from client