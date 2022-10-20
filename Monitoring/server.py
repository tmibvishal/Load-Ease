import psutil

from xmlrpc.server import SimpleXMLRPCServer

def available():
    mem = psutil.virtual_memory()
    d = {'available' : str(mem.available)}
    return d

# Main function of Monitoring Service
# This script will run in all hosts.
# And will set up RPC Calls / Other API for the Load balancer to use.
if __name__ == '__main__':
    server = SimpleXMLRPCServer(("localhost", 8000))
    print("Listening on port 8000...")
    server.register_function(available, "available")
    server.serve_forever()
    pass

