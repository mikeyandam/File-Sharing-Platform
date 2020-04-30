"""
CSE 3461 Project 2: File Sharing Platform - Using DGRAM
By: Mike Yandam (yandam.4)

Note: Used the udpclient.py as a starting point
"""

# Echo client program
import socket, sys, select

#### CLIENT SETUP BEGIN ####

#Get IP Address of server
HOST = raw_input("What is the IP address of the server you wish to connect to?: ")
#Port Number 
PORT = 5000           # The same port as used by the server

#Create client socket object
clientSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) # UDP uses Datagram, but not stream

#Constant buffer size
buff = 1024

#Function that opens the file and then sends packet of size 1024 to the requester address 
def send_file(fileName, addr):
    print "\n\nSomeone has requested this file\n\n"

    x = addr.split(",")
    x1 = x[0].split("(")
    x2 = x[1].split(")")
    ip_address = x1[1].split("'")
    pnum = x2[0].strip()
    temp = (HOST, PORT)

    #first packet is the title of the file 
    clientSocket.sendto("title/" + fileName,(str(ip_address[1]),int(pnum)))
    f = open(fileName, "rb")
    data=f.read(buff)
    while(data):
        #Add some key identifying info like the title of the file and then the data
        #Packet structure: title/[filename]/data/[data that is read in]
        if(clientSocket.sendto("title/" + fileName +"/" +  "data/" + data,(str(ip_address[1]),int(pnum)))):
            print("sending...")
            data = f.read(buff)
    f.close()
    return

#Function that will download the file from the packets that are sent in
def download_file(title,data,flag):
    #If flag is 0 that means that the packet received was just the title
    if flag == 0:
        f = open(title, "ab")
        f.close()
    #If the flag is 1 that means the packet received had data 
    elif flag == 1:
        f = open(title, "ab")
        f.write(data)
        print "downloading..."

inputs = [clientSocket, sys.stdin]

print("Enter 0 if you would like to see a list of commands!")
sys.stdout.write("Enter your command -> ")
sys.stdout.flush()

while (1):
    readable, writable, exceptional = select.select(
        inputs, [], [])
    for s in readable:
        if s == clientSocket:
            response, serverAddress = clientSocket.recvfrom(65535)
            #Max split is 3 because the last part of the packet could potentially include '/' and that corrupts the data sent
            message = response.split('/',3)
            #Message sent to owner of file to send file to reciept
            if not response: sys.exit()
            else:
                #Send file to receiver
                if (message[0] == "1"):
                    x = list(response)
                    x[0] = "0"
                    fullMes = "".join(x)
                    fullMes
                    send_file(message[2],message[1]) 

                    #Parse the data to get IP and HOST
                    x = message[1].split(",")
                    x1 = x[0].split("(")
                    x2 = x[1].split(")")
                    ip_address = x1[1].split("'")
                    pnum = x2[0].strip()
                    temp = (HOST, pnum)

                    #Send to receiver socket
                    clientSocket.sendto(str(fullMes), (str(ip_address[1]), int(pnum)))
                    
                    print("Enter 0 if you would like to see a list of commands!")
                    sys.stdout.write("Enter your command -> ")
                    sys.stdout.flush()   
                else:
                    #If title that means packet has file information
                    if message[0] == "title":
                        #Packet is just title
                        if len(message) == 2:
                            download_file(message[1], "", 0)
                        #Packet has data information
                        elif len(message) == 4:
                            download_file(message[1], message[3], 1)
                    elif message[0] != "0" and message[0] != "1": 
                        print message[0]
                        print("Enter 0 if you would like to see a list of commands!")
                        sys.stdout.write("Enter your command -> ")
                        sys.stdout.flush()   
                    else:
                        print("Enter 0 if you would like to see a list of commands!")
                        sys.stdout.write("Enter your command -> ")
                        sys.stdout.flush()         
        else:
            message = sys.stdin.readline()
            if(message == "5\n" or message =="exit\n"):
                clientSocket.sendto("exit".encode(), (HOST, PORT))
                sys.exit()
            else:
                print message
                clientSocket.sendto(message.encode(), (HOST, PORT))




