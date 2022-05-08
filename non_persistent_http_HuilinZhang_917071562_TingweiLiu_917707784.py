from socket import *
from html.parser import HTMLParser
from bs4 import BeautifulSoup
from PIL import Image
import PIL

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
        clientSocket.sendall(get_request.encode())
        img_data = b''
        while(True):
            response = clientSocket.recv(4096)
            img_data += response
            data += str(response, "utf-8")
            if(response == b''):
                break

        # load data
        path = './ecs152a.html'
        data_file = open(path, 'w')
        data_file.write(data)

        data_file.close()
        # clientSocket.close()

        page = open("./ecs152a.html").read()
        print("================")
        parsed_img_data = BeautifulSoup(img_data, 'html.parser')
        images = parsed_img_data.find_all('img', src=True)

        print('Number of Images: ', len(images))
        image_src = [x['src'] for x in images]
        image_src = [x for x in image_src if x.endswith('.jpg')]
        image_src = image_src[3:]
        image_count = 1

        print("================")
        # ==================== Save Image ===================== #
        # clientSocket = socket(AF_INET, SOCK_STREAM)
        # clientSocket.connect((serverName, serverPort))
        number = 1
        clientSocket = socket(AF_INET, SOCK_STREAM)
        clientSocket.connect((serverName, serverPort))
        
        for image in image_src:
            # try:
            #     clientSocket.setblocking(False)
            # except:
            #     print('non-block error:', Exception)
            get_request = "GET /{} HTTP/1.1\r\nX-Client-project:project-152A-part2\r\n\r\n".format(image)
            clientSocket.sendall(get_request.encode())
            savedImageData = b''
            while (True):
                res = clientSocket.recv(4096)
                savedImageData += res
                if(not res):
                    break
            print(savedImageData)
            
            headers =  savedImageData.split(b'\r\n\r\n')[0]
            saved_image = savedImageData[len(headers)+4:]
            img_path = './images/img{}.png'.format(number)
            print(number)
            # print(saved_image)
            number += 1
            # print(saved_image)
            f = open(img_path, 'wb')
            f.write(saved_image)
            f.close()
            if (number == 3):
                break
        clientSocket.close()

    except Exception as ex:
        print("error: ",ex)


def main():
    request_server()

if __name__=="__main__":
    main()