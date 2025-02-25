# Guide Deploiment sur une VM On Promise
***


Ce document décrit la configuration des services systemd mis en place pour :

- Lancer le backend FastAPI dans un container Docker.
- Lancer le frontend React en mode preview via Yarn.
- Rebuild automatiquement le frontend React et le backend python tous les soirs à 18h.

## 1. Service pour le Backend FastAPI (Docker)

- creer le fichier jobs.service dans system

```bash
nano /etc/systemd/system/jobs.service

```
-copier le contenu suivant 

```ini
[Unit]
Description=Service Docker pour le container "jobs"
After=docker.service
Requires=docker.service

[Service]
Restart=always
# Arrête et supprime le container existant pour éviter les conflits
ExecStartPre=-/usr/bin/docker stop jobs
ExecStartPre=-/usr/bin/docker rm jobs
# Lancement du container avec les ports et volumes définis
ExecStart=/usr/bin/docker run --name jobs -p 8081:8081 -p 3306:3306 -p 5672:5672 -p 15762:15672 -v mysql_data:/var/lib/mysql -v jobs_media:/app/media backend-image

[Install]
WantedBy=multi-user.target


```
- recharger systemd


```bash
sudo systemctl daemon-reload

```
-Activer et démarrer le service :

```bash
sudo systemctl enable jobs.service
sudo systemctl start jobs.service

```

2. Service pour le Build

- creer le fichier /etc/systemd/system/rebuild.service

```bash
nano /etc/systemd/system/rebuild.service

```
- copier le contenu suivant 

```ini

[Unit]
Description=Reconstruction de l'image Docker backend-image

[Service]
Type=oneshot
ExecStart=/usr/bin/docker build -t backend-image /root/apps/linkedin_aubay_apps/linkedin_recruting/Dockerfile
ExecStartPost=/usr/bin/docker rm -f jobs
ExecStartPost=/usr/bin/docker run --name jobs -p 8081:8081 -p 3306:3306 -p 5672:5672 -p 15762:15672 -v mysql_data:/var/lib/mysql -v jobs_media:/app/media backend-image


```

- Créez un fichier /etc/systemd/system/rebuild.timer :

ce timer va construire l'image docker pour le backend tous les soir a 18h

```ini
[Unit]
Description=Timer pour reconstruire l'image Docker tous les jours à 18h

[Timer]
OnCalendar=*-*-* 18:00:00
Persistent=true

[Install]
WantedBy=timers.target

```
- redemmarer les daemons

```bash
sudo systemctl daemon-reload
sudo systemctl enable rebuild.timer
sudo systemctl start rebuild.timer


```



## Service pour le Frontend React (Yarn Preview)

Ce service lance l'application React en mode preview via Yarn.
La commande utilise l'option --host pour lier le serveur sur toutes les interfaces (0.0.0.0) 
- creer le fichier de service 

```bash
nano /etc/systemd/system/linkedin-frontend.service

```
- copier et coller le contenu suivant

```ini
[Unit]
Description=Service pour lancer le frontend React avec Yarn
After=network.target

[Service]
WorkingDirectory=/root/apps/linkedin-apps-aubay/linkedin_recruting_frontend
ExecStart=/usr/local/bin/yarn preview --host 
Restart=always
User=root
# Définition du PATH pour s'assurer que yarn et node sont accessibles
Environment="PATH=/usr/local/bin:/usr/bin"

[Install]
WantedBy=multi-user.target

```

- Recharger systemd:

```bash
sudo systemctl daemon-reload


```
- Activer et démarrer le service :

```bash
sudo systemctl enable linkedin-frontend.service
sudo systemctl start linkedin-frontend.service


```

- verifier le statut:

```bash
sudo systemctl status linkedin-frontend.service

```

## Service de build du frontend React

Pour reconstruire automatiquement l’application tous les soirs à 18h, nous avons créé un service associé à un timer.

1.  Service de build

- creer le Fichier : /etc/systemd/system/linkedin-frontend-build.service


```bash
nano /etc/systemd/system/linkedin-frontend-build.service

```

- copier le contenu suivant:

```ini

[Unit]
Description=Timer pour lancer le build du frontend React tous les soirs à 18h

[Timer]
OnCalendar=*-*-* 18:00:00
Persistent=true

[Install]
WantedBy=timers.target


```

2. Service du Timer

Ce timer déclenche le service de build tous les jours à 18h.

- creer le fichier /etc/systemd/system/linkedin-frontend-build.timer

```bash

nano /etc/systemd/system/linkedin-frontend-build.timer

```

- recharger les daemon

```bash

sudo systemctl daemon-reload
sudo systemctl enable linkedin-frontend-build.timer
sudo systemctl start linkedin-frontend-build.timer


```






























