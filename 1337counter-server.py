#!/usr/bin/python -u
import socket
import sys
from multiprocessing import Process
import time

send = ")"
receive = "("
BPM = 0
 
HOST = ''   # Symbolic name meaning all available interfaces
PORT = 50000 # Arbitrary non-privileged port
 
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
print 'Socket created'
 
#Bind socket to local host and port
try:
    s.bind((HOST, PORT))
except socket.error as msg:
    print 'Bind failed. Error Code : ' + str(msg[0]) + ' Message ' + msg[1]
    sys.exit()
     
print 'Socket bind complete'
 
#Start listening on socket
s.listen(10)
print 'Socket now listening'

def minuteCounter():
    while True:
        global BPM
        print "BPM = " + str(BPM*6)
        BPM = 0
        time.sleep(10)

p = Process(target=minuteCounter)
p.start()

#Function for handling connections. This will be used to create threads
def clientthread(conn):
    #Sending message to connected client
    conn.send('Welcome to the server. Type something and hit enter\n') #send only takes string
     
    #infinite loop so that function do not terminate and thread do not end.
    global BPM
    BPM = -1
    old_data = "0"
    zaps = -1

    while True:
         
        #Receiving from client
        data = conn.recv(1)
        if not data:
            break
        if data == send:
            if old_data != data:
                zaps = zaps+1
                print "zaps = " + str(zaps)
                BPM = BPM + 1
                old_data = data
        if data == receive:
            if old_data != data:
                old_data = data
     
    #came out of loop
    conn.close()
 
#now keep talking with the client
while 1:
    #wait to accept a connection - blocking call
    conn, addr = s.accept()
    print 'Connected with ' + addr[0] + ':' + str(addr[1])
     
 
s.close()

