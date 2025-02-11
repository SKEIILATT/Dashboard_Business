import pandas as pd
import mysql.connector as msc

conexion = msc.connect(
    user="Javier",
    password = "admin",
    host="localhost",
    database="company",
    port = "3306"
)
print(conexion)

