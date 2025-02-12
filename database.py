import pandas as pd
from config import get_credentials
import mysql.connector as msc

#CONNECT DATABASE
def connect_database():
    credentials = get_credentials()
    connection = msc.connect(
        host = credentials["MYSQL_HOST"],
        user = credentials["MYSQL_USER"],
        password = credentials["MYSQL_PASSWORD"],
        database = credentials["MYSQL_DATABASE"]
    )
    return connection

#GENERATE DATAFRAMES
print(connect_database())