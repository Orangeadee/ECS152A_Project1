from pydoc import cli
from socket import *
from html.parser import HTMLParser
from bs4 import BeautifulSoup
from PIL import Image
import PIL
import time
import statistics
import requests

# class MyParse(HTMLParser):
#     def handle_starttag(self, tag, attrs):
#         if tag=="img":
#             print(dict(attrs)["src"])

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
            if(response == b''):
                PLT = time.time() - now
                break

        # load data
        path = './ecs152a.html'
        data_file = open(path, 'w')
        data_file.write(data)

        data_file.close()
        clientSocket.close()

        page = open("./ecs152a.html").read()
        print("================")
        parsed_img_data = BeautifulSoup(img_data, 'html.parser')
        images = parsed_img_data.find_all('img', src=True)

        print('Number of Images: ', len(images))
        image_src = [x['src'] for x in images]
        image_src = [x for x in image_src if x.endswith('.jpg')]
        #print('Number of Images: ', len(image_src))
        link_img = image_src[0:3]
        image_src = image_src[3:]
        print('Number of Images: ', len(image_src))
        #image_count = 1


        # ==================== Link Image ===================== #

        number = 0
        for img in link_img:
            number += 1
            print(img)
            path = './images/img{}.png'.format(number)
            clientSocket = socket(AF_INET, SOCK_STREAM)
            clientSocket.connect((serverName, serverPort))
            now = time.time()
            r = requests.get(img,stream = True)
            avg_Rd.append(time.time()-now)
            clientSocket.close()
            if r.status_code == 200:
                with open(path,'wb') as f:
                    for chunk in r:
                        f.write(chunk)


        print("================")
        # ==================== Save Image ===================== #
        # clientSocket = socket(AF_INET, SOCK_STREAM)
        # clientSocket.connect((serverName, serverPort))
        number = 4

        
        for image in image_src:
            # try:
            #     clientSocket.setblocking(False)
            # except:
            #     print('non-block error:', Exception)
            clientSocket = socket(AF_INET, SOCK_STREAM)
            clientSocket.connect((serverName, serverPort))
            get_request = "GET /{} HTTP/1.1\r\nX-Client-project:project-152A-part2\r\n\r\n".format(image)
            now = time.time()
            clientSocket.sendall(get_request.encode())
            savedImageData = b''
            while (True):
                res = clientSocket.recv(4096)
                avg_Rd.append(time.time() - now)
                now = time.time()
                savedImageData += res
                if(not res):
                    break
            # print(savedImageData)
            
            headers =  savedImageData.split(b'\r\n\r\n')[0]
            saved_image = savedImageData[len(headers)+4:]
            img_path = './images/img{}.png'.format(number)
            # print(number)
            # print(saved_image)
            number += 1
            # print(saved_image)
            f = open(img_path, 'wb')
            f.write(saved_image)
            f.close()
            # if (number == 3):
            #     break
            clientSocket.close()

        # ==================== Compute Result ===================== #
        print("******************************************************")
        print("HTTP Client Version: Non-persistent HTTP")
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