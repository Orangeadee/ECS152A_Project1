from ctypes import sizeof
from socket import *
import time
import math
import random
import os

def client_send():
    serverName = '173.230.149.18'
    serverPort = 5006

    clientSocket = socket(AF_INET, SOCK_DGRAM)

    message = 'ping'
    path = './data.txt'
    totalSize = 1300000

    data_file = open(path, 'a')
    size = os.path.getsize(path)
    percentage = 0
    clientSocket.sendto(message.encode(),(serverName, serverPort))
    clientSocket.settimeout(30)
    now = time.time()
    while(size <= totalSize):
        modifiedMessage, serverAddress = clientSocket.recvfrom(4096)

        data_file.write(modifiedMessage.decode())
        data_file.flush()
        os.fsync(data_file.fileno())

        
        percentage = os.path.getsize(path) / totalSize * 100
        print("received %: ", int(percentage))
        size = os.path.getsize(path)
    now = time.time() - now
    print("break")
    print("Time elapsed: {} seconds".format(now))
    throu = size / now
    print("Throughput: {} bps".format(throu))
    print("Size of file is {} bites".format(size))
    print("File Downloaded")



def main():
    client_send()

if __name__=="__main__":
    main()