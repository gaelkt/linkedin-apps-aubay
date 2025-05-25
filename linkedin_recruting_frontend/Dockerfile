# Étape 1 : build
FROM node:22-alpine AS builder
WORKDIR /app

# On copie package.json et yarn.lock en premier pour profiter du cache Docker
COPY package.json yarn.lock ./
RUN yarn install --frozen-lockfile

# On copie le reste du code et on build
COPY . .
RUN yarn build

# Étape 2 : serveur statique
FROM nginx:stable-alpine
# On supprime la config par défaut pour la remplacer
RUN rm -rf /usr/share/nginx/html/*
# On copie le build Vite dans le dossier servi par Nginx
COPY --from=builder /app/dist /usr/share/nginx/html

# Optionnel : configuration custom (pour history mode React Router, etc.)
COPY nginx.conf /etc/nginx/conf.d/default.conf

EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]




