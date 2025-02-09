# linkedin-apps-aubay

## Création de l'image pour le backend

Naviguez dans le répertoire `linkedin_recruiting` et créez l'image Docker pour le backend :

```bash
cd linkedin_recruiting
docker build -t linkedin_backend .
Création de l'image pour le frontend
Naviguez dans le répertoire linkedin_recruiting_frontend et créez l'image Docker pour le frontend :

bash
Copy
cd ../linkedin_recruiting_frontend
docker build -t linkedin_frontend .
Assemblage des containers avec Docker Compose
Retournez dans le répertoire parent et démarrez les containers avec Docker Compose :

bash
Copy
cd ..
docker-compose up
Création d'un service systemd pour lancer les containers
Vous pouvez créer un service pour lancer vos containers automatiquement. Commencez par créer le fichier de service :

bash
Copy
sudo nano /etc/systemd/system/linkedin_recruiting.service
Ensuite, ajoutez le contenu suivant (n'oubliez pas d'adapter les chemins et commandes selon votre configuration) :

ini
Copy
[Unit]
Description=Lancement automatique de mes conteneurs avec Docker Compose
Requires=docker.service
After=docker.service

[Service]
# Indiquez le répertoire où se trouve votre fichier docker-compose.yml
WorkingDirectory=/chemin/vers/votre/projet
# Commande pour démarrer les conteneurs en arrière-plan
ExecStart=/usr/local/bin/docker-compose up -d
# Commande pour arrêter les conteneurs proprement
ExecStop=/usr/local/bin/docker-compose down
# Redémarrer le service en cas d'échec
Restart=always

[Install]
WantedBy=multi-user.target
Après avoir sauvegardé le fichier, rechargez les fichiers de configuration systemd :

bash
Copy
sudo systemctl daemon-reload
Ensuite, activez et démarrez le service pour qu’il se lance automatiquement au démarrage :

bash
Copy
sudo systemctl start linkedin_recruiting.service
Vous pouvez vérifier immédiatement le statut du service avec :

bash
Copy
sudo systemctl status linkedin_recruiting.service