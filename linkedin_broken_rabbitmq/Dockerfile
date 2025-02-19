FROM rabbitmq:management

# Activer le plugin de gestion (déjà activé dans l'image `management`)
RUN rabbitmq-plugins enable --offline rabbitmq_management

# Définir les variables d'environnement pour l'utilisateur par défaut
ENV RABBITMQ_DEFAULT_USER=aubay
ENV RABBITMQ_DEFAULT_PASS=aubay
ENV RABBITMQ_DEFAULT_VHOST=/

# Exposer les ports nécessaires
EXPOSE 5672 15672

CMD ["rabbitmq-server"]


