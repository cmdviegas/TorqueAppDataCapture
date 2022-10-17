# ██████╗  ██████╗ █████╗   DEPTO DE ENGENHARIA DE
# ██╔══██╗██╔════╝██╔══██╗  COMPUTACAO E AUTOMACAO
# ██║  ██║██║     ███████║  UFRN, NATAL-RN, BRASIL
# ██║  ██║██║     ██╔══██║   
# ██████╔╝╚██████╗██║  ██║  PROF CARLOS M D VIEGAS
# ╚═════╝  ╚═════╝╚═╝  ╚═╝  viegas '@' dca.ufrn.br
#
# SCRIPT TO READ DATA FROM TORQUE/OBD2
#

# libs
from socket import * 
from datetime import datetime
import json
from http.server import BaseHTTPRequestHandler, HTTPServer
import urllib
#import netifaces as ni
 
# get ip address
# for intf in ni.interfaces():
#     if intf == 'lo':
#         continue
#     else:
#         serverIPaddr = ni.ifaddresses(intf)[ni.AF_INET][0]['addr'] # get server IP address
#         break
serverIPaddr = 0

# socker creation
serverPort = 5000 # port
# serverSocket = socket(AF_INET,SOCK_STREAM) # create socket
# serverSocket.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1) # reuse address
# serverSocket.bind(('',serverPort)) # bind socket to port
# serverSocket.listen(1) # listen for connections

def getJsonByKey(key):
    with open('torqueCodes.json') as json_file:
        torqueCodes = json.load(json_file)
        for code in torqueCodes:
            if code['id'] == key:
                return code['description']

#print(getJsonByKey('kff1276'))

class MyHandler(BaseHTTPRequestHandler):

    def do_GET(self):
        # Parse out the GET URL parameters
        params = urllib.parse.parse_qs(urllib.parse.urlparse(self.path).query)
        print (params)

        exit()

# print ('> servidor iniciado %s:%d ...' % (serverIPaddr,serverPort))
# lineCounter = 1
# try:
#   while 1:
#     clientSocket, clientAddr = serverSocket.accept() # wait for client connection
#     inputData = clientSocket.recv(1024).decode('utf-8')  # read data from client
#     params = urllib.parse.parse_qs(urllib.parse.urlparse(inputData.path).query)
#     outputData = inputData.split("&") # split data into a list
#     lenoutputData = len(outputData) # get number of elements in the list
#     outputData[lenoutputData-1] = outputData[lenoutputData-1].split(' ')[0] # remove the HTTP/1.0 from the last element
#     dateTime = datetime.now().strftime("%d/%m/%Y %H:%M:%S") # get current date and time
#     print ('%d [%s] > %s:%d' % (lineCounter, dateTime, clientAddr[0], clientAddr[1])) # print date, client IP and port
#     #print('\t\t\t > %s' % outputData) # print data based on codes.csv
#     for row in outputData[1:]: # print data
#         rowParts = row.split('=') # split data into a list
#         #if rowParts[0] == 'time':
#         #  rowParts[1] = str(datetime.fromtimestamp(166518417990))
#         #print(rowParts[0])
#         print('\t\t\t > %s = %s' % (getJsonByKey(rowParts[0]), rowParts[1])) # print data based on torqueCodes.json
#     response = "HTTP/1.0 200 OK\r\n\r\n" # HTTP response
#     #clientSocket.send(response.encode('utf-8')) # send HTTP response
#     lineCounter = lineCounter + 1 # increment line counter
#     clientSocket.close() # close client connection
# except KeyboardInterrupt:
#   print("Caught keyboard interrupt, exiting") # print message when user press CTRL+C
# finally:
#   serverSocket.close() # close server socket

#   datetime.fromtimestamp(1485714600).strftime("%A, %B %d, %Y %I:%M:%S")

if __name__ == '__main__':
    server_class = HTTPServer
    httpd = server_class(('', serverPort), MyHandler)
    print(datetime.now().strftime("%d/%m/%Y %H:%M:%S"), 'Server Starts - %s:%s' % ('', serverPort))
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        pass
    httpd.server_close()
    print(datetime.now().strftime("%d/%m/%Y %H:%M:%S"), 'Server Stops - %s:%s' % ('', serverPort))
