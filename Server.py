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
        self.port = 5555
        self.StartGameMessage ="Welcome to Keyboard Spamming Battle Royale. \n"

    def sendUdpBroadcast(self):
        threading.Timer(1.0,self.sendUdpBroadcast).start()
        #  sock.settimeout(2)
        message = struct.pack("Ibh",0xfeedbee,0x2,self.port)
        self.udpSocket.sendto(message, ("<broadcast>", 13117)) ## send port to connect with tcp connection


    def StartClickGame(self,client):
        counter = 0
        start = time.time()
        while time.time() - start < 10:

            client.settimeout(10)
            try:
                chartype = client.recv(1024).decode("utf-8")
                print(chartype)
                counter += len(chartype)
            except:
                pass

        return counter


if __name__ == '__main__':

    server = Server()
    ## starting msg
    print(f"Server started,listening on IP address {server.hostIP}")
    teams = []
    ## start sending udp offer annoucements via udp broadcast once every second
    threading.Thread(target=server.sendUdpBroadcast).start()
    startTime = time.time()
    tcpSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    tcpSocket.bind(("", server.port))
    with concurrent.futures.ThreadPoolExecutor(2) as pool:
        while time.time() - startTime < 10:
            # all clients gets this annoucements “Received offer from 172.1.0.4,attempting to connect...”

            tcpSocket.listen(3)  ## max clients
            startTime = time.time()
            client, addr = tcpSocket.accept()

            groupName = client.recv(1024).decode("utf-8")
            time.sleep(0.1)
            teams.append(groupName)
            print(f"team {len(teams)} name is {groupName}")
            client1, addr1 = tcpSocket.accept()
            groupName1 = client1.recv(1024).decode("utf-8")
            time.sleep(0.1)
            teams.append(groupName1)
            print(f"team {len(teams)} name is {groupName1}")
            break

        print("now we start to play!")
        ## print group devide
        welcomeMsg = f"Welcome to Keyboard Spamming Battle Royale.\nGroup 1:\n==\n{teams[0]}\nGroup 2:\n==\n{teams[1]}\n\n" \
                     f"Start pressing keys on your keyboard as fast as you can!!"

        # time.sleep(10)
        client.sendall(bytes(welcomeMsg,"utf-8"))
        client1.sendall(bytes(welcomeMsg,"utf-8"))

        firstGroup = pool.submit(server.StartClickGame,client)
        secondGroup = pool.submit(server.StartClickGame,client1)
        client.sendall(bytes("times up!","utf-8"))
        client1.sendall(bytes("times up!","utf-8"))

        firstGroupRes = firstGroup.result()
        secondGroupRes = secondGroup.result()
        print(f"Game over!\nGroup 1 types in {firstGroupRes} characters. Group 2 typed in {secondGroupRes} characters.")
        if firstGroupRes>secondGroupRes:
            print("Group 1 wins!")
        elif secondGroupRes > firstGroupRes:
            print("Group 2 wins!")
        else:
            print("Draw")

    client.close()
    client1.close()

    print("Game over, sending out offer requests...")


