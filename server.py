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
parser.add_option('-p', '--port', dest='port', help='Port to use', type=int)

(options, args) = parser.parse_args()

if options.port is None:
    options.port = int(raw_input('Enter Port: '))

#port number > 5000
serverPort = options.port

#########################################################################################################
#Establishing UDP connection for Packet Error Rate measuring
#creating socket with IPV4 and UDP params, and binding it to serverPort
serverSocket = socket(AF_INET, SOCK_DGRAM)
serverSocket.bind(('', serverPort))
print ("Starting service listening on port <" + str(serverPort) + ">")
count = 0
iterator = 0
escape = ""

#when a connection request is recieved, a new socket is created
while escape != "quit":
    message, clientAddress = serverSocket.recvfrom(2048)
    count = int(message[4:])
    print ("count: " + message[4:])
    print ("Sending Packets for " + message[:3] + " test...");
    if(message[:3] == "PER"):
        time.sleep(.2)
        while iterator < count:
            send(createPacket(iterator, clientAddress[0], clientAddress[1], serverPort))
            iterator += 1

#Specify whether to run another test or to quit the program
    while 1:
        escape = raw_input("Hit ENTER to run another test or type \"quit\" to stop\n")
        if(escape == "quit"):
           print ("Thank You")
           break
        if(escape != "" and escape != "quit"):
            escape = ""
        elif(escape == ""):
            print ("Ready for new test.")
            break
#reset packet count for subsequent tests  
    count = 0
    iterator = 0
#End of Packet Error Rate Measuring
##########################################################################################################
