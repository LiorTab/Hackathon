import socket
import struct
import time


import getch
# import msvcrt

# def __init__(self):
#     self.udpSocket =         sock = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
#     sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1) ## multi clients
#     sock.bind(("",13117))


def lookingForServer():
    ## state 1
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)  ## multi clients
    sock.bind(("", 13117))
    return sock.recvfrom(1024)


def startPlaying(tcpSocket):
    ## game state
    try:
        start = time.time()
        while time.time() - start < 10:
            val = getch.getch() ## TODO GETCH
            tcpSocket.send(bytes(val, "utf-8"))
        msgFromServer = tcpSocket.recv(1024).decode("utf-8")
        print(msgFromServer)
    except:return

def connectTcp(addr, portNum):
    tcpIp, _ = addr
    tcpSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # TCP
    tcpSocket.connect((tcpIp, portNum))
    tcpSocket.send(bytes("BlackShadow", "utf-8")) # TODO THINK !!!!!!!!!!!!
    data = tcpSocket.recv(1024).decode("utf-8")
    print(data)  ## print welcome msg
    ## game state
    startPlaying(tcpSocket)


def getPort(receivedData):
    # check if message is correct type - if yes return port number else return None
    try:
        print(struct.unpack("Ibh", receivedData))
        unPackMsg = struct.unpack("Ibh", receivedData)
        if unPackMsg[0] != 4276993775 or unPackMsg[1] != 2 or unPackMsg[2] < 1024 or unPackMsg[2] > 32768:
            return None
    except:  # message format not good (needs to be "Ibh")
        return None
    return unPackMsg[2]


def startClient():
    print("Client started, listening for offer requests...")
    ## wait for offers
    while True:
        receivedData, addr = lookingForServer()  ## check buffer size
        print(f"Received offer from {addr[0]},attempting to connect...")
        ## state 2
        # print(struct.unpack("Ibh",receivedData))
        # verify what message
        portNum = getPort(receivedData)  # if message type is not good - returns None
        ## TODO what rejected means ?!?!?!!?!
        if portNum is None:
            continue
        ## attempting to connect TCP
        connectTcp(addr, portNum)
        print("Server disconnected, listening for offer requests...")
        ## continue to wait for offers


startClient()
