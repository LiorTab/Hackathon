import socket
import struct


def connectTcp(addr):
    tcpIp,tcpPort = addr
    tcpSocket = socket.socket(socket.AF_INET,socket.SOCK_STREAM) #TCP
    tcpSocket.connect((tcpIp,tcpPort))


def startClient():
    print("Client started, listening for offer requests...")
    ## wait for offers
    udp_ip = "255.255.255.255"
    udp_port = 5005

    sock = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
    sock.bind(("",udp_port))

    while 1:
        recivedData , addr = sock.recvfrom(1024) ## check buffer size
        print(f"Received offer from {addr[0]},attempting to connect...")
        print(addr)
        ## attempting to connect TCP
        # connectTcp(addr)
        # break ?


startClient()