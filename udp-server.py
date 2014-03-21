#!/usr/bin/env python
#coding:utf-8

import ssl
import socket
import SocketServer
import select

UDP_IP = "127.0.0.1"
UDP_PORT = 53

class SSlSocketServer(SocketServer.ThreadingMixIn, SocketServer.TCPServer):
    def get_request(self):#overwritten
        newsocket, fromaddr = self.socket.accept()
        connstream = ssl.wrap_socket(newsocket,
            server_side=True,
            certfile="cacert.pem",
            keyfile="privkey.pem",
            ssl_version=ssl.PROTOCOL_TLSv1)
        return connstream, fromaddr

class Decoder(SocketServer.StreamRequestHandler):
    def handle_tcp(self, sock, remote):
        while 1:
            data = sock.recv(64*1024)
            if data:
                remote.sendto(data[:-2], (UDP_IP, UDP_PORT))
                new_data, addr = remote.recvfrom(64*1024)
                sock.send(new_data + data[-2:])
            else:
                break

    def handle(self):
        remote = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.handle_tcp(self.connection, remote)

def main():
    server = SSlSocketServer(('0.0.0.0', 63235), Decoder)
    server.serve_forever()
if __name__ == '__main__':
    main()
 