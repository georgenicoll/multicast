#!/usr/bin/env python3
#Shamelessly cribbed from https://github.com/dumplab/python_multicast/a
# and
# https://stackoverflow.com/questions/6243276/how-to-get-the-physical-interface-ip-address-from-an-interface#6250688
#
import netifaces
import sys
import socket
import struct
import multiprocessing
from time import sleep
import time

IF_ADDRESS='<Edit This>'
ADDRESS = "224.0.9.1"
PORT = 31001
TTL = 5
READ = 'read'
WRITE = 'write'
PAYLOAD_PREFIX = 'Multicast Hello'
ADDRESS_PORT = (ADDRESS, PORT)

def main(argv):
    if len(argv) > 2:
        interfaceName = argv[2]
        print('InterfaceName     : ', interfaceName)
        interface = getIPAddressOfInterface(interfaceName)
    else:
        interface = IF_ADDRESS

    print('Interface         : ', interface)
    print('Multicast Address : ', ADDRESS)
    print('Port              : ', str(PORT))
    print('Arguments         : ', str(argv))

    if len(argv) < 2:
        print('Need a mode and interface name.  Expecting <' + READ + '|' + WRITE + '> <interface>')
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
    sockfunc(sock, interface)

    print('Finished.')

# Nicked from https://code.activestate.com/recipes/439094-get-the-ip-address-associated-with-a-network-inter/
def getIPAddressOfInterface(ifname):
    return netifaces.ifaddresses(ifname)[netifaces.AF_INET][0]['addr']

def read(sock, interface):
    print('Reading from', ADDRESS, PORT, '...')
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock.bind(ADDRESS_PORT)
    sock.setsockopt(socket.SOL_IP, socket.IP_ADD_MEMBERSHIP, socket.inet_aton(ADDRESS)+socket.inet_aton(interface)) 

    while True:
        print(time.asctime(), sock.recv(10240))
        sleep(0.02)

def write(sock, interface):
    hostname = socket.gethostname()
    payload = PAYLOAD_PREFIX + ' from ' + hostname + ' (' + interface + ')'
    print('Writing to', ADDRESS, PORT, 'as', hostname, '...')
    sock.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, TTL) 
    sock.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_IF, socket.inet_aton(interface))
    num = 0
    while True:
        thisPayload = str(num) + ': ' + payload
        print(time.asctime(), "Sending:", thisPayload)
        sock.sendto(bytes(thisPayload,encoding='UTF-8'), ADDRESS_PORT)
        num = num + 1
        sleep(1)

if __name__ == "__main__":
    main(sys.argv)

