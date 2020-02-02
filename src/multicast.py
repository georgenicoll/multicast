#!/usr/bin/env python3
#Shamelessly cribbed from https://github.com/dumplab/python_multicast/
import sys
import socket
import struct
import multiprocessing
from time import sleep
import time

ADDRESS = "239.2.2.2"
PORT = 31001
TTL = 5
READ = 'read'
WRITE = 'write'
PAYLOAD = 'Multicast Hello'
ADDRESS_PORT = (ADDRESS, PORT)

def main(argv):
    print('Arguments: ', str(argv))

    if len(argv) < 2:
        print('Need a mode.  Expecting', READ, '|', WRITE)
        exit(1)

    mode = argv[1]
    if mode == READ:
        sockfunc=read
    elif mode == WRITE:
        sockfunc=write
    else:
        print('Unrecognised mode', mode, '. Expecting', READ, '|', WRITE)
        exit(1)

    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
    sockfunc(sock)

    print('Finished.')

def read(sock):
    print('Reading from', ADDRESS, PORT, '...')
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock.bind(ADDRESS_PORT)
    mreq = struct.pack("4sl", socket.inet_aton(ADDRESS), socket.INADDR_ANY)
    sock.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, mreq) ## sending IGMPv2 membership queries
    while True:
        print(time.asctime(), sock.recv(10240))
        sleep(0.02)

def write(sock):
    print('Writing to', ADDRESS, PORT, '...')
    sock.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, TTL) 
    while True:
        print(time.asctime(), "Sending:", PAYLOAD)
        sock.sendto(bytes(PAYLOAD,encoding='UTF-8'), ADDRESS_PORT)
        sleep(1)

if __name__ == "__main__":
    main(sys.argv)

