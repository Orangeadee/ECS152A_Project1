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
    serverName = '173.230.149.18'
    serverPort = 23662

    data = ''
    try:
        clientSocket = socket(AF_INET, SOCK_STREAM)
        clientSocket.connect((serverName, serverPort))

        get_request = "GET /ecs152a.html HTTP/1.1\r\nX-Client-project:project-152A-part2\r\n\r\n"
        now = time.time()
        clientSocket.sendall(get_request.encode())
        img_data = b''
        PLT = 0
        ATF = 0
        avg_Rd = []
        while(True):
            response = clientSocket.recv(4096)
            avg_Rd.append(time.time() - now)
            img_data += response
            data += str(response, "utf-8")
            if b'Pantry' in response:
                ATF = time.time() - now
                                
            if response == b'':
                PLT = time.time() - now
                break

        # load data
        path = './ecs152a.html'
        data_file = open(path, 'w')
        data_file.write(data)

        data_file.close()
        clientSocket.close()

        page = open("./ecs152a.html").read()
        # print("================")
        parsed_img_data = BeautifulSoup(img_data, 'html.parser')
        images = parsed_img_data.find_all('img', src=True)

        # print('Number of Images: ', len(images))
        image_src = [x['src'] for x in images]
        image_src = [x for x in image_src if x.endswith('.jpg')]
        #print('Number of Images: ', len(image_src))
        link_img = image_src[0:3]
        image_src = image_src[3:]
        # print('Number of Images: ', len(image_src))
        image_count = 1

        print("================")
        # ==================== Link Image ===================== #

        number = 0
        for img in link_img:
            number += 1
            print(img)
            path = './images/img{}.png'.format(number)
            now = time.time()
            r = requests.get(img,stream = True)
            avg_Rd.append(time.time()-now)
            if r.status_code == 200:
                with open(path,'wb') as f:
                    for chunk in r:
                        f.write(chunk)

        
        # ==================== Save Image ===================== #
        # clientSocket = socket(AF_INET, SOCK_STREAM)
        # clientSocket.connect((serverName, serverPort))
        number = 4
        clientSocket = socket(AF_INET, SOCK_STREAM)
        clientSocket.connect((serverName, serverPort))
      


        for image in image_src:
            # print(number)
            # try:
            #     clientSocket.setblocking(False)
            # except:
            #     print('non-block error:', Exception)

            #get_request = "GET /{} HTTP/1.1\r\nContent-length:10000\r\nConnection:keep-alive\r\nX-Client-project:project-152A-part2\r\n\r\n".format(image)
            get_request = "GET /{} HTTP/1.1\r\nX-Client-project:project-152A-part2\r\nConnection:keep-alive\r\n\r\n".format(image)
            now = time.time()
            clientSocket.sendall(get_request.encode())
            res = clientSocket.recv(4096)
            avg_Rd.append(time.time() - now)
            # print(res)
            le=re.search("Content-length: (.*?)\r", res.decode('utf-8', 'ignore'))
            #le=re.search("Content-length: (.*?)\r", res.decode()).group(1)
            le = int(le.group(1))
            # print("content length is")
            # print(le)
            headers =  res.split(b'\r\n\r\n')[0]
            hdrlength = len(headers) + 4
            savedImageData = b''
            savedImageData += res
            filelength=le + hdrlength
            #print(filelength)
            while (len(savedImageData) < filelength):
                now = time.time()
                res = clientSocket.recv(4096)
                avg_Rd.append(time.time() - now)

                #print(res)
                # le=re.search("Content-length: (.*?)\r", res.decode('utf-8', 'ignore'))
                # print(le)
                # if(le):
                #     filelength = int(le.group(1))
                savedImageData += res
                # if(len(savedImageData)>=filelength):
                #     break
            #print(savedImageData)
            
            headers =  savedImageData.split(b'\r\n\r\n')[0]
            saved_image = savedImageData[len(headers)+4:]
            img_path = './images/img{}.png'.format(number)
            #print(number)
            #print(saved_image)
            number += 1
            # print(saved_image)
            f = open(img_path, 'wb')
            f.write(saved_image)
            f.close()
            # if (number == 100):
            #     break
        clientSocket.close()
        
        # ==================== Compute Result ===================== #
        print("******************************************************")
        print("HTTP Client Version: Persistent HTTP")
        print("Total PLT = ", PLT)
        print("Average Request Delay = ", statistics.mean(avg_Rd))
        print("ATF PLT = ", ATF)
        RPS = 339/sum(avg_Rd)
        print("RPS = ", RPS)
        print("******************************************************")


    except Exception as ex:
        print("error: ",ex)


def main():
    request_server()

if __name__=="__main__":
    main()