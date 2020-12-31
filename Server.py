import concurrent
import socket
import struct
import threading
import time
from concurrent.futures import thread
from termcolor import colored


class Server:
    def __init__(self):
        self.udpSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)  # UDP
        self.udpSocket.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        #self.udpSocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.hostName = socket.gethostname()
        self.hostIP = socket.gethostbyname(self.hostName)
        self.port = 2043
        self.teams = []
        self.tcpSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.devNet = "172.1.255.255"
        self.portForSendsUdp = 13117
        self.gameTime = 10 ## sec
        self.bufferSize = 1024


    def sendUdpBroadcast(self):
        ## this thread sending offers every 1 sec
        threading.Timer(1.0,self.sendUdpBroadcast).start()
        #  sock.settimeout(2)
        message = struct.pack("Ibh",0xfeedbeef,0x2,self.port)
        self.udpSocket.sendto(message, (self.devNet, self.portForSendsUdp)) ## send port to connect with tcp connection


    def StartClickGame(self,client):
        """ this func gets a Client connected to game
        and start counting his keyboard presses
        this Func return how many buttons Client click"""
        counter = 0
        start = time.time()
        while time.time() - start < self.gameTime:

            try:
                client.settimeout(0.01)
                chartype = client.recv(self.bufferSize).decode("utf-8")
                counter += len(chartype)
            except:
                pass

        return counter

    def waitForClients(self):
        """ this func is the first stage of server
                here server start to send offers to clients in net
                and listen for Tcp connections for Players that want to join
                this Func update in Self.Teams the Clients that Registered """
        startTime = time.time()
        threading.Thread(target=server.sendUdpBroadcast).start()

        while time.time() - startTime < 10:
            self.tcpSocket.settimeout(0.1)
            try:
                client, addr = self.tcpSocket.accept()
                groupName = client.recv(self.bufferSize).decode("utf-8")
                time.sleep(0.1)
                self.teams.append((client,addr,groupName))
                print(colored(f'{groupName} in the game', 'red'))
            except:
                continue



## flow of the game
if __name__ == '__main__':
    server = Server()
    con=False
    while not con:
        try:
            server.tcpSocket.bind(("", server.port))
            con=True
        except:
            pass
    server.tcpSocket.listen()
    while 1:
        server.teams = []
        ## starting msg
        print(colored(f"Server started,listening on IP address {server.hostIP}",'red'))
        ## start sending udp offer annoucements via udp broadcast once every second
        server.waitForClients()

        ## we got players


        groupEven = ""
        groupOdd = ""
        for i in range(0, len(server.teams), 2):
            groupEven+=server.teams[i][2]
        for j in range(1, len(server.teams), 2):
            groupOdd+=server.teams[j][2]

        if len(server.teams) == 0: #or len(server.teams) == 1:
            continue

        welcomeMsg = f"Welcome to Keyboard Spamming Battle Royale.\nGroup 1:\n==\n{groupEven}\nGroup 2:\n==\n{groupOdd}\n\n" \
                     f"Start pressing keys on your keyboard as fast as you can!!"

        for client in server.teams:
            client[0].sendall(bytes(welcomeMsg, "utf-8"))
        print(colored(welcomeMsg,'red'))


        Group1Res = 0
        Group2Res = 0

        with concurrent.futures.ThreadPoolExecutor(len(server.teams)) as pool:

            results = []
            for client in server.teams:
                clientPlay = pool.submit(server.StartClickGame, client[0])
                results.append(clientPlay)



            for i in range(0, len(server.teams), 2):
                Group1Res += results[i].result()
            for j in range(1, len(server.teams), 2):
                Group2Res += results[j].result()
            winTeam = ''
            teamsInGroup = ''
            if Group1Res > Group2Res:
                winTeam = "Group 1 wins!"
                teamsInGroup = groupEven
            elif Group2Res > Group1Res:
                winTeam = "Group 2 wins!"
                teamsInGroup = groupOdd
            else:
                winTeam = "Draw"
            gameOvermsg = f"Game over!\nGroup 1 types in {Group1Res} characters. Group 2 typed in {Group2Res} characters.\n{winTeam}\n\nCongratulations to the winners:\n==\n{teamsInGroup}"
            print(colored(gameOvermsg,'red'))
            ## send game over msg to all clients !


            for client in server.teams:
                try:
                    client[0].send(bytes(f"Game over!\nGroup 1 types in {Group1Res} characters. Group 2 typed in {Group2Res} characters.\n{winTeam}\n\nCongratulations to the winners:\n==\n{teamsInGroup}","utf-8"))
                except:continue
            ## close every conection
            for client in server.teams:
                try:
                    client[0].close()
                except:continue

            print(colored("Game over, sending out offer requests...",'red'))




