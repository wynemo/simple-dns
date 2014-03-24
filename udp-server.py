#!/usr/bin/env python
#coding:utf-8

import ssl
import socket
import SocketServer
import json

DNS_SERVER = ""
DNS_PORT = 53
CONFIG_FILE = 'config.json'


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
        global DNS_SERVER
        while 1:
            data = sock.recv(64*1024)
            if data:
                remote.sendto(data, (DNS_SERVER, DNS_PORT))
                new_data, addr = remote.recvfrom(64*1024)
                sock.send(new_data)
            else:
                break

    def handle(self):
        remote = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.handle_tcp(self.connection, remote)


def main():
    global DNS_SERVER
    with open(CONFIG_FILE, 'rb') as f:
        o = json.load(f)
        f.close()
        DNS_SERVER = o['server']['real-dns-server']
        listen_port = o['server']['listen-port']
        server = SSlSocketServer(('0.0.0.0', listen_port), Decoder)
        server.serve_forever()

if __name__ == '__main__':
    main()
