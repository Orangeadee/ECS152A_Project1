from ctypes import sizeof
from socket import *
import time
import math
import random
import os

def client_send():
    # Given server Name and Port Number.
    serverName = '173.230.149.18'
    serverPort = 5006

    # Connect socket with udp protocal.
    clientSocket = socket(AF_INET, SOCK_DGRAM)

    # Message to send is ping.
    # Path is where data are stored.
    # TotalSize is the total size to be stored.
    message = 'ping'
    path = './data.txt'
    totalSize = 1300000

    # Open the data file with permission 'a' to prevent overwrite.
    data_file = open(path, 'a')
    # Record the size of the file.
    size = os.path.getsize(path)
    # For storing further calculation of how many bytes written in the file.
    percentage = 0
    # Start sending message to the server, only sending one time.
    clientSocket.sendto(message.encode(),(serverName, serverPort))
    # Set timeout to 30 seconds: stop the program if can't receive the message in 30 seconds.
    # The prompt said to set timeout to 10 seconds, but it will timeout before the data file
    # is written 100%, it needs more time to receive data from the server. 
    # Hence, we decide to set timeout to 30 seconds.
    clientSocket.settimeout(30)
    now = time.time()
    while(size <= totalSize):
        # Receive message from the server and write the message to the data file.
        modifiedMessage, serverAddress = clientSocket.recvfrom(4096)
        data_file.write(modifiedMessage.decode())
        data_file.flush()
        os.fsync(data_file.fileno())
        
        # Calculating the percentage of data file written / total size to be written.
        percentage = os.path.getsize(path) / totalSize * 100
        # Print the result.
        print("received %: ", int(percentage))
        # Update the size of data file.
        size = os.path.getsize(path)

    # ========================= Print Final Result ========================= #
    # Get the total time spent when writing to the data file.
    now = time.time() - now
    print("break")
    print("Time elapsed: {} seconds".format(now))
    # Thoroughput = size of the file / total time
    throu = size / now
    print("Throughput: {} bps".format(throu))
    print("Size of file is {} bites".format(size))
    print("File Downloaded")

def main():
    client_send()

if __name__=="__main__":
    main()