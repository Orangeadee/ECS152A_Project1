from socket import *
import time
import math
import random
import statistics

def client_send():
    # Given server Name and Port Number.
    serverName = '173.230.149.18'
    serverPort = 12000
    # Set timeout seconds to 10s.
    timeout_seconds = 10.0
    # For storing Round Trip Times.
    rtt_list = []
    # Count for number of succeed packages.
    succeed_count = 0
    # Connect socket with udp protocal.
    clientSocket = socket(AF_INET, SOCK_DGRAM)
    message = 'ping'
        
    # Sending 10 messages in total.
    for i in range(0,10):
        # Start counting the time when sending message to the server.
        now = time.time()
        # Timeout_count is for further calculation of timeout_seconds.
        timeout_count = 0
        try:
            # Start sending message to server.
            clientSocket.sendto(message.encode(),(serverName, serverPort))
            # Receive message from server with max buffer size of 4096.
            modifiedMessage, serverAddress = clientSocket.recvfrom(4096)
            # If the decoded message is PING, then we successfully sending one message.
            if(modifiedMessage.decode() == 'PING'):
                succeed_count += 1
        # Throwing an exception meands the message didn't send successfully.
        except Exception as ex:
            # Succeed_count increments by 1 every time we receive PING, so if the message
            # failed to send, the count won't increment and will be the same as i.
            # This will be its first timeout.
            if (succeed_count == i):
                # Apply the formula of timeout_seconds if it's not the first time it timeout
                timeout_seconds = timeout_seconds * math.pow(2,timeout_count)+random.uniform(0,1)
            # Increment count for timeout by 1.
            timeout_count = timeout_count + 1

            # We need to limit the timeout seconds to less or equal to 10 minutes.
            # 10 min = 10 * 60 = 600 seconds.
            if (timeout_seconds >= 600):
                timeout_seconds = 600
            time.sleep(timeout_seconds)
            # After sleeping for timeout_seconds amout of time, continue to next iteration.
            continue
        # ========================= Print Result In Loop ========================= #
        print("The current time is: {} and this is message number: {}".format(now, (i+1)))
        print("Uppercase Message from the Server: {}".format(modifiedMessage))
        # Calculate the current round trip time and store it in the list.
        rtt_time = time.time() - now
        rtt_list.append(rtt_time)
        print("The Round Trip Time is: {}".format(rtt_time))

    # ========================= Print Final Result ========================= #
    print("the program is done")
    print("Stored RTTs are: ", rtt_list)
    print("Max RTT is: {}".format(max(rtt_list)))
    print("Min RTT is: {}".format(min(rtt_list)))
    print("Sum of all RTTs is: {}".format(sum(rtt_list)))
    print("Average Round Trip Time is: {}".format(statistics.mean(rtt_list)))
    # Counts for package lost.
    lost_count = 10 - succeed_count
    print("Total number of packet lost is: ",lost_count)
    clientSocket.close()

def main():
    client_send()

if __name__=="__main__":
    main()