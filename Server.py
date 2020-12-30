import concurrent
import socket
import struct
import threading
import time
from concurrent.futures import thread


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



    def sendUdpBroadcast(self):
        threading.Timer(1.0,self.sendUdpBroadcast).start()
        #  sock.settimeout(2)
        message = struct.pack("Ibh",0xfeedbeef,0x2,self.port)
        self.udpSocket.sendto(message, ("<broadcast>", 13117)) ## send port to connect with tcp connection


    def StartClickGame(self,client):
        counter = 0
        start = time.time()
        while time.time() - start < 10:

            client.settimeout(10)
            try:
                chartype = client.recv(1024).decode("utf-8")
                counter += len(chartype)
            except:
                pass

        return counter

    def waitForClients(self):
        startTime = time.time()
        threading.Thread(target=server.sendUdpBroadcast).start()

        while time.time() - startTime < 10:
            self.tcpSocket.settimeout(0.1)
            try:
                client, addr = self.tcpSocket.accept()
                groupName = client.recv(1024).decode("utf-8")
                time.sleep(0.1)
                self.teams.append((client,addr,groupName))
            except:continue






if __name__ == '__main__':
    server = Server()
    server.tcpSocket.bind(("", server.port))
    server.tcpSocket.listen()
    while 1:
        server.teams = []
        ## starting msg
        print(f"Server started,listening on IP address {server.hostIP}")
        ## start sending udp offer annoucements via udp broadcast once every second
        server.waitForClients()

        ## we got players


        groupEven = ""
        groupOdd = ""
        for i in range(0, len(server.teams), 2):
            groupEven+=server.teams[i][2]
        for j in range(1, len(server.teams), 2):
            groupOdd+=server.teams[j][2]

        if len(server.teams) == 0 or len(server.teams) == 1:
            continue

        welcomeMsg = f"Welcome to Keyboard Spamming Battle Royale.\nGroup 1:\n==\n{groupEven}\nGroup 2:\n==\n{groupOdd}\n\n" \
                     f"Start pressing keys on your keyboard as fast as you can!!"

        for client in server.teams:
            client[0].sendall(bytes(welcomeMsg, "utf-8"))


        Group1Res = 0
        Group2Res = 0

        with concurrent.futures.ThreadPoolExecutor(len(server.teams)) as pool:
            # time.sleep(10)

            # client1.sendall(bytes(welcomeMsg,"utf-8"))
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

            for client in server.teams:
                client[0].send(bytes(f"Game over!\nGroup 1 types in {Group1Res} characters. Group 2 typed in {Group2Res} characters.\n{winTeam}\n\nCongratulations to the winners:\n==\n{teamsInGroup}","utf-8"))





            for client in server.teams:
                client[0].close()


            print("Game over, sending out offer requests...")




