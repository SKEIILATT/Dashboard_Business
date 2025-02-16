import pandas as pd
import mysql.connector as msc

connection = None

#CONNECT DATABASE
def connect_database(user, password,host,database):
    global connection
    try:
        if connection and connection.is_connected():
            return connection

        connection = msc.connect(
            host = host,
            user = user,
            password = password,
            database = database
        )
        if connection.is_connected():
            print("Succesfull connected to the database")
            return connection
        else:
            print("Failed to connect to the database.")
            return None
    except msc.Error as e:
        print(f"Could not connect to the database, try again: {e}")

def close_connection():
    global connection
    if connection and connection.is_connected():
        connection.close()
        print("Connection closed")
