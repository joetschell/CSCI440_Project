# CSCI 440 Final Project
## Ian Brown - Joe Schell - Colton Williams ##

### Welcome to PacketPal! ###
PacketPal is a network tool used to calculate two metrics:

    1. Packet Error Rate
    2. Packet Delay Variation

### How it Works ###
PacketPal makes use of Scapy, a python library used for packet manipulation, including sending and receiving custom made packets.  In order to get proper measurements, PacketPal uses Scapy to generate uniform packets using a file called `packTemplate.txt`. For each test, the client and server must be up and running.  Once that has happened the tests begin once the user hits the **ENTER** key on the client.  The client will send a message to the server so it knows to begin.  The server will then generate packets and send them back to the client.  The client will run calculations on the packets and output the results to the screen.  When the test has complete, the user is prompted to run another test, or can input `"quit"` on the client and server to end testing.  

#### Packet Error Rate ####
In order to test packet error rate the client and server scripts, `clientPal` and `serverPal`, create a UDP connection with each other.  This allows errors to be detected in the packets once they have been received.  A payload in a packet whose content is not the same as the `packTemplate.txt` constitutes a packet error, and so does receiving packets out of order. To check for these UDP packets coming in out of order, the server appends a sequence number to the payload of each outgoing packet.  These sequence numbers are ignored when the client checks the payload for errors. When the client receives the packets, it writes the payload of each one to a file called `sniffed_per.txt` for use in comparison with `packTemplate.txt`.  The client counts how many packets it finds errors in and divides that number by how many packets were received to give an error rate percentage.
76
#### Packet Delay Variation ####
To properly start the test for packet delay variation, it is important to note that a TCP connection must be established between the client and the server.  This ensures each packet will be received by the client.  Therefore the server must be started **BEFORE** the client is started.  Similar to packet error rate, the client sends a message to the server to initiate the test.  Before this message is sent, however, the clint runs a `ping` command using the server as the destination.  The current version currently sends 15 pings to the server, so it is normal to experience a few moments of no output to the screen as the client is doing this.  The client does this to get the average round trip time to the server.  This value is divided by 2, and sent in the message to the server.  This way the server will know the one way delay to the client.  The server generates then its packets and appends a timestamp to the payload of each packet that is the time the packet was generated plus the one way delay, as a method to sync the clocks of the client and the server.   When the client receives each packet, it appends the time it received them to the payload and writes the payload of each packet to a file called `sniffed_pdv.txt` for use in calculating the packet delay variation.  The client then calculates the difference of when it received each packet and when the packet was sent.  The result is the delay of the packet.  These are converted to milliseconds and written to a file called `avgDelay.txt`.  From there, each of these values is added up and divided by the number of values added to give the average delay.  The client then calculates the standard deviation of the delays using the average delay and each packet's delay.  Then the packet delay variation is calculated by taking the difference of each packet's delay to the average.  That value is then subtracted by the standard deviation and then the absoltue value of the subtraction is taken.  The maximum and minimum values are found from among those.  The maximum is subtracted by the minimum to give the packet delay variation in terms of plus or minus (+/-) of the average.  

### Usage ###

#### Server ####
The server has two flags that must be specified:

    1. The port to be opened on the server and
    2. The second is the test to run.  The test must be either "per" or "pdv".  (This is caps insensitve).

```bash
sudo ./serverPal.py -p <ServerPort> -t <TestType>
```
#### Client ####
The client has four flags that must be specified.  

    1. The IP of the server.  
    2. The port to be opened on the server
    3. The number of packets for the server to send to the client
    4. The test to run.  The test must be either "per" or "pdv".  (This is caps insensitve).
    
```bash
sudo ./clientPal.py -i <ServerIP> -p <ServerPort> -c <PacketCount> -t <TestType>
```
**IMPORTANT NOTE:** the ports and test types specified on client and server must match each other for PacketPal to work.

### Dependencies ###

Scapy


