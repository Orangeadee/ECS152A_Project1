from audioop import avg
from socket import *
from html.parser import HTMLParser
from bs4 import BeautifulSoup
from PIL import Image
import statistics
import time
import PIL
import re
import requests


def request_server():
    # Given server Name and Port Number.
    serverName = '173.230.149.18'
    serverPort = 23662
    # Data is for storing the entire html from get request and write to local html file.
    data = ''
    try:
        # ==================== GET HTML File ===================== #
        # Start connecting the socket to the server.
        clientSocket = socket(AF_INET, SOCK_STREAM)
        clientSocket.connect((serverName, serverPort))

        get_request = "GET /ecs152a.html HTTP/1.1\r\nX-Client-project:project-152A-part2\r\n\r\n"
        # Start counting the time when sending the get request to server.
        now = time.time()
        clientSocket.sendall(get_request.encode())

        # - img_data is to store all image data for further usage.
        # - PLT represents the page load time.
        # - ATF represents above the fold page load time.
        # - avg_Rd = average request delay.
        img_data = b''
        PLT = 0
        ATF = 0
        avg_Rd = []
        # Continuously receiving from server until reach the end.
        while(True):
            # Receive message with buffer size of 4096.
            response = clientSocket.recv(4096)
            # time.time() - now = time it takes to receive one message.
            avg_Rd.append(time.time() - now)
            # Temporary store all response in img_data and parse later.
            img_data += response
            data += str(response, "utf-8")
            # The initial page stops at the list named 'Pantry'.
            # So above the fold should stop there since it's the first page load.
            if b'Pantry' in response:
                ATF = time.time() - now
            # If response is empty, then we reach the end and will exit the loop.
            if response == b'':
                PLT = time.time() - now
                break

        # ================= Loading Data To Local File ================== #
        path = './ecs152a_HuilinZhang_917071562_TingweiLiu_917707784.html'
        data_file = open(path, 'w')
        data_file.write(data)
        data_file.close()
        clientSocket.close()

        # ==================== Parse HTML File ===================== #
        # Use BeautifulSoup to parse image data.
        # The variable 'img_data' that stored all the html data earlier
        # will be used here.
        parsed_img_data = BeautifulSoup(img_data, 'html.parser')
        images = parsed_img_data.find_all('img', src=True)
        image_src = [x['src'] for x in images]
        image_src = [x for x in image_src if x.endswith('.jpg')]

        # Link_img will store the first 3 images that are links.
        # Then remove the first 3 images in image_src.
        link_img = image_src[0:3]
        image_src = image_src[3:]

        # ==================== Link Image ===================== #
        number = 0
        # Downloading the first 3 pictures first by using request.
        for img in link_img:
            # Increment number by 1 once an image is looped.
            number += 1
            # Path is the location for us to download the images.
            path = './images/img{}.png'.format(number)
            now = time.time()
            # Getting request and response from links.
            response = requests.get(img,stream = True)
            # Record the time by subtracting previous recorded time from current time.
            avg_Rd.append(time.time()-now)

            # If the server response with code 200, means request succeed.
            # Then write the image to desired image file.
            if response.status_code == 200:
                with open(path,'wb') as f:
                    for chunk in response:
                        f.write(chunk)

        # ==================== Save Image ===================== #
        # Number is 4 because we already downloaded 3 images above.
        number = 4
        # Connect to the socket before getting the rest of the images in image_src.
        clientSocket = socket(AF_INET, SOCK_STREAM)
        clientSocket.connect((serverName, serverPort))
        for image in image_src:
            get_request = "GET /{} HTTP/1.1\r\nX-Client-project:project-152A-part2\r\nConnection:keep-alive\r\n\r\n".format(image)
            # Counting the request delay, which is time after send - time before send.
            now = time.time()
            clientSocket.sendall(get_request.encode())
            res = clientSocket.recv(4096)
            avg_Rd.append(time.time() - now)

            le=re.search("Content-length: (.*?)\r", res.decode('utf-8', 'ignore'))
            le = int(le.group(1))
            headers =  res.split(b'\r\n\r\n')[0]
            hdrlength = len(headers) + 4
            savedImageData = b''
            savedImageData += res
            filelength=le + hdrlength

            # Getting the full image.
            while (len(savedImageData) < filelength):
                # Calculating the request delay.
                # Reset the variable now for next calculation.
                now = time.time()
                res = clientSocket.recv(4096)
                avg_Rd.append(time.time() - now)
                savedImageData += res
            
            headers =  savedImageData.split(b'\r\n\r\n')[0]
            saved_image = savedImageData[len(headers)+4:]
            img_path = './images/img{}.png'.format(number)
            # Increment number by 1 for the next image path.
            number += 1
            f = open(img_path, 'wb')
            f.write(saved_image)
            f.close()
        # Close the socket when done.
        clientSocket.close()
        
        # ==================== Compute Result ===================== #
        print("******************************************************")
        print("HTTP Client Version: Persistent HTTP")
        print("Total PLT = ", PLT)
        print("Average Request Delay = ", statistics.mean(avg_Rd))
        print("ATF PLT = ", ATF)
        # Requests Per Second = Total requests / Total time spend.
        # Total request = 339 because 338 for images and 1 for the html file.
        RPS = 339 / sum(avg_Rd)
        print("RPS = ", RPS)
        print("******************************************************")


    except Exception as ex:
        print("Error: ",ex)


def main():
    request_server()

if __name__=="__main__":
    main()