#!/usr/bin/env python
#coding:utf-8

import socket
import select
import SocketServer
import logging
import ssl
import threading
import struct
import random

ssl_sockets = []

for i in xrange(0, 6):
    remote = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    ssl_socket = ssl.wrap_socket(remote, ssl_version=ssl.PROTOCOL_TLSv1)
    l = ('198.58.115.107', 63235)
    ssl_socket.connect(l)
    ssl_sockets.append((ssl_socket, threading.RLock()))
print 21, ',,,,,'
d = {}

def foo():
    global ssl_socket
    global d
    while True:
        r, w, e = select.select([ssl_socket], [], [])
        if ssl_socket in r:
            data = ssl_socket.recv(64*1024)
            print 27, len(data)
            port = struct.unpack('<H', data[-2:])[0]
            print 29, port
            sock = d[port]
            d.pop(port)
            sock.sendto(data[:-2], ('127.0.0.1', port))

class Encoder(SocketServer.DatagramRequestHandler):
    
    def handle(self):
        global ssl_sockets
        #global d
        print 43, self.client_address
        random.seed()
        i = random.randint(0, 5)
        ssl_socket, lock = ssl_sockets[i]
        
        data, sock = self.request
        
        port = self.client_address[1]
        #d[port] = sock
        
        with lock:
            ssl_socket.send(data + struct.pack('<H', port))
            data = ssl_socket.recv(64*1024)
            #port = struct.unpack('<H', data[-2:])[0]
        print 57, self.client_address, len(data)
        sock.sendto(data[:-2], (self.client_address[0], port))
            
def main():
    level = logging.INFO
    logging.basicConfig(format='%(asctime)s [%(levelname)s] %(message)s',
        datefmt='%m/%d/%Y %I:%M:%S %p',
        level=level)
    #t = threading.Thread(target=foo)
    #t.daemon = True
    #t.start()
    server = SocketServer.ThreadingUDPServer(('0.0.0.0', 53), Encoder)
    server.serve_forever()
    ssl_socket.close()
    
if __name__ == '__main__':
    main()
