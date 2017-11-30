#!/usr/bin/env python
file = open("block.txt",  "r")
text = file.read()
print("original text: " + text)
text1 = text.split()
print("text1: " + text1[0])
file.close()

with open("block.txt") as f:
    while 1:
        c = f.read(1)
        print(c)
        if(not c):
            break