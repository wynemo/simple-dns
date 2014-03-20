#!/usr/bin/env python
#coding:utf-8

import socket
import select
import SocketServer
import logging
import ssl

class Encoder(SocketServer.DatagramRequestHandler):
    
    def handle(self):
        data, sock = self.request
        # socket.sendto(data, self.client_address)
        remote = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        ssl_socket = ssl.wrap_socket(remote, ssl_version=ssl.PROTOCOL_TLSv1)
        l = ('198.58.115.107', 63235)
        ssl_socket.connect(l)
        ssl_socket.send(data)

        r, w, e = select.select([ssl_socket], [], [])
        try:
            if ssl_socket in r:
                data = ssl_socket.recv(64*1024)
                if data:
                    sock.sendto(data, self.client_address)
        except socket.sslerror as e:
            if e.args[0] != socket.SSL_ERROR_EOF:
                raise

        ssl_socket.close()
                        

def main():
    level = logging.INFO
    logging.basicConfig(format='%(asctime)s [%(levelname)s] %(message)s',
        datefmt='%m/%d/%Y %I:%M:%S %p',
        level=level)
    server = SocketServer.ThreadingUDPServer(('127.0.0.1', 53), Encoder)
    server.serve_forever()
    
if __name__ == '__main__':
    main()
