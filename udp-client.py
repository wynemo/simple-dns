#!/usr/bin/env python
#coding:utf-8

import socket
import SocketServer
import logging
import ssl
import threading
import random

ssl_sockets = []
CONNECTION_NUM = 5


class Encoder(SocketServer.DatagramRequestHandler):
    
    def handle(self):
        global ssl_sockets
        random.seed()
        i = random.randint(0, CONNECTION_NUM)
        ssl_socket, lock = ssl_sockets[i]
        data, sock = self.request
        with lock:
            ssl_socket.send(data)
            data = ssl_socket.recv(64*1024)
        sock.sendto(data, self.client_address)


def main():
    global ssl_sockets
    level = logging.INFO
    logging.basicConfig(
        format='%(asctime)s [%(levelname)s] %(message)s',
        datefmt='%m/%d/%Y %I:%M:%S %p',
        level=level)

    for i in xrange(0, CONNECTION_NUM + 1):
        remote = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        ssl_socket = ssl.wrap_socket(remote, ssl_version=ssl.PROTOCOL_TLSv1)
        l = ('198.58.115.107', 63235)
        ssl_socket.connect(l)
        ssl_sockets.append((ssl_socket, threading.RLock()))

    server = SocketServer.ThreadingUDPServer(('0.0.0.0', 53), Encoder)
    server.serve_forever()

if __name__ == '__main__':
    main()
