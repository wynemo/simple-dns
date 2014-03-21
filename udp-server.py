#!/usr/bin/env python
#coding:utf-8

import ssl
import socket
import SocketServer

UDP_IP = "127.0.0.1"
UDP_PORT = 53


class SSlSocketServer(SocketServer.ThreadingTCPServer):
    def get_request(self):
        new_socket, from_addr = self.socket.accept()
        conn_stream = ssl.wrap_socket(
            new_socket,
            server_side=True,
            certfile="cacert.pem",
            keyfile="privkey.pem",
            ssl_version=ssl.PROTOCOL_TLSv1)
        return conn_stream, from_addr


class Decoder(SocketServer.StreamRequestHandler):
    @staticmethod
    def handle_tcp(sock, remote):
        while 1:
            data = sock.recv(64*1024)
            if data:
                remote.sendto(data, (UDP_IP, UDP_PORT))
                new_data, addr = remote.recvfrom(64*1024)
                sock.send(new_data)
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
