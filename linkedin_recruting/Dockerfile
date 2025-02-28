# Utiliser une image Ubuntu de base
FROM ubuntu:latest

# Mettre à jour et installer les outils nécessaires
RUN apt-get update && apt-get install -y \
    python3-pip \
    python3-venv \
    python3-dev \
    mysql-server \
    libmysqlclient-dev \
    build-essential \
    libssl-dev \
    curl \
    rabbitmq-server \
    && apt-get clean

# Activer le plugin de gestion de RabbitMQ
RUN rabbitmq-plugins enable --offline rabbitmq_management
# Définir les variables d'environnement pour RabbitMQ
ENV RABBITMQ_DEFAULT_USER=aubay
ENV RABBITMQ_DEFAULT_PASS=aubay
ENV RABBITMQ_DEFAULT_VHOST=/

# Définir le répertoire de travail
WORKDIR /app

# Copier les fichiers de l'application dans le conteneur
COPY . /app

# Créer un environnement virtuel et installer les dépendances Python
RUN python3 -m venv /app/venv && \
    /app/venv/bin/pip install --no-cache-dir -r requirements.txt


# Configurer MySQL pour utiliser mysql_native_password pour l'utilisateur root
RUN service mysql start && \
    sleep 20 && \
    mysql -u root -e "ALTER USER 'root'@'localhost' IDENTIFIED WITH mysql_native_password BY '';" && \
    mysql -u root -e "FLUSH PRIVILEGES;"


EXPOSE 8081 3306 5672 15672

CMD service mysql start && \
    sleep 20 && \
    rabbitmq-server -detached && \
    sleep 20 && \
    /app/venv/bin/celery -A celery_app worker --loglevel=info -Q aubay & \
    sleep 20 && \
    /app/venv/bin/python3 main.py
