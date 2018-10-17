#! /usr/bin/env python3

# Echo server program

import socket, sys, re, os
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

while True:
    sock, addr = lsock.accept()
    
    from framedSock import framedSend, framedReceive

    if not os.fork():
        print('new child process handling connection from', addr)
        while True:
            payload = framedReceive(sock, debug)
            if debug: print("received: ", payload)
            if not payload: 
                if debug: print("child exiting")
                sys.exit(0)
            framedSend(sock, payload.encode("utf-8"), debug)

