import mysql.connector
from mysql.connector import Error

# Paramètres de connexion
host = "20p87j.stackhero-network.com"
port = 4072
user = "root"
password = "1kuePUKuZIZSu2LQrTcbaoFYtqOJsBfI"
database = "essai"  # À adapter selon le nom de ta base

try:
    connection = mysql.connector.connect(
        host=host,
        port=port,
        user=user,
        password=password,
        database=database
    )
    
    if connection.is_connected():
        print("Connexion réussie !")
        cursor = connection.cursor()
        cursor.execute("SELECT VERSION()")
        version = cursor.fetchone()
        print("Version de la base de données :", version)
        
except Error as err:
    print("Erreur lors de la connexion :", err)
    
finally:
    if connection.is_connected():
        cursor.close()
        connection.close()
