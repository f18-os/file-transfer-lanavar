# File send sendfile and receive assistance
# Import necessary files
import re, sys

# Framed send original
def framedSend(sock, payload, debug=0):
     if debug: print("framedSend: sending %d byte message" % len(payload))
     msg = str(len(payload)).encode() + b':' + payload
     while len(msg):
         nsent = sock.send(msg)
         msg = msg[nsent:]

# Global buffer     
rbuf = b""   

# Static send file takes the socket, the file where it will come from and the file where it will go
def framedFileSend(sock, inFile, outFile, debug=0):
     if debug: print("framedFileSend: sending from file %s, to %s total %b" % inFile, outFile, size)
     fullText = ""

     # Open file to read
     inF = open(inFile, "r+")

     # Get the text from the file
     with open(inFile, "r") as textFile:
          for line in textFile:
               fullText += line

     # Find the total length of the file and filename that will be sent
     totalSize = len(outFile) 
     totalSize += len(fullText)
     
     # Concantanetes the message with size:filename;payload
     msg = str(totalSize).encode("utf-8") + b':' + outFile + b";" +fullText.encode("utf-8")

     # Send the message
     while len(msg):
          nsent = sock.send(msg)
          msg = msg[nsent:]
     
# Static receive buffer
def framedReceive(sock, debug=0):
    global rbuf
    state = "getLength"
    msgLength = -1
    fileName = "msg.txt"

    # Loop to get the message
    while True:
         # Starts by getting the length from the message
         if (state == "getLength"):
             match = re.match(b'([^:]+):(.*)', rbuf, re.DOTALL | re.MULTILINE) # look for colon
             if match:
                  lengthStr, rbuf = match.groups()
                  try: 
                       msgLength = int(lengthStr) 
                  except:
                       if len(rbuf):
                            print("badly formed message length:", lengthStr)
                            return None
                  state = "getFilename"
         # Get the name of the file similarly
         if state == "getFilename":
               match = re.match(b'([^;]+);(.*)', rbuf, re.DOTALL | re.MULTILINE) # look for semicolon
               if match:
                    fileName, rbuf = match.groups()
                    fileLength = len(fileName)
                    msgLength -= fileLength
               state = "getPayload"
         # Get the entire payload of message
         if state == "getPayload":
             # Event where the entire message is read, it writes it to a file
             if len(rbuf) >= msgLength:
                 payload = rbuf[0:msgLength]
                 rbuf = rbuf[msgLength:]
                 of = open(fileName, "w+")
                 of.write(payload.decode("utf-8"))
                 of.close
                 return ("File transfered!")

         r = sock.recv(100)
         rbuf += r
         
         # Event where nothing new is received it is an error
         if len(r) == 0:
             if (rbuf.decode("utf-8") == '\n'):
                  print("Transfer complete")
                  return(None)
             if len(rbuf) != 0:
                 print("FramedReceive: incomplete message. \n  state=%s, length=%d, rbuf=%s" % (state, msgLength, rbuf))
             return None
         if debug: print("FramedReceive: state=%s, length=%d, rbuf=%s" % (state, msgLength, rbuf))
