# # server.py
# import socket
#
# serverIP = input("Enter server IP Address: ")
# serverPort = int(input("Enter server port number: "))
#
# myTCPSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# myTCPSocket.bind((serverIP, serverPort))
# myTCPSocket.listen(5)
# incomingSocket, incomingAddress = myTCPSocket.accept()
# maxBytesToReceive = 1024
#
# while True:
#     myData = incomingSocket.recv(maxBytesToReceive).decode('utf-8')
#     if not myData:
#         break
#     print("Client says: ", myData)
#     myMessage = input("Enter a message to send to client: ")
#     incomingSocket.send(bytearray(str(myMessage), encoding="utf-8"))
#
# incomingSocket.close()
# myTCPSocket.close()

import socket
import psycopg2

host = input("Enter the server IP address: ")
port = int(input("Enter the server port: "))

myTCPSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
myTCPSocket.bind((host, port))
myTCPSocket.listen(5)
incomingSocket, incomingAddress = myTCPSocket.accept()

try:
    db_connection = psycopg2.connect(
        "postgresql://neondb_owner:npg_ognWcMRFyS52@ep-withered-fog-a444emeu-pooler.us-east-1.aws.neon.tech/neondb?sslmode=require")
    cursor = db_connection.cursor()
    print("Successfully connected to PostgreSQL")
    cursor.execute("SELECT version();")
    print("PostgreSQL version:", cursor.fetchone())

    # Execute queries
    numberOfBytes = 1024

    while True:
        clientData = incomingSocket.recv(numberOfBytes).decode('utf-8')
        if not clientData:
            break
        print("Client says: ", clientData)

        if clientData == "1":
            cursor.execute('SELECT AVG("value")'
                           'FROM "Data_metadata" '
                           'WHERE "assetUid" AND "assetType" = "Smart Refrigerator" ')
            data = cursor.fetchall()
            incomingSocket.send(bytearray(str(data), encoding='utf-8'))
        elif clientData == "2":
            cursor.execute("SELECT ")  # INSERT QUERY 2 HERE
        elif clientData == "3":
            print("QUERY 3")  # INSERT QUERY # HERE


except Exception as e:
    print("Error connecting to the database:", e)



finally:
    # Close when done
    cursor.close()
    db_connection.close()

myTCPSocket.close()
print("Connection closed")
