import socket
import struct
import time
#import getch
import msvcrt


def startPlaying(tcpSocket):
    start = time.time()
    while time.time() - start < 10:
        val = input("Enter: ")
        tcpSocket.send(bytes(val, "utf-8"))
    print("Server disconnected, listening for offer requests...")


def connectTcp(addr,recivedData):
    tcpIp,tcpPort = addr
    tcpSocket = socket.socket(socket.AF_INET,socket.SOCK_STREAM) #TCP
    print(tcpIp)
    print(tcpPort)
    tcpSocket.connect((tcpIp,5555))

    tcpSocket.send(bytes("Dolphin","utf-8"))
    data = tcpSocket.recv(1024).decode("utf-8")
    print(data) ## print welcome msg
    startPlaying(tcpSocket)


def checkMessageTypes(recivedData):
    return True


def startClient():
    print("Client started, listening for offer requests...")
    ## wait for offers
    udp_ip = "255.255.255.255"
    udp_port = 5005
    flag = 0

    sock = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1) ## multi clients
    sock.bind(("",13117))
    recivedData, addr = sock.recvfrom(1024)  ## check buffer size
    print(f"Received offer from {addr[0]},attempting to connect...")

    while 1:

        # print(addr)
        # print(struct.unpack("Ibh",recivedData))
        #sock.close()
        # verify what message
        check = checkMessageTypes(recivedData)
        ## what rejected means ?!?!?!!?!?
        if not check:break
        ## attempting to connect TCP
        if flag==0:
            connectTcp(addr,recivedData)
            flag=1
        # break ?


startClient()