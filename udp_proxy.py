#!/usr/bin/python

import sys, socket

def errOut(error):
    sys.stderr.write(error + "\n")
    sys.exit(1)

if len(sys.argv) != 2 or len(sys.argv[1].split(':')) != 3:
    errOut('Usage: udp_proxy.py localPort:remoteHost:remotePort')

localPort, remoteHost, remotePort = sys.argv[1].split(':')

try:
	localPort = int(localPort)
except:
	errOut('Invalid port number: ' + str(localPort))
try:
	remotePort = int(remotePort)
except:
	errOut('Invalid port number: ' + str(remotePort))

try:
	s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
	s.bind(('', localPort))
except:
	errOut('Failed to bind on port ' + str(localPort))

knownClient = None
knownServer = (remoteHost, remotePort)
sys.stderr.write('All set.\n')
while True:
    data, addr = s.recvfrom(32768)
    if knownClient is None:
        knownClient = addr
    if addr == knownClient:
        s.sendto(data, knownServer)
    else:
        s.sendto(data, knownClient)