import re, sys

def framedSend(sock, payload, debug=0):
     if debug: print("framedSend: sending %d byte message" % len(payload))
     msg = str(len(payload)).encode() + b':' + payload
     while len(msg):
         nsent = sock.send(msg)
         msg = msg[nsent:]
     
rbuf = b""   

#Stratic send file
def framedFileSend(sock, inFile, outFile, debug=0):
     if debug: print("framedFileSend: sending from file %s, to %s total %b" % inFile, outFile, size)
     fullText = ""
     # Open file to read
     inF = open(inFile, "r+")
     
     with open(inFile, "r") as textFile:
          for line in textFile:
               fullText += line
     totalSize = len(outFile) + len(":;bb ")
     
     
     totalSize += len(fullText)
     

     msg = str(totalSize).encode("utf-8") + b':' + outFile + b";" +fullText.encode("utf-8")
     print (msg)
     print (len(msg))
     while len(msg):
          nsent = sock.send(msg)
          msg = msg[nsent:]
     
     

                   # static receive buffer
def framedReceive(sock, debug=0):
    global rbuf
    state = "getLength"
    msgLength = -1
    fileName = "msg.txt"
    while True:
         if (state == "getLength"):
             match = re.match(b'([^:]+):(.*)', rbuf, re.DOTALL | re.MULTILINE) # look for colon
             if match:
                  lengthStr, rbuf = match.groups()
                  try: 
                       msgLength = int(lengthStr) 
                       msgLength -= len(lengthStr)
                       msgLength -= 1
                  except:
                       if len(rbuf):
                            print("badly formed message length:", lengthStr)
                            return None
                  state = "getFilename"
         if state == "getFilename":
               match = re.match(b'([^;]+);(.*)', rbuf, re.DOTALL | re.MULTILINE) # look for semicolon
               if match:
                    fileName, rbuf = match.groups()
                    fileLength = len(fileName)+1
                    msgLength -= fileLength
               state = "getPayload"
         if state == "getPayload":
             if len(rbuf) >= msgLength:
                 payload = rbuf[0:msgLength]
                 rbuf = rbuf[msgLength:]
                 of = open(fileName, "w+")
                 of.write(payload.decode("utf-8"))
                 
                 of.close
                 print (rbuf)
                 print ("done")
                 return payload
         r = sock.recv(100)
         rbuf += r
         
         if len(r) == 0:
             if len(rbuf) != 0:
                 print("FramedReceive: incomplete message. \n  state=%s, length=%d, rbuf=%s" % (state, msgLength, rbuf))
             return None
         if debug: print("FramedReceive: state=%s, length=%d, rbuf=%s" % (state, msgLength, rbuf))
