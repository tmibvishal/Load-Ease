import xmlrpc.client

with xmlrpc.client.ServerProxy("http://localhost:8000/") as proxy:
    print(f"{proxy.available()}")
    print(f"{proxy.available()}")
    d = proxy.available()
    print(type(d))
    print(d['available'])