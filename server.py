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
        "postgresql://neondb_owner:npg_F0ItnOsQ4kLv@ep-calm-moon-a5o0nb9m-pooler.us-east-2.aws.neon.tech/neondb?sslmode=require")
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
            cursor.execute(
                'SELECT payload ->> \'Moisture Meter - Refrigerator_Moisture\' AS moisture_value FROM "Data_virtual" WHERE payload ->> \'asset_uid\' = \'510-8u0-wpw-f29\';')  # INSERT QUERY 1 HERE
            data = cursor.fetchall()
            incomingSocket.send(bytearray(str(data), encoding='utf-8'))
        elif clientData == "2":
            cursor.execute(
                'SELECT AVG(CAST(payload ->> \'YF-S201 - Dishwasher_Water\' AS FLOAT)) AS avg_wtr_lit FROM "Data_virtual" WHERE payload ->> \'asses_uid\' = \'fci-ra7-433-615\';') # INSERT QUERY 2 HERE
        elif clientData == "3":
            cursor.execute(
            'SELECT device_id, SUM(kwh) AS total_kwh FROM (''SELECT \'510-8u0-wpw-f29\' AS device_id, payload ->> \'ACS712 - Refrigerator_Ammeter\' FROM "Data_virtual" WHERE payload ->> \'asset_uid\' = \'510-8u0-wpw-f29\' AND payload ->> \'ACS712 - Refrigerator_Ammeter\' IS NOT NULL'
                'UNION ALL'
                'SELECT \'4e308b46-9041-400c-a5ae-279f6ca506a9\' AS device_id, payload ->> \'sensor 3 35c551e7-b6ab-4f5c-9853-7ce4f6b58bbc\' FROM "Data_virtual" WHERE payload ->> \'asset_uid\' = \'4e308b46-9041-400c-a5ae-279f6ca506a9\' AND payload ->> \'sensor 3 35c551e7-b6ab-4f5c-9853-7ce4f6b58bbc\' IS NOT NULL'
                'UNION ALL'
                'SELECT \'fci-ra7-433-615\' AS device_id, payload ->> \'ACS712 - Dishwasher_Ammeter\' FROM "Data_virtual" WHERE payload ->> \'asset_uid\' = \'fci-ra7-433-615\' AND payload ->> \'ACS712 - Dishwasher_Ammeter\' IS NOT NULL'
            ') AS all_data'
            'GROUP BY device_id'
            'ORDER BY total_kwh DESC'
            'LIMIT 1;'
            )  # INSERT QUERY #3 HERE

except Exception as e:
    print("Error connecting to the database:", e)



finally:
    # Close when done
    cursor.close()
    db_connection.close()

myTCPSocket.close()
print("Connection closed")