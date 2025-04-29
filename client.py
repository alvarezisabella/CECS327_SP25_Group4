#client.py
import socket

serverIP = input("Enter server IP Address: ")
serverPort = int(input("Enter server port number: "))
maxBytesToReceive = 1024
myTCPSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
myTCPSocket.connect((serverIP, serverPort))
validQuery = False

while True:
    myMessage = input("Please choose one of the following queries to process\n"
                         "1. What is the average moisture inside my kitchen fridge in the past three hours?\n"
                             "2. What is the average water consumption per cycle in my smart dishwasher?\n"
                             "3. Which device consumed more electricity among my three IoT devices (two refrigerators and a dishwasher)?\n")
    if myMessage == "exit":
        break
    selection = int(myMessage)
    if 1 <= selection <= 3:
        validQuery = True
    else:
        print("Sorry, this query cannot be processes. Please try one of the following:\n"
                         "1. What is the average moisture inside my kitchen fridge in the past three hours?\n"
                             "2. What is the average water consumption per cycle in my smart dishwasher?\n"
                             "3. Which device consumed more electricity among my three IoT devices (two refrigerators and a dishwasher)?\n")

    myTCPSocket.send(bytearray(str(myMessage), encoding='utf-8'))
    serverResponse = myTCPSocket.recv(maxBytesToReceive).decode('utf-8')
    print("Server Response: ", serverResponse)
myTCPSocket.close()