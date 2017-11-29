#!/usr/bin/env python
from __future__ import print_function
from scapy.all import *
from datetime import datetime
import sys
import optparse
import os
from shutil import copyfile
from socket import *
from time import gmtime, strftime, localtime, sleep



def custom_action(packet):
    print (packet[0][2].payload)
    file.write(str(packet[0][2].payload) + "\n")

##Take input from user off the command line
parser = optparse.OptionParser()
parser.add_option('-i', '--ip', dest='ip', help='IP to sniff')
parser.add_option('-p', '--port', dest='port', help='Port to sniff', type=int)
parser.add_option('-c', '--count', dest='count', help='Number of packets to receive', type=int)
parser.add_option('-t', '--test', dest='test', help='Kind of test to run')

(options, args) = parser.parse_args()

if options.ip is None:
    options.ip = raw_input('Enter IP to sniff: ')

if options.port is None:
    options.port = int((raw_input('Enter Port to sniff on: ')))

if options.count is None:
    options.count = (raw_input('Enter packet count to receive: '))

if options.test is None:
    options.test = (raw_input('Enter type of test to run [PER/PDV]: '))

if (options.test.upper() != "PER" and options.test.upper() != "PDV"):
    while 1:
        options.test = (raw_input('Enter type of test to run [PER/PDV]: '))
        if (options.test.upper() == "PER" or options.test.upper() == "PDV"):
            break

if(options.test.upper() == "PER"):
    escape = ""
    #allows the user to keep running tests until "quit" is enterd
    while escape != "quit":
        serverName = options.ip
        serverPort = options.port
        file = open("sniffed.txt", "w")
        clientSocket = socket(AF_INET,SOCK_DGRAM)
        print ("Test initialized, hit ENTER to begin")
        message = str(options.count)
        clientSocket.sendto(message,(serverName, serverPort))
        pkts = sniff(filter="host " +  options.ip + " and port " + str(options.port) + 
                        " and ip and udp", count=options.count, prn=custom_action)

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
    file.close()
    clientSocket.close()


#elif(options.test.upper() == "PDV"):
    ##for ian to work on for PDV