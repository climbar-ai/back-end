import socket
import threading

IP = '0.0.0.0'
PORT = 8081
SIZE = 1024
FORMAT = "utf-8"

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
    message = sock.recv(SIZE).decode(FORMAT)
    return message


def stopAlarm(sock):
    print("'stop alarm' recieved")
    sock.send("alarm stopped".encode(FORMAT));
    pass


def startAlarm(sock):
    print("'start alarm' recieved")
    sock.send("alarm started".encode(FORMAT));
    pass


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
                if message != '':
                    if message == 'stop alarm':
                        stopAlarm(sock_server)
                    elif message == 'start alarm':
                        startAlarm(sock_server)
                    sock_server.close()
                    break

if __name__ == '__main__':  
    ## we expect, as a hand-shake agreement, that there is a .yml config file in top level of lib/configs directory
    #config_dir = os.path.join('.')
    #yaml_path = os.path.join(config_dir, 'main.yml')
    #with open(yaml_path, "r") as stream:
    #    config = yaml.load(stream)

    sock_server = None
    start_server(IP, PORT) # pass the host and the port as parameters
    Waiter().start() #start the thread which will wait for messages from client