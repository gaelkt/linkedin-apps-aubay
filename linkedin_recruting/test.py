import pymysql

# Paramètres de connexion
host = "20p87j.stackhero-network.com"
port = 4072  # port spécifique de l'instance
user = "root"  # ou l'utilisateur indiqué dans ta configuration
password = "1kuePUKuZIZSu2LQrTcbaoFYtqOJsBfI"
database = "root"  # ou "essai" si c'est bien ta base de données
ssl_ca = "./isrgrootx1.pem"  # chemin vers le certificat CA téléchargé

try:
    connection = pymysql.connect(
        host=host,
        port=port,
        user=user,
        password=password,
        db=database,
        connect_timeout=10,
        ssl={'ca': ssl_ca}  # activation de SSL avec le certificat CA
    )
    print("Connexion réussie !")
    
    # Exemple : récupérer la version du serveur MySQL
    with connection.cursor() as cursor:
        cursor.execute("SELECT VERSION()")
        version = cursor.fetchone()
        print("Version de la base de données :", version)
except pymysql.MySQLError as e:
    print("Erreur lors de la connexion :", e)
finally:
    if 'connection' in locals() and connection.open:
        connection.close()
