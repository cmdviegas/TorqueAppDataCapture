# ██████╗  ██████╗ █████╗   DEPTO DE ENGENHARIA DE
# ██╔══██╗██╔════╝██╔══██╗  COMPUTACAO E AUTOMACAO
# ██║  ██║██║     ███████║  UFRN, NATAL-RN, BRASIL
# ██║  ██║██║     ██╔══██║   
# ██████╔╝╚██████╗██║  ██║  PROF CARLOS M D VIEGAS
# ╚═════╝  ╚═════╝╚═╝  ╚═╝  viegas '@' dca.ufrn.br
#
# SCRIPT TO READ DATA FROM TORQUE/OBD2
#

from datetime import datetime
from http.server import BaseHTTPRequestHandler, HTTPServer
import urllib.parse
import sys
import json
import socket

class TorqueApp(BaseHTTPRequestHandler):

    counter = 0

    def timeStamp(self):
        return datetime.now().strftime("%d/%m/%Y %H:%M:%S")

    def do_GET(self):
        # Parse out the GET URL parameters
        params = urllib.parse.parse_qs(urllib.parse.urlparse(self.path).query)
        TorqueApp.counter += 1

        print(
            self.timeStamp(), 
            f'Message {TorqueApp.counter} from {self.client_address}'
            )

        for key,value in params.items():
            if key == 'eml' or key == 'time' or key == 'session' or key == 'v' or key == 'id':
                # ignore email address and other already used fields
                continue
            elif value[0] == 'NaN':
                # Skip invalid data. This is likely a divide by zero error.
                continue
            elif value[0] == 'Infinity' or value[0] == '-Infinity':
                # Skip invalid data. This is likely a divide by zero error.
                continue
            else:
                #print(self.getJsonByKey(key))
                print('\t > %s = %s' % (self.getJsonByKey(key), value[0])) # print data based on torqueCodes.json

        self.send_response_only(200)
        self.end_headers()
        self.wfile.write(bytes('OK!', 'UTF-8'))

    def getJsonByKey(self, key):
        with open('torqueCodes.json') as json_file:
            torqueCodes = json.load(json_file)
            for code in torqueCodes:
                if code['id'] == key:
                    return code['description']

if __name__ == '__main__':
    serverPort = 5000 # port
    serverHost = '' # host
    httpd = HTTPServer((serverHost, serverPort), TorqueApp)
    host, port = httpd.socket.getsockname()[:2]
    print(
        TorqueApp.timeStamp(0), 
        f'Server starts - {host}:{port}'
        )
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        httpd.server_close()
        print(
            TorqueApp.timeStamp(0), 
            f'Server stops - {host}:{port}'
            )
        sys.exit(0)