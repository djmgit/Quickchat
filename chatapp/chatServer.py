
import socket
import time
host2='127.0.0.1'
host = '172.16.135.83'
port = 5000



clients = []

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
# provide port......default is 80....leaving the ip '' allows the server to response to other computers as well
s.bind(('',80))
s.setblocking(0)


quitting = False
print "Server Started."
while not quitting:
    try:
        data, addr = s.recvfrom(1024)
        if "Quit" in str(data):
            quitting = True
        if addr not in clients:
            clients.append(addr)
            
        print time.ctime(time.time()) + str(addr) + ": :" + str(data)
        for client in clients:
            s.sendto(data, client)
    except:
        pass
s.close()



