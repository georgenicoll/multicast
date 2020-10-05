#!/usr/bin/env python3
#Shamelessly cribbed from https://github.com/dumplab/python_multicast/
import sys
import socket
import struct
import multiprocessing
from time import sleep
import time

IF_ADDRESS='<Edit This>'
ADDRESS = "224.0.9.1"
PORT = 31001
TTL = 6
READ = 'read'
WRITE = 'write'
PAYLOAD_PREFIX = 'Multicast Hello'
ADDRESS_PORT = (ADDRESS, PORT)

def main(argv):
    if len(argv) > 1:
        interfaceAddress = argv[2]
    else:
        interfaceAddress = IF_ADDRESS

    print('Interface         : ', interfaceAddress)
    print('Multicast Address : ', ADDRESS)
    print('Port              : ', str(PORT))
    print('Arguments         : ', str(argv))

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
    sockfunc(sock, interfaceAddress)

    print('Finished.')

def read(sock, interfaceAddress):
    print('Reading from', ADDRESS, PORT, '...')
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock.bind(ADDRESS_PORT)
    sock.setsockopt(socket.SOL_IP, socket.IP_ADD_MEMBERSHIP, socket.inet_aton(ADDRESS)+socket.inet_aton(interfaceAddress)) 
    while True:
        print(time.asctime(), sock.recv(10240))
        sleep(0.02)

def write(sock, interfaceAddress):
    hostname = socket.gethostname()
    payload = PAYLOAD_PREFIX + ' from ' + hostname + ' (' + interfaceAddress + ')'
    print('Writing to', ADDRESS, PORT, 'as', hostname, '...')
    sock.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, TTL) 
    sock.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_IF, socket.inet_aton(interfaceAddress))
    num = 0
    while True:
        thisPayload = str(num) + ': ' + payload
        print(time.asctime(), "Sending:", thisPayload)
        sock.sendto(bytes(thisPayload,encoding='UTF-8'), ADDRESS_PORT)
        num = num + 1
        sleep(1)

if __name__ == "__main__":
    main(sys.argv)

