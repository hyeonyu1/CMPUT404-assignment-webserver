    #  coding: utf-8 
import socketserver
import os

# Copyright 2013 Abram Hindle, Eddie Antonio Santos
# 
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
# 
#     http://www.apache.org/licenses/LICENSE-2.0
# 
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
#
# Furthermore it is derived from the Python documentation examples thus
# some of the code is Copyright © 2001-2013 Python Software
# Foundation; All Rights Reserved
#
# http://docs.python.org/2/library/socketserver.html
#
# run: python freetests.py

# try: curl -v -X GET http://127.0.0.1:8080/

# US
#As a user I want to view files in ./www via a webbrowser
#As a user I want to view files in ./www via curl
#As a webserver admin I want to serve HTML and CSS files from ./www
#As a webserver admin I want ONLY files in ./www and deeper to be served.


#Req
#[X] The webserver can serve files from ./www
#[X] The webserver can be run using the runner.sh file
#[?] The webserver can pass all the tests in freetests.py
#[?] The webserver can pass all the tests in not-free-tests.py (you only have part of this one, I reserve the right to add tests)
#[X] The webserver supports mime-types for HTML
#[X] The webserver supports mime-types for CSS
#[?] The webserver can return index.html from directories (paths that end in /)
#[X] The webserver can server 404 errors for paths not found
#[ ] The webserver works with Firefox and Chromium http://127.0.0.1:8080/
#[?] The webserver can serve CSS properly so that the front page has an orange h1 header.
#[ ] I can check out the source code via an HTTP git URL
#[ ] Provide 1 screenshot (commit and push it!) of Firefox at http://127.0.0.1:8080/ as ./root.png in the root of the repo
#[ ] Provide 1 screenshot (commit and push it!) of Firefox at http://127.0.0.1:8080/deep/ as ./deep.png in the root of the repo
#[X] Return a status code of “405 Method Not Allowed” for any method you cannot handle (POST/PUT/DELETE)
#[?] Must use 301 to correct paths such as http://127.0.0.1:8080/deep to http://127.0.0.1:8080/deep/ (path ending)


# Content-length
# Content-type 


#open() css and html?
class MyWebServer(socketserver.BaseRequestHandler):

    # generates body of reeponse if needed    
    def body_generator(self,body_string):
        length = str(len(body_string))
        body = "<html><body>" + str(body_string) + "</body/></html>"

        return length, body

    def redirection(self,file_path):
        length, body = self.body_generator("correct path = " + file_path + "/")
        return "Location: " + file_path + "/\r\n", length, body

    #generates error code, content_type and contents length
    def response_generator(self,code, ftype, path):
        header = "HTTP/1.1 "
        content_length = "Content-length: "
        content_type = "Content-type: "
        
        if ftype == "css":
            file_type = "text/css"
        else:
            file_type = "text/html"

        if code == 200:
            length = str(len(open(path).read()))
            response = header + "200 OK\r\n" + content_type + file_type + "\r\n" + content_length + length  +"\r\n" + "Connection: close\r\n\r\n" + open(path).read() 
        elif code == 404:
            length, body = self.body_generator("path: " + path + "not found")
            response = header + "404 Not Found\r\n" + content_type + file_type + "\r\n" + content_length + length + "\r\n"+ body + "\r\n" + "Conntection: close\r\n\r\n"
        elif code == 405:
            length, body = self.body_generator("Method is not allowed")
            response = header + "405 Method Not Allowed\r\n" + content_type + file_type + "\r\n" + content_length + length + "\r\n" + body + "\r\n"  + "Conntection: close\r\n\r\n"
        # open and read the changed path?
        elif code == 301:
            location, length, body = self.redirection(path)
            response = header + "301 Moved Permanently\r\n" + content_type + file_type + "\r\n" + content_length + length + "\r\n"  + location +"Conntection: close\r\n\r\n" + open(path+ "/index.html").read()
        
        return response
    
    def handle(self):
        self.data = self.request.recv(1024).strip()
        
        print ("Got a request of: %s\n" % self.data)
        #Got a request of: b'GET /base.css HTTP/1.1\r\nAccept-Encoding:identity\r\nHost: 127.0.0.1:8080\r\nUser-Agent: Python-urllib/3.6\r\nConnection: close'
       
        #decode bytes
        self.data = self.data.decode()       
        # The webserver can serve files from ./www
        path = os.path.abspath("www")
        #print("path", path)
        
        
    #     get method and file name in www
        # if len(self.data) > 0:
        #     method = self.data.split()[0]
        #     file_name = self.data.split()[1]
        #     print("string_split", file_name + "\n" + method)
        # else:
        #     print("data is empty")


        #Got a request of: b'GET /../../../../../../../../../../../../etc/group HTTP/1.1\r\n
        # Accept-Encoding: identity\r\nHost: 127.0.0.1:8080\r\n
        # User-Agent: Python-urllib/3.7\r\nConnection: close'
        
        #Got a request of: b'GET /base.css HTTP/1.1\r\n
        # Accept-Encoding:identity\r\n
        # Host: 127.0.0.1:8080\r\n
        # User-Agent: Python-urllib/3.6\r\nConnection: close'
        # need = self.data.split("\r\n")[0]
        method = self.data.split()[0]
        file_name = self.data.split()[1]
        print("string_split", file_name + "\n" + method)
        
        if method != "GET":
            print("Method not supported")
            send = self.response_generator(405, "html", "")
            print("send: ", send)
            self.request.sendall(bytearray(send,'utf-8'))
            
        else:
            print("possible method\n")        
            file_path = path + file_name
            print("file_path", file_path)
           
            if os.path.exists(file_path):
                print("file exists")
                if os.path.isfile(file_path):
                    print("opening file")
                    if "." in file_name:
                        ftype = file_name.split(".")[1]
                    else:
                        ftype = "html"
  
                    send = self.response_generator(200, ftype, file_path)
                    self.request.sendall(bytearray(send,'utf-8'))

                elif os.path.isdir(file_path) and file_path[-1] == '/':
                    print("opening html in directory")
                    send = self.response_generator(200, "html", file_path + "index.html")
                    self.request.sendall(bytearray(send,'utf-8'))
                
                elif os.path.isdir(file_path) and file_path[-1] != '/':
                    print("relocating and opening dir")
                    send = self.response_generator(301, "html", path)
                    # send = "HTTP/1.1 " + "301 Moved Permanently\r\n" + "Content-Type: text/html" + "\r\n"   + "Conntection: close\r\n\r\n" + open(path+"/index.html").read()
        
                    print("sending: " + send)
                    self.request.sendall(bytearray(send,'utf-8'))
            
            else:
                send = self.response_generator(404, "html", file_path)
                self.request.sendall(bytearray(send,'utf-8'))
        
        
if __name__ == "__main__":
    HOST, PORT = "localhost", 8080

    socketserver.TCPServer.allow_reuse_address = True
    # Create the server, binding to localhost on port 8080
    server = socketserver.TCPServer((HOST, PORT), MyWebServer)

    # Activate the server; this will keep running until you
    # interrupt the program with Ctrl-C
    server.serve_forever()
