"""
CSE 3461 Project 2: File Sharing Platform - Using DGRAM
By: Mike Yandam (yandam.4)

Note: Used the udpserver.py on Carmen as a starting point
"""

import socket, sys, select
import os.path
from os import path

####SERVER SETUP BEGIN####

#List of ERROR Messages that will be used
error_message_general = "\n**ERROR: Command entered is not valid.**\n"
error_message_duplicate_shared_file_name = "\n**ERROR: File with this name is already shared. Rename file and then share.**\n"
error_message_requested_file_not_found = "\n**ERROR: File with this name is not shared!.**\n"

#Get host's IP and choose a port
HOST = socket.gethostbyname(socket.gethostname())
print HOST
PORT = 5000

#Create server socket object
server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) # UDP uses Datagram, but not stream
server.bind((HOST, PORT))
server.settimeout(5)

addr = (HOST, PORT)
buff = 1024

inputs = [server]
#Container that will hold the shared files
sharedFiles = {}

#Function that prints out the list of commands for the user
def print_protocol_to_client():
    message= "\nWeclome to Mike's File Sharing Platform! \n"\
    "---------------------------------------------\n"\
    "NOTE: Arguments found between [ ] will be provided by the user. DO NOT include the [ ]\n"\
    "--------------------------------------------------------------------------------------\n"\
    "To download a file, type the following: \n"\
    "1 [file]\n"\
    "-------------------------------------------------------------------------\n"\
    "To share a file, type the following: \n"\
    "2 [file]\n"\
    "--------------------------------------------------------------------\n"\
    "To get a list of files avaliable, type the following\n"\
    "3\n"\
    "----------------------------------------------------------------------------\n"\
    "To search for a file, type the following (*Remember to include extension):\n"\
    "4 [filename]\n"\
    "-------------------------------------------------------------------\n"\
    "Type 5 to exit the platform!\n"\
    "--------------------------------\n/0"
    return message

#Function that checks if a file exists in the sharedFile container
def fileExists(fileName):
      for key, value in sharedFiles.iteritems():
            for x in value:
                  if x == fileName:
                    return True
      return False

#Function that returns who the owner of a requested file is
def find_owner(dictionary, fileName):
      owner_Of_File = ""
      for key, value in dictionary.iteritems():
            if fileName in value:
                  owner_Of_File = key
                  break
      return owner_Of_File

#Function that handles requesting to download a file
#First element in msg string is a flag
def download_file(requester, requestedFileName, socket):
      if (fileExists(requestedFileName)):
         ownerOfFile = find_owner(sharedFiles, requestedFileName)
         msg = "1/" + str(requester) +"/"+requestedFileName+"/0"
         socket.sendto(msg,ownerOfFile)
      else:
        socket.sendto(error_message_requested_file_not_found, requester) 
                   
#Function that handles sharing a file
def share_file(ownerOfFile, fileName, socket):
      if fileExists(fileName):
        socket.sendto(error_message_duplicate_shared_file_name, ownerOfFile)
        return
      if (ownerOfFile in sharedFiles):
            sharedFiles[ownerOfFile].append(fileName)
      else:
            tempArray = []
            tempArray.append(fileName)
            sharedFiles[ownerOfFile] = tempArray
      message = "File has been added to shared file list!/1"
      socket.sendto(message,ownerOfFile)
      print sharedFiles
      return

#Function that displays a list of all the shared files
def list_shared_files():
      listOfCurrentSharedFiles = []
      for key,value in sharedFiles.iteritems():
            listOfCurrentSharedFiles.extend(value)
      listOfCurrentSharedFiles = list(dict.fromkeys(listOfCurrentSharedFiles))
      message = "\nAccess to the following shared files: \n" + str(listOfCurrentSharedFiles) + "\n/1"
      return message

#Function where when user logs out it will remove their shared files
def user_log_out(clientAddress):
      if clientAddress in sharedFiles:
            del sharedFiles[clientAddress]

while inputs:
    readable, writable, exceptional = select.select(
      inputs, [], [])
    for s in readable:
        if(s is server):
          message, clientAddress = server.recvfrom(2048)
          response = message.decode().split()
          if message == "\n":
            server.sendto(error_message_general,clientAddress)
          elif len(response) > 2:
            error_message_general = "\n**ERROR: Command entered is not valid.**\n"
          else: 
            #Print protocol
            if response[0] == "0":
                  message = print_protocol_to_client()
                  server.sendto(message, clientAddress)
            #User requests to download a file
            elif response[0] == "1" and len(response) == 2:
                  download_file(clientAddress,response[1], server)
                  print "A File has requested for download!"
            #User has a file to share
            elif response[0] == "2" and len(response) == 2:
                  share_file(clientAddress, response[1],server)
                  print "A file may have been shared!"
            #User has requested to see a list of shared file
            elif response[0] == "3" and len(response) == 1:
                  message = list_shared_files()
                  server.sendto(message,clientAddress)
                  print "List all files requested!"
            #User has requested to search for a file
            elif response[0] == "4" and len(response) == 2:
                  print "A user is requesting to search for a file!"
                  if fileExists(response[1]):
                        msg = "File: " + "[" +response[1] + "]" + " is currently a downloadable file!"
                        server.sendto(msg,clientAddress)
                  else: 
                        msg = "File: " + "[" +response[1] + "]" + " is not currently a downloadable file!"
                        server.sendto(msg,clientAddress)
            #User has decided to exit platform
            elif response[0] == "exit" and len(response) == 1:
                  user_log_out(clientAddress)
                  print "A user has exited. Removing their files from list!"
            #User has entered an invalid command
            elif response[0] == "\n":
                        server.sendto(error_message_general,clientAddress)
            else:
                  server.sendto(error_message_general,clientAddress)
    for s in exceptional:
          inputs.remove(s)
          s.close()
                
