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
    rawData = file.read()
    if(rawData[-1] == '\n'):
        rawData = rawData[:-2]
    rawData = rawData + " " + timestamp + " " + str(seqNum)
    print (rawData)
    packet = IP(dst=dstIP, proto=17) / UDP(sport=srcPort, dport=dstPort) / Raw(load=rawData)
    #packet.show()
    file.close()
    return packet

##Take input from user off the command line
parser = optparse.OptionParser()
parser.add_option('-g', '--generate', dest='generate', help='Use this to generate packets')
parser.add_option('-p', '--port', dest='port', help='Port to use', type=int)
parser.add_option('-t', '--test', dest='test', help='Kind of test to run')

(options, args) = parser.parse_args()

if options.port is None:
    options.port = int(raw_input('Enter Port: '))

if options.test is None:
    options.test = (raw_input('Enter type of test to run [PER/PDV]: '))

if (options.test.upper() != "PER" and options.test.upper() != "PDV"):
    while 1:
        options.test = (raw_input('Enter type of test to run [PER/PDV]: '))
        if (options.test.upper() == "PER" or options.test.upper() == "PDV"):
            break

#port number > 5000
serverPort = options.port


#########################################################################################################
#Establishing UDP connection for Packet Error Rate measuring
#creating socket with IPV4 and UDP params, and binding it to serverPort
if(options.test.upper() == "PER"):
    serverSocket = socket(AF_INET, SOCK_DGRAM)
    serverSocket.bind(('', serverPort))
    print ("Starting service listening on port <" + str(serverPort) + ">")
    count = 0
    iterator = 0
    escape = ""

    #when a connection request is recieved, a new socket is created
    while escape != "quit":
        message, clientAddress = serverSocket.recvfrom(2048)
        count = int(message)
        print ("count: " + message)
        print ("Sending Packets for PER test...");

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
