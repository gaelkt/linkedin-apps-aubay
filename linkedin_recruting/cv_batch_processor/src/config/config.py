import yaml
import os

# Fonction pour charger la configuration à partir du fichier config.yaml
def load_config(config_path='config.yaml'):
    """
    Charge la configuration depuis un fichier YAML.
    
    :param config_path: Chemin vers le fichier de configuration (par défaut 'config.yaml').
    :return: Un dictionnaire contenant les paramètres de configuration.
    """
    config_path = os.path.join(os.path.dirname(__file__), 'config.yaml')
    if not os.path.exists(config_path):
        raise FileNotFoundError(f"Le fichier de configuration '{config_path}' est introuvable.")
    
    with open(config_path, 'r') as file:
        config = yaml.safe_load(file)
    
    return config