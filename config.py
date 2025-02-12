#ADD YOUR CREDENTIALS
#EXAMPLE WITH MY CREDENTIALS

def get_credentials():
    user = input("Enter your database username: ")
    password = input("Enter your database password: ")
    host = input("Enter your database host: ")
    database = input("Enter your database name: ")

    dict_credentials={
        "MYSQL_USER": user,
        "MYSQL_PASSWORD": password,
        "MYSQL_HOST": host,
        "MYSQL_DATABASE": database,
    }
    return dict_credentials