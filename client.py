#!/usr/bin/env python
#coding:utf-8

import socket
import SocketServer
import ssl
import threading
import random
import json
import errno

ssl_sockets = []
CONNECTION_NUM = 5
CONFIG_FILE = 'config.json'
server_ip = None
server_port = None


class Encoder(SocketServer.DatagramRequestHandler):
    
    def handle(self):
        global ssl_sockets
        global server_ip
        global server_port
        random.seed()
        i = random.randint(0, CONNECTION_NUM - 1)
        ssl_socket, lock = ssl_sockets[i]
        data, sock = self.request
        with lock:
            try:
                ssl_socket.sendall(data)
                data = ssl_socket.recv(64*1024)
            except socket.error as error:
                if error.errno == errno.WSAECONNRESET:
                    remote = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                    ssl_socket = ssl.wrap_socket(remote, ssl_version=ssl.PROTOCOL_TLSv1)
                    l = (server_ip, server_port)
                    ssl_socket.connect(l)
                    ssl_sockets[i] = ssl_socket, threading.RLock(),
                else:
                    raise
        sock.sendto(data, self.client_address)


def main():
    global ssl_sockets
    global server_ip
    global server_port

    with open(CONFIG_FILE, 'rb') as f:
        o = json.load(f)
        f.close()
        server_ip = o['client']['server-ip']
        server_port = o['server']['listen-port']
        listen_ip = o['client']['listen-ip']
        listen_port = o['client']['listen-port']
        
        for i in xrange(0, CONNECTION_NUM):
            remote = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            ssl_socket = ssl.wrap_socket(remote, ssl_version=ssl.PROTOCOL_TLSv1)
            l = (server_ip, server_port)
            ssl_socket.connect(l)
            ssl_sockets.append((ssl_socket, threading.RLock()))

        server = SocketServer.ThreadingUDPServer((listen_ip, listen_port), Encoder)
        server.serve_forever()

if __name__ == '__main__':
    main()
