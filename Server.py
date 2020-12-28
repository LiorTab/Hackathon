import socket
import struct
import threading

class Server:
    def __init__(self):
        self.udpSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)  # UDP
        self.udpSocket.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)

        self.hostName = socket.gethostname()
        self.hostIP = socket.gethostbyname(self.hostName)





    def sendUdpBroadcast(self):
        #  sock.settimeout(2)
        while True:
            port = 5555 ## tcp port
            self.udpSocket.sendto(bytes("test", "utf-8"), ("255.255.255.255", 5005)) ## send port to connect with tcp connection

        #threading.sleep(1)


    def StartClickGame(self):
        ## starting msg
        print(f"Server started,listening on IP address {self.hostIP}")
        ## start sending udp offer annoucements via udp broadcast once every second
        self.sendUdpBroadcast()



        ## all clients gets this annoucements “Received offer from 172.1.0.4,attempting to connect...”
        tcpSocket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        tcpSocket.bind((self.hostIP,5555))


server = Server()
server.StartClickGame()