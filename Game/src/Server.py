import socket
import time
import json


class Server:
    def __init__(self):
        self.main_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.main_socket.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)

        hostname = socket.gethostname()
        ip_address = socket.gethostbyname(hostname)
        with open('ipadress.json', 'w') as f:
            print(ip_address)
            json.dump(ip_address, f)

        self.main_socket.setblocking(0)

        self.main_socket.bind((ip_address, 10000))
        self.main_socket.listen(2)

        self.players = []
        self.draw()

    def draw(self):
        while True:
            try:
                new_soccket, addr = self.main_socket.accept()
                self.players.append(new_soccket)
                print('Connected by', addr)

                data = new_soccket.recv(1024)

                message = data.decode()
                print("Получено от клиента:", message)
            except:
                pass

            time.sleep(1)

server = Server()
