File Sharing Platform - Using DGRAM
Mike Yandam


****List of Files****:
1)udpclient.py: Code to interact with server, outbound requests, and inbound packet data. 
2)udpserver.py: Code that handles incomming client connection/requests
3)0.jpg: A headshot of myself used for testing. 
4)0.pdf: A pdf of my resume used for testing.
5)1.txt: A text file of text copied from wikipedia of Thomas Jefferson used for testing. 

#3-5: Various files used to show grader that different file sizes and extensions can be sent on my application. 

****List of Features****: 
1)1 [file] - Download a file
2)2 [file] - "Upload" a file
3)3 - List all the avaliable files
4)4 - Search to see if specific file exists to download. 
5)Useful information is displayed in the server's terminal: It will print a message to the server's console if a user logged in or out and then displays the current logged in user count. 

****How to run****
NOTE: 
-In order to run this application, machines must be on the same network. 
-Server must be running first.
-Clients must use the IP address displayed in server's terminal.
-IP address that client enters is assumed to be correct.
-File that is shared must exist in current directory. 
-There is no file in current directory that is named to file that is requested to download. 
-Since UDP is connectionless, it is difficult to keep track of which clients are connected, so we are also assuming that client ONLY exists the application by enter '5' or 'exit'


1)SERVER:
To run the server, type the following in the terminal:
python udpserver.py

The server will then print out an IP address that the server will be hosted on. Have the user who runs 
the server send thes IP address to the clients who plan to use the File sharing Platform 

2)CLIENT:
To run the client, type the following in the terminal:
python udpclient.py

The application will then ask for the IP address which was printed when the server.py was run. 
Paste this IP address in the client terminal. 

To see a list of the accepted commands type 0 in the client terminal and you will see the following:

Weclome to Mike's File Sharing Platform!
---------------------------------------------
NOTE: Arguments found between [ ] will be provided by the user. DO NOT include the [ ]
--------------------------------------------------------------------------------------
To download a file, type the following:
1 [file]
-------------------------------------------------------------------------
To share a file, type the following:
2 [file]
--------------------------------------------------------------------
To get a list of files avaliable, type the following
3
----------------------------------------------------------------------------
To search for a file, type the following (*Remember to include extension):
4 [filename]
-------------------------------------------------------------------
Type 5 to exit the platform!
--------------------------------

