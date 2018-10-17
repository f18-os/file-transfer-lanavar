#! /usr/bin/env python3

#File transfer client program
import socket, sys, re
sys.path.append("../lib")    # for params
import params, os

from framedSock import framedSend, framedReceive, framedFileSend


#First get input from user, loop until a valid entry is selected
command = input("Please enter the command for file transfer: ")



# Loop to get valid entry
while(True):

#Check for correct information provided
    wordSplit = command.split()
    length = len(wordSplit)
    if(length == 0):             # event nothing is entered
        print("No commands entered.")
        command = input("Please enter a valid command, or exit: ")
        continue
    if(length ==  1):           # if only one word is entered check for exit
        if (command == "exit"): # Exit clause
            print("Finished with file transfer.")
            exit(1)
        else:
            print("Invalid command.")
            command = input("Please enter a valid command, or exit: ")
            continue
    if(length > 2):           # if there are too many comands entered
        print("Invalid command, it can only have 2 words.")
        command = input("Please enter a valid command, or exit: ")
        continue
    commandPart = wordSplit[0]
    commandFile = wordSplit[1]
    #print("first word is %s" % commandPart)
    #print("second word is %s" % commandFile)
    if(commandPart == "put"): # Check to put document
        print ("Valid command")
        choice = 1
        break
    elif(commandPart == "get"): # Check to get a document
        print("Valid command")
        choice = 2
        break
    
    command = input("Please enter a new command or exit to finish: ")
if choice == 2:
    outputFile = commandFile
    commandFile = "serverfiles/"+outputFile
elif choice == 1:
    outputFile = "serverfiles/" + commandFile

# Check for a valid file to transfer
if not os.path.isfile(commandFile):
    print("File does not exist!")
    exit(1)


#Check for empty file
sizeFile = os.path.getsize(commandFile)
if (sizeFile == 0):
    print("Zero size file!")
    exit(1)

# Check if file already exists in destination folder
if os.path.isfile(outputFile):
    print("File already exists as output!")
    exit(1)

    
#print ("Command to transmit is '%s'" % command)
size = sys.getsizeof(commandFile)
#print ("Size in bytes is '%d'" % size)

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

#print("Sending '%s'" % command)


framedFileSend(s, commandFile.encode("utf-8"), outputFile.encode("utf-8"), debug)
print("Done sending")
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
