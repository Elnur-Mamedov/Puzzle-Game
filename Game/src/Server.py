import socket


class Server:
    def __init__(self):
        self.main_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.main_socket.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)

        hostname = socket.gethostname()
        ip_address = socket.gethostbyname(hostname)

        self.main_socket.bind((ip_address, 10000))
        self.main_socket.listen(2)

        self.start = False
        self.players = []
        self.draw()

    def draw(self):
        data = None
        check = True
        while True:
            # Gathering the players
            if not self.start:
                try:
                    new_soccket, addr = self.main_socket.accept()
                    self.players.append(new_soccket)
                    print('Connected by', addr)

                    if len(self.players) == 1:
                        self.players[0].send("Send".encode())
                        data = self.players[0].recv(1080249).decode()
                    elif len(self.players) == 2:
                        self.players[1].send(data.encode())
                        self.start = True
                except:
                    pass
            else:
                if check:
                    data = self.players[0].recv(1024).decode()
                    check = False
                else:
                    self.players[1].send(data.encode())
                    data = self.players[1].recv(1024).decode()
                    self.players[0].send(data.encode())
                    check = True

server = Server()
