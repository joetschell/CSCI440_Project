#!/usr/bin/env python
from __future__ import print_function
from scapy.all import *
from datetime import datetime, timedelta
import sys
import optparse
import os
from shutil import copyfile
from socket import *
from time import gmtime, strftime, localtime, sleep, strptime
from subprocess import call


#For PER Test
def custom_action(packet):
    print (packet[0][2].payload)
    file.write(str(packet[0][2].payload) + "\n")

#For PDV Test
def custom_action2(packet):
    timestamp = datetime.now()
    timestampString = timestamp.strftime("%H:%M:%S.%f")
    print (packet[0][2].payload)
    file2.write(str(packet[0][2].payload) + " " + timestampString + "\n")

def calculateAverageDelay():
    avgDelayFile = open("avgDelay.txt", "w")
    with open("sniffed_pdv.txt") as f:
        for line in f:
            temp = line.split()
            print("temp1: " + temp[1] + " temp2: " + temp[2])
            serverTime = datetime.strptime(temp[1], "%H:%M:%S.%f")
            clientTime = datetime.strptime(temp[2], "%H:%M:%S.%f")
            timeDiff = clientTime - serverTime
            timeDiffString = str(timeDiff)
            print("timeDiff: " + timeDiffString)
            timeSplit = timeDiffString.split(':')
            hours = timeSplit[0]
            minutes = timeSplit[1]
            seconds = timeSplit[2]
            ms = float(seconds)*1000 + int(minutes)*60000 + int(hours)*3600000
            print(str(ms) + "ms")
            avgDelayFile.write(str(ms) + "\n")
    avgDelayFile.close()
    avg = 0
    lineCount = 0
    with open("avgDelay.txt") as f:
        for line in f:
            avg += float(line)
            lineCount += 1
    avg = avg / lineCount
    print("avg: " + str(avg))


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
#########################################################################################################
#
#                           PACKET ERROR RATE TEST
#
##########################################################################################################
if(options.test.upper() == "PER"):
    escape = ""
    begin = "a"
    #allows the user to keep running tests until "quit" is enterd
    while escape != "quit":
        serverName = options.ip
        serverPort = options.port
        file = open("sniffed.txt", "w")
        clientSocket = socket(AF_INET,SOCK_DGRAM)
        print ("PER Test initialized, hit ENTER to begin")
        #Wait for user to press ENTER before beginning the test
        while 1:
            begin = raw_input("")
            if(begin != ""):
                print("Invalid value")
            elif(begin == ""):
                print ("Starting test...")
                break

        message = str(options.count)
        clientSocket.sendto(message,(serverName, serverPort))
        pkts = sniff(filter="host " +  options.ip + " and port " + str(options.port) + 
                        " and ip and udp", count=options.count, prn=custom_action)

    #Specify whether to run another test or to quit the program
        while 1:
            escape = raw_input("Hit ENTER to run another PER test or type \"quit\" to stop\n")
            if(escape == "quit"):
                print ("Thank You")
                break
            if(escape != "" and escape != "quit"):
                escape = ""
            elif(escape == ""):
                print ("Ready for new PER test.")
                break
    file.close()
    clientSocket.close()
#################################################################################################################
#                           END OF PACKET ERROR RATE TEST 
###################################################################################################################


#################################################################################################################
#
#                           PACKET DELAY VARIATION TEST
#
#################################################################################################################


elif(options.test.upper() == "PDV"):
    escape = ""
    begin = "a"

    #allows the user to keep running tests until "quit" is enterd
    while escape != "quit":
        serverName = options.ip
        serverPort = options.port
        file2 = open("sniffed_pdv.txt", "w")
        clientSocket = socket(AF_INET, SOCK_STREAM)
        clientSocket.connect((serverName,serverPort))
        print("PDV Test initialized, hit ENTER to begin.")
        #Wait for user to press ENTER before beginning the test
        while 1:
            begin = raw_input("")
            if(begin != ""):
                print("Invalid value")
            elif(begin == ""):
                print ("Starting test...")
                break

        #Start ping to server
        print("Calculating average one way delay...")
        ping = subprocess.check_output(["ping", options.ip, "-c 1"])
        print("PING START-----------------------------")
        print(ping)
        print("PING END--------------------------------")
        print(ping[-21:-16])
        print("PING DOUBLE END--------------------------")
        oneWayDelay = float(ping[-21:-16])/2
        print("ONE WAY DELAY: " + str(oneWayDelay) + " --------------------")

        clientSocket.send(str(options.count)+ " " + str(oneWayDelay))
        pkts = sniff(filter="host " +  options.ip + " and port " + str(options.port) + 
                        " and ip and tcp", count=options.count, prn=custom_action2)
        file2.close()
        calculateAverageDelay()

        #Specify whether to run another test or to quit the program
        while 1:
            escape = raw_input("Hit ENTER to run another PDV test or type \"quit\" to stop\n")
            if(escape == "quit"):
                print ("Thank You")
                break
            if(escape != "" and escape != "quit"):
                escape = ""
            elif(escape == ""):
                print ("Ready for new PDV test.")
                break

    
    clientSocket.close()