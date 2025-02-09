import os
import json
import logging
from datetime import datetime

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def save_progress(file_path, progress_data):
    """ Sauvegarde de l'état de progression """
    try:
        with open(file_path, 'w') as f:
            json.dump(progress_data, f)
    except Exception as e:
        print(f"Erreur lors de la sauvegarde de la progression : {e}")

def load_progress(file_path):
    """ Chargement de l'état de progression depuis un fichier """
    try:
        if os.path.exists(file_path):
            with open(file_path, 'r') as f:
                return json.load(f)
        return {}
    except Exception as e:
        print(f"Erreur lors du chargement de la progression : {e}")
        return {}
    
def save_global_progress(cv_id, step, status, result=None):
    """
    Sauvegarde la progression globale du traitement de tous les CV dans un fichier JSON centralisé.
    Seules les étapes modifiées sont sauvegardées pour éviter de réécrire toutes les étapes.
    """
    global_progress_file = "./data/output/global_progress.json"
    
    # Vérifier si le dossier de sortie existe, sinon le créer
    output_dir = os.path.dirname(global_progress_file)
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    # Charger l'état actuel du fichier s'il existe, sinon initialiser un dictionnaire vide
    global_progress = {}
    if os.path.exists(global_progress_file):
        try:
            with open(global_progress_file, 'r', encoding='utf-8') as file:
                global_progress = json.load(file)
            logging.info(f"Fichier de progression chargé avec succès.")
        except (json.JSONDecodeError, IOError) as e:
            logging.error(f"Erreur lors du chargement du fichier de progression : {e}")
            global_progress = {}  # Si erreur de lecture, on commence avec un fichier vide

    # Si le CV n'existe pas encore dans le fichier global, l'ajouter avec un état de départ
    if cv_id not in global_progress:
        global_progress[cv_id] = {
            "status": "in_progress", 
            "steps": {},
            "last_update": ""
        }
    
    # Mettre à jour l'étape en cours
    global_progress[cv_id]['steps'][step] = {
        "status": status,
        "result": result
    }

    # Mettre à jour la date et heure de la dernière modification avec un timestamp formaté
    global_progress[cv_id]['last_update'] = datetime.now().strftime("%Y-%m-%dT%H:%M:%S")

    # Sauvegarder uniquement le CV modifié
    try:
        with open(global_progress_file, 'w', encoding='utf-8') as file:
            json.dump(global_progress, file, indent=4, ensure_ascii=False)  # Assure que les caractères spéciaux sont sauvegardés correctement
        logging.info(f"Progression globale sauvegardée pour cv_id : {cv_id+1} à l'étape {step}.")
    except (IOError, json.JSONDecodeError) as e:
        logging.error(f"Erreur lors de la sauvegarde du fichier de progression : {e}")