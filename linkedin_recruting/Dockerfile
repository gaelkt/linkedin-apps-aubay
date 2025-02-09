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
    && apt-get clean

# Installer Ollama
RUN curl -fsSL https://ollama.com/install.sh | sh

# Ajouter Ollama au PATH
ENV PATH="/root/.ollama/bin:$PATH"

# Vérifier que Ollama est bien installé
RUN ollama --version

# Définir le répertoire de travail
WORKDIR /app

# Copier les fichiers de l'application dans le conteneur
COPY . /app

# Créer un environnement virtuel et installer les dépendances Python
RUN python3 -m venv /app/venv && \
    /app/venv/bin/pip install --no-cache-dir -r requirements.txt

# Télécharger le modèle Phi4
RUN ollama pull phi4

# Configurer MySQL pour utiliser mysql_native_password pour l'utilisateur root
RUN service mysql start && \
    sleep 10 && \
    mysql -u root -e "ALTER USER 'root'@'localhost' IDENTIFIED WITH mysql_native_password BY '';" && \
    mysql -u root -e "FLUSH PRIVILEGES;"
