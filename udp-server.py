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
        fdset = [sock, remote]
        while True:
            r, w, e = select.select(fdset, [], [])
            try:
                if sock in r:
                    data = sock.recv(64*1024)
                    if not data:
                        break
                    else:
                        remote.sendto(data, (UDP_IP, UDP_PORT))
                if remote in r:
                    data, addr = remote.recvfrom(64*1024)
                    sock.send(data)
            except socket.sslerror, x:
                if x.args[0] == socket.SSL_ERROR_EOF:
                    break
                else:
                    raise

    def handle(self):
        remote = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.handle_tcp(self.connection, remote)

def main():
    server = SSlSocketServer(('0.0.0.0', 63235), Decoder)
    server.serve_forever()
if __name__ == '__main__':
    main()
 
