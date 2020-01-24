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


#open() css and html?
class MyWebServer(socketserver.BaseRequestHandler):

    # generates body of reeponse if needed    
    def body_generator(self,body_string):
        length = str(len(body_string))
        body = "<html><body>" + str(body_string)  + "</body/></html>"
        return length, body


    #generates error code, content_type and contents length
    def response_generator(self,code, ftype, path):
        header = "HTTP/1.1 "
        content_length = "Content-length: "
        content_type = "Content-type: "
        
        # getting file type
        if ftype == "css":
            file_type = "text/css"
        else:
            file_type = "text/html"

        # generating http response
        if code == 200:
            length = str(len(open(path).read()))
            response = header + "200 OK\r\n" + content_type + file_type + "\r\n" + content_length + length  +"\r\n" + "Connection: close\r\n\r\n" + open(path).read() 
        
        elif code == 404:
            length, body = self.body_generator("Page Not Found")
            response = header + "404 Not Found\r\n"  + content_type + file_type + "\r\n"  + "Conntection: close\r\n\r\n"+  body
        
        elif code == 405:
            length, body = self.body_generator("Method is not allowed")
            response = header + "405 Method Not Allowed\r\n" + content_type + file_type + "\r\n" + content_length + length + "\r\n" + "Conntection: close\r\n\r\n" +  body 
        
        elif code == 301:
            length, body = self.body_generator("directory was missing '/'")
            response = header + "301 Moved Permanently\r\n" + content_type + file_type + "\r\n" + content_length + length + "\r\n"  + "Conntection: close\r\n\r\n" + open(path+ "/index.html").read()
        
        return response
    

    def handle(self):
        self.data = self.request.recv(1024).strip()
        
        print ("_________________________________________________________________\nGot a request of: %s\n" % self.data)
        
        # decode bytes
        self.data = self.data.decode()       

        # setting abs path
        path = os.path.abspath("www")
        print("\n" + self.data + "\n")
        try: 
            # getting method and file
            method = self.data.split()[0]
            file_name = self.data.split()[1]
            
            # if method is not GET
            if method != "GET":
                send = self.response_generator(405, "html", "")
                print("========================> sending: \n" + send)
                self.request.sendall(bytearray(send,'utf-8'))
                
            else:
                # chekcing for "/../"
                if not os.path.exists(path + os.path.realpath(file_name)):
                    send = self.response_generator(404, "html", path + os.path.realpath(file_name))
                    print("========================> sending: \n" + send)
                    self.request.sendall(bytearray(send,'utf-8'))
                
                else:

                    file_path = path + file_name

                    #if file or dir exists
                    if os.path.exists(file_path):

                        # if its a file
                        if os.path.isfile(file_path):
                            # getting type of file
                            if "." in file_name:
                                ftype = file_name.split(".")[1]
                            else:
                                ftype = "html"
        
                            send = self.response_generator(200, ftype, file_path)
                            print("========================> sending: \n" + send)
                            self.request.sendall(bytearray(send,'utf-8'))

                        # if it is a dir and ends with "/"
                        elif os.path.isdir(file_path) and file_path[-1] == '/':
                            send = self.response_generator(200, "html", file_path + "index.html")
                            print("========================> sending: \n" + send)
                            self.request.sendall(bytearray(send,'utf-8'))
                    
                        # if it is a dir but and is missing "/"
                        elif os.path.isdir(file_path) and file_path[-1] != '/':
                            send = self.response_generator(301, "html", path)            
                            print("========================> sending: \n" + send)
                            self.request.sendall(bytearray(send,'utf-8'))
                
                    # file does not exist
                    else:
                        send = self.response_generator(404, "html", file_path)
                        print("========================> sending: \n" + send)
                        self.request.sendall(bytearray(send,'utf-8'))
            
        except:
            print("Empty Request")    
if __name__ == "__main__":
    HOST, PORT = "localhost", 8080

    socketserver.TCPServer.allow_reuse_address = True
    # Create the server, binding to localhost on port 8080
    server = socketserver.TCPServer((HOST, PORT), MyWebServer)

    # Activate the server; this will keep running until you
    # interrupt the program with Ctrl-C
    server.serve_forever()
