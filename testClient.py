#!/usr/bin/env python
import sys
import os
from socket import *


serverName = "127.0.0.1"
serverPort = 13037

clientSocket = socket(AF_INET,SOCK_DGRAM)
message = raw_input('What test do u wanna run?: ')
clientSocket.sendto(message,(serverName, serverPort))
modifiedMessage, serverAddress = clientSocket.recvfrom(2048)
print modifiedMessage

clientSocket.close()


