# Documentation des Services Systemd pour le Déploiement et la Maintenance

Ce document décrit la configuration des services systemd mis en place pour :

- Lancer le backend FastAPI dans un container Docker.
- Lancer le frontend React en mode preview via Yarn.
- Rebuild automatiquement le frontend React tous les soirs à 18h.

---

## 1. Service pour le Backend FastAPI (Docker)

Ce service se charge de lancer le container Docker au démarrage de la machine.

**Fichier :** `/etc/systemd/system/jobs.service`

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

sudo systemctl daemon-reload
