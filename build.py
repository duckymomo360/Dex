import os
import sys
from http.server import BaseHTTPRequestHandler, HTTPServer

def readfile(path):
    file = open(path,"r")
    str = file.read()
    file.close()
    return str

def build():
    global embedStr
    embedStr = "local EmbeddedModules = {\n"
    files = os.listdir("modules")

    def addModuleFile(path):
        global embedStr

        moduleName = os.path.splitext(os.path.basename(path))[0]
        moduleSource = readfile(path)

        embedStr = embedStr + '["' + moduleName + '"] = function()\n' + moduleSource + '\nend,\n'

    for filename in files:
        addModuleFile("modules/" + filename)

    embedStr = embedStr + "}"
    embedStr = embedStr + "\n" + readfile("main.lua")

    return embedStr

if len(sys.argv) > 1 and sys.argv[1] == "server":
    class BuildServer(BaseHTTPRequestHandler):
        def do_GET(self):
            self.send_response(200)
            message = bytes(build(), "utf8")
            
            self.send_header("Content-type", "text/plain; charset=utf-8")
            self.send_header("Content-length", str(len(message)))
            self.end_headers()

            self.wfile.write(message)
    
    server = HTTPServer(("127.0.0.1", 8081), BuildServer)
    server.serve_forever()
else:
    file = open("out.lua","w")
    file.write(build())
    file.close()