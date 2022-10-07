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
import csv
import netifaces as ni

# get ip address
for intf in ni.interfaces():
    if intf == 'lo':
        continue
    else:
        serverIPaddr = ni.ifaddresses(intf)[ni.AF_INET][0]['addr'] # get server IP address
        break

# socker creation
serverPort = 5000 # port
serverSocket = socket(AF_INET,SOCK_STREAM) # create socket
serverSocket.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1) # reuse address
serverSocket.bind(('',serverPort)) # bind socket to port
serverSocket.listen(1) # listen for connections

def getCode(key): # get code from key
    with open('codes.csv', 'r') as inputFile:
        csv_file = csv.reader(inputFile)
        for row in csv_file:
            if row[0] == key:
                return row[1]

print ('> servidor iniciado %s:%d ...' % (serverIPaddr,serverPort))
lineCounter = 1
try:
  while 1:
    dateTime = datetime.now().strftime("%d/%m/%Y %H:%M:%S") # get current date and time
    clientSocket, clientAddr = serverSocket.accept() # wait for client connection
    inputData = clientSocket.recv(1024).decode('utf-8')  # read data from client
    outputData = inputData.split("&") # split data into a list
    lenoutputData = len(outputData) # get number of elements in the list
    outputData[lenoutputData-1] = outputData[lenoutputData-1].split(' ')[0] # remove the HTTP/1.0 from the last element
    print ('%d [%s] > %s:%d' % (lineCounter, dateTime, clientAddr[0], clientAddr[1])) # print date, client IP and port
    print('\t\t\t > %s' % outputData) # print data based on codes.csv
    #for row in outputData[1:]: # print data
    #    rowParts = row.split('=') # split data into a list
    #    #if rowParts[0] == 'time':
    #    #  rowParts[1] = str(datetime.fromtimestamp(166518417990))
    #    print('\t\t\t > %s = %s' % (getCode(rowParts[0]), rowParts[1])) # print data based on codes.csv
    response = "HTTP/1.0 200 OK\r\n\r\n" # HTTP response
    #clientSocket.send(response.encode('utf-8')) # send HTTP response
    lineCounter = lineCounter + 1 # increment line counter
    clientSocket.close() # close client connection
except KeyboardInterrupt:
  print("Caught keyboard interrupt, exiting") # print message when user press CTRL+C
finally:
  serverSocket.close() # close server socket

  datetime.fromtimestamp(1485714600).strftime("%A, %B %d, %Y %I:%M:%S")