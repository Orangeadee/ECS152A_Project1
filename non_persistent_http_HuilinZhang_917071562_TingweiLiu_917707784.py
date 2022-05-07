from socket import *
from html.parser import HTMLParser
from bs4 import BeautifulSoup
from PIL import Image
import PIL

class MyParse(HTMLParser):
    def handle_starttag(self, tag, attrs):
        if tag=="img":
            print(dict(attrs)["src"])


serverName = '173.230.149.18'
serverPort = 23662

data = ''
try:
    clientSocket = socket(AF_INET, SOCK_STREAM)
    # clientSocket = socket()
    clientSocket.connect((serverName, serverPort))

    get_request = "GET /ecs152a.html HTTP/1.1\r\nX-Client-project:project-152A-part2\r\n\r\n"
    clientSocket.sendall(get_request.encode())
    temp = b''
    while(True):
        response = clientSocket.recv(4096)
        temp = temp + response
        data += str(response, "utf-8")
        if(response == b''):
            break
    # print(data)

    # load data
    path = '/Users/huilinzhang/Desktop/ECS_152A/ecs152a.html'
    data_file = open(path, 'w')
    data_file.write(data)

    data_file.close()
    # clientSocket.close()

    image_parse = MyParse()
    page = open("/Users/huilinzhang/Desktop/ECS_152A/ecs152a.html").read()
    # new_data = image_parse.feed(page)
    print("================")
    neww_ata = BeautifulSoup(temp, 'html.parser')
    images = neww_ata.find_all('img', src=True)
    # for image in images:
    #     print(image)
    print('Number of Images: ', len(images))
    image_src = [x['src'] for x in images]
    image_src = [x for x in image_src if x.endswith('.jpg')]
    image_src = image_src[3:]
    image_count = 1

    # for image in image_src:
    #     with open('image_'+str(image_count)+'.jpg', 'wb') as f:
    #         get_request = "GET /{} HTTP/1.1\r\nX-Client-project:project-152A-part2\r\n\r\n".format(str(image))
    #         clientSocket.sendall(get_request.encode())
    #         res = clientSocket.recv(4096)
    #         f.write(res.content)
    #     image_count = image_count+1
        # print(image)
    print(image_src[0])
    clientSocket = socket(AF_INET, SOCK_STREAM)
    # clientSocket = socket()
    clientSocket.connect((serverName, serverPort))
    get_request = "GET /images/visuel_salle_reunion.jpg HTTP/1.1\r\nX-Client-project:project-152A-part2\r\n\r\n"
    clientSocket.sendall(get_request.encode())
    res = clientSocket.recv(4096)
    print(res.decode())
    # picture = Image.open(r'img1.jpg')
    # picture = picture.save(res)
    clientSocket.close()

except Exception as ex:
    print("error: ",ex)

