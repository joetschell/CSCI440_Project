#!/usr/bin/env python
#Created by Ian Brown and Joe Schell and Colton Williams
#CSCI 440 Dr. Mountrouidou

from __future__ import print_function
from scapy.all import *
from datetime import datetime
import sys
import optparse
import os
from shutil import copyfile
from socket import *
from time import gmtime, strftime, localtime, sleep

def createPacket(seqNum, dstIP, dstPort, srcPort):
    #read from the packet file and save it to variable rawData with timestamp and sequence number
    file = open("packTemplate.txt", "r")
    timestamp = datetime.now().strftime("%H:%M:%S.%f")
    rawData = file.read() + " " + timestamp + " " + str(seqNum)
    print (rawData)
    packet = IP(dst=dstIP, proto=17) / UDP(sport=srcPort, dport=dstPort) / Raw(load=rawData)
    #packet.show()
    file.close()
    return packet

##Take input from user off the command line
parser = optparse.OptionParser()
parser.add_option('-g', '--generate', dest='generate', help='Use this to generate packets')
parser.add_option('-p', '--protocol', dest='protocol', help='Protocol to use')

(options, args) = parser.parse_args()

#port number > 5000
serverPort = 13037

#########################################################################################################
#Establishing UDP connection for Packet Error Rate measuring
#creating socket with IPV4 and UDP params, and binding it to serverPort
serverSocket = socket(AF_INET, SOCK_DGRAM)
serverSocket.bind(('', serverPort))
print ("Starting service listening on port <" + str(serverPort) + ">")
count = 0

#when a connection request is recieved, a new socket is created
while 1:
    message, clientAddress = serverSocket.recvfrom(2048)
    print ("Socket successfully opened from client, sending packets now.")
    print ("message: " + message);
    if(message == "PER"):
        while count < 10:
            send(createPacket(count, clientAddress[0], clientAddress[1], serverPort))
            count += 1
connectionSocket.close();
#End of Packet Error Rate Measuring
##########################################################################################################
