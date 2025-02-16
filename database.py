import pandas as pd
import mysql.connector as msc
#CONNECT DATABASE
def connect_database(user, password,host,database):
    try:
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
        return None

