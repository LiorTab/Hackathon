import socket
import struct
import time
from termcolor import colored


import getch
# import msvcrt


def lookingForServer():
    ## state 1
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)  ## multi clients
    sock.bind(("", 13117))
    get_message=None
    while get_message is None:
        try:
            sock.settimeout(0.5)
            get_message= sock.recvfrom(1024)
        except:
            continue
    return get_message

def startPlaying(tcpSocket):
    ## game state
    try:
        start = time.time()
        while time.time() - start < 10:
            val = getch.getch()
            tcpSocket.sendall(bytes(val, "utf-8"))
        msgFromServer = tcpSocket.recv(1024).decode("utf-8")
        print(colored(msgFromServer,'blue'))
    except:
        return

def connectTcp(addr, portNum):
    tcpIp, _ = addr
    #tcpIp="127.0.0.1"  # for check our server
    #portNum=2043
    tcpSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # TCP
    tcpSocket.connect((tcpIp, portNum))
    tcpSocket.send(bytes("BlackShadow"+"\n", "utf-8"))
    data = tcpSocket.recv(1024).decode("utf-8")
    print(data)  ## print welcome msg
    ## game state
    startPlaying(tcpSocket)


def getPort(receivedData):
    # check if message is correct type - if yes return port number else return None
    try:
        # print(struct.unpack("Ibh", receivedData))
        unPackMsg = struct.unpack("Ibh", receivedData)
        if unPackMsg[0] != 4276993775 or unPackMsg[1] != 2 or unPackMsg[2] < 1024 or unPackMsg[2] > 32768:
            return None
    except:  # message format not good (needs to be "Ibh")
        return None
    return unPackMsg[2]

## Flow of Client
def startClient():
    print(colored("Client started, listening for offer requests...",'yellow'))
    ## wait for offers
    while True:
        receivedData, addr = lookingForServer()  ## check buffer size
        print(colored(f"Received offer from {addr[0]},attempting to connect...",'red'))
        ## state 2
        # print(struct.unpack("Ibh",receivedData))
        # verify what message
        portNum = getPort(receivedData)  # if message type is not good - returns None
        ## continue wait for others if None
        if portNum is None:
            continue
        ## attempting to connect TCP
        try:
            connectTcp(addr, portNum)
        except:
            continue
        print(colored("Server disconnected, listening for offer requests...",'blue'))
        ## continue to wait for offers


startClient()
