#! /usr/bin/env python3

# Echo server program

import socket, sys, re
sys.path.append("../lib")       # for params
import params

switchesVarDefaults = (
    (('-l', '--listenPort') ,'listenPort', 50001),
    (('-d', '--debug'), "debug", False), # boolean (set if present)
    (('-?', '--usage'), "usage", False), # boolean (set if present)
    )


progname = "echoserver"
paramMap = params.parseParams(switchesVarDefaults)

debug,listenPort = paramMap['debug'], paramMap['listenPort']
#listenAddr = ''       # Symbolic name meaning all available interfaces

if paramMap['usage']:
    params.usage()

lsock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
bindAddr = ("127.0.0.1", listenPort)
lsock.bind(bindAddr)
lsock.listen(5)
#s.bind((listenAddr, listenPort))
#s.listen(1)              # allow only one outstanding request
# s is a factory for connected sockets
print("Listeing on:", bindAddr)

sock, addr = lsock.accept()

#conn, addr = s.accept()  # wait until incoming connection request (and accept it)
print('Connection received from', addr)

from framedSock import framedSend, framedReceive


while True:
    payload = framedReceive(sock, debug)
    if debug: print("received: ", payload)
    if not payload: break
    payload += b"!"
    framedSend(sock, payload, debug)

#sendMsg = "Echoing %s" % data
 #   print("Received '%s', sending '%s'" % (data, sendMsg))
  #  conn.send(sendMsg.encode())
#conn.close()
