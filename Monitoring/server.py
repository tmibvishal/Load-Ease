import psutil

from xmlrpc.server import SimpleXMLRPCServer

def available():
    mem = psutil.virtual_memory()
    d = {'available' : str(mem.available)}
    return d

server = SimpleXMLRPCServer(("localhost", 8000))
print("Listening on port 8000...")
server.register_function(available, "available")
server.serve_forever()