#! /usr/bin/env python3

#File transfer client program
import socket, sys, re
sys.path.append("../lib")    # for params
import params

from framedSock import framedSend, framedReceive


#First get input from user
command = input("Please enter the command for file transfer. ")

print ("Command to transmit is '%s'" % command)
size = sys.getsizeof(command)
print ("Size in bytes is '%d'" % size)

switchesVarDefaults = (
    (('-s', '--server'), 'server', "127.0.0.1:50001"),
    (('-d', '--debug'), "debug", False), # boolean (set if present)
    (('-?', '--usage'), "usage", False), #boolean (set if present)
    )

progname = "framedClient"
paramMap = params.parseParams(switchesVarDefaults)

server, usage, debug = paramMap["server"], paramMap["usage"], paramMap["debug"]

if usage:
    params.usage()

try:
    serverHost, serverPort = re.split(":", server)
    serverPort = int(serverPort)
except:
    print ("Can't parse server: port from '%s'" % server)
    sys.exit(1)

s = None
for res in socket.getaddrinfo(serverHost, serverPort, socket.AF_UNSPEC, socket.SOCK_STREAM):
    af, socktype, proto, canonname, sa = res
    try:
        print("creating sock: af=%d, type=%d, proto=%d" % (af, socktype, proto))
        s = socket.socket(af, socktype, proto)
    except socket.error as msg:
        print(" error: %s" % msg)
        s = None
        continue
    try:
        print(" attempting to connect to %s" % repr(sa))
        s.connect(sa)
    except socket.error as msg:
        print(" error: %s" % msg)
        s.close()
        s = None
        continue
    break

if s is None:
    print("Could not open Socket")
    sys.exit(1)

#s.send(command.encode())

print("Sending '%s'" % command)
framedSend(s, command.encode('UTF-8'), debug)
print("reveived:", framedReceive(s, debug))
#s.send(command.encode())

#s.shutdown(socket.SHUT_WR) # no more ouput

#while 1:
 #   data = s.recv(1024).decode()
  #  print("Received '%s'" % data)
   # if len(data) == 0:
    #    break
#print("Zero length read. Closing")
#s.close()
