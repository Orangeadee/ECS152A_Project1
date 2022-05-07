from socket import *
import time
import math
import random

import statistics

def client_send():
    serverName = '173.230.149.18'
    serverPort = 12000
    timeout_seconds = 10.0
    rtt_list = []
    succeed_count = 0

    clientSocket = socket(AF_INET, SOCK_DGRAM)

    message = 'ping'

    clientSocket.sendto(message.encode(),(serverName, serverPort))
    print("here")
    modifiedMessage, serverAddress = clientSocket.recvfrom(4096)
    # print(modifiedMessage)
    
    for i in range(0,10):
        now = time.time()
        # while(time.time() - now<10):
        #     pass
        timeout_count = 0

        clientSocket.sendto(message.encode(),(serverName, serverPort))
        # print("here")
        modifiedMessage, serverAddress = clientSocket.recvfrom(4096)
        # print(modifiedMessage)
        # 丢包
        while(modifiedMessage.decode() != 'PING'):
            print("not pint!")
            if(time.time()-now >= timeout_seconds):
                print("time out!")
                inner_timeout = inner_timeout * math.pow(2,timeout_count)+random.uniform(0,1)
                inner_now = time.time()
                while(time.time()-inner_now <= inner_timeout):
                    pass
                timeout_count += 1
            modifiedMessage, serverAddress = clientSocket.recvfrom(2048)
            
        if(modifiedMessage.decode() == 'PING'):
            succeed_count += 1
        

        print("The current time is: {} and this is message number: {}".format(now, (i+1)))
        print("Uppercase Message from the Server: {}".format(modifiedMessage))
        rtt_time = time.time() - now
        rtt_list.append(rtt_time)
        print("The Round Trip Time is: {}".format(rtt_time))

    print("the program is done")
    print("Stored RTTs are: ", rtt_list)
    print("Max RTT is: {}".format(max(rtt_list)))
    print("Min RTT is: {}".format(min(rtt_list)))
    print("Sum of all RTTs is: {}".format(sum(rtt_list)))
    print("Average Round Trip Time is: {}".format(statistics.mean(rtt_list)))

    lost_count = 10 - succeed_count
    print("Total number of packet lost is: ",lost_count)
    clientSocket.close()

def main():
    client_send()

if __name__=="__main__":
    main()