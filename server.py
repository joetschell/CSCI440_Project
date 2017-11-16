#!/usr/bin/env python
#Created by Ian Brown and Joe Schell
#CSCI 440 Dr. Mountrouidou

from __future__ import print_function
from scapy.all import *
from datetime import datetime
import sys
import optparse
import os


##Take input from user off the command line
parser = optparse.OptionParser()
parser.add_option('-g', '--generate', dest.'generate', help='Use this to generate packets')
parser.add_option('-p', '--protocol', dest='protocol', help='Protocol to use')


(options, args) = parser.parse_args()

