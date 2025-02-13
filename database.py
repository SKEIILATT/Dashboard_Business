import pandas as pd
from config import get_credentials
import mysql.connector as msc

#CONNECT DATABASE
def connect_database():
    credentials = get_credentials()
    try:
        connection = msc.connect(
            host = credentials["MYSQL_HOST"],
            user = credentials["MYSQL_USER"],
            password = credentials["MYSQL_PASSWORD"],
            database = credentials["MYSQL_DATABASE"]
        )
        return connection 
    except msc.Error as e:
        print(f"Could not connect to the database, try again: {e}")

