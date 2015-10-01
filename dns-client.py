#!/usr/bin/env python
#coding:utf-8

import asyncore
import socket
import json
import sys

local_address = ('127.0.0.1', 53)
remote_address = ('8.8.8.8', 53)


class DnsClient(asyncore.dispatcher):
    def __init__(self,  server):
        asyncore.dispatcher.__init__(self)
        self.create_socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.info = []
        self.server = server
        self.d = {}

    def add_request(self, address, data):
        self.info.append((data, address))
        self.d[data[0:2]] = address

    def handle_read(self):
        data, _ = self.socket.recvfrom(64*1024)
        address = self.d[data[0:2]]
        self.server.datas.append((data, address,))

    def handle_write(self):
        for each in self.info:
            data, _ = each
            self.socket.sendto(data, remote_address)
        self.info = []

    def writable(self):
        return len(self.info) > 0


class DnsServer(asyncore.dispatcher):
    def __init__(self, address):
        asyncore.dispatcher.__init__(self)
        self.create_socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.set_reuse_addr()
        self.bind(address)
        self.datas = [] # address, data

    def set_client(self, client):
        self.client = client

    def handle_read(self):
        data, address = self.socket.recvfrom(64*1024)
        self.client.add_request(address, data)

    def writable(self):
        return len(self.datas) > 0

    def handle_write(self):
        for each in self.datas:
            data, address = each
            self.socket.sendto(data, address)
        self.datas = []


if len(sys.argv) < 2:
    print("please specify a configuration file")
    exit(0)
with open(sys.argv[1], 'rb') as f:
    o = json.load(f)
    f.close()
    local_address = o['local_ip'], o['local_port'],
    remote_address = o['remote_ip'], o['remote_port'],
    server = DnsServer(local_address)
    client = DnsClient(server)
    server.set_client(client)
    asyncore.loop()

