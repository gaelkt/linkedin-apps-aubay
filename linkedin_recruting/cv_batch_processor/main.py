import logging
from src.cv_processing import CVProcessor
from src.state_management import save_progress, load_progress
from src.config import config  
import pandas as pd
import os

# Désactiver les logs ONNXRuntime en réglant le niveau à 'FATAL'
os.environ['ORT_LOG_LEVEL'] = 'ERROR'  # Pour ne loguer que les erreurs

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Charger la configuration
config = config.load_config()
# Paramètres de génération et du modèle
onnx_model_path = config['model']['onnx_model_path']
generation_params = config['generation']


def run():
    # Initialiser le processeur CV
    processor = CVProcessor(onnx_model_path)

    # Chemin du fichier contenant les CV et du fichier de progression
    input_cv_file = "./data/data-brut/candidatures.csv"
    progress_file = "./data/output/progress.json"

    # Charger l'état de la progression précédente
    progress = load_progress(progress_file)
    processed_count = progress.get("processed_count", 0)

    logging.info(f"Continuing from CV #{processed_count + 1}...")

    try:
        # Lire le fichier des CV (supposons que chaque ligne est un CV)
        df_job_applys = pd.read_csv(input_cv_file)

        # Liste des CV à traiter (remplacer 'Texte_CV' par le nom réel de la colonne)
        cvs = df_job_applys["Texte_CV"].to_list()

        # Processer les CV un à un, en continuant à partir de l'index de progression
        for i, cv_text in enumerate(cvs[processed_count:], start=processed_count):
            if len(str(cv_text))<100:
                logging.info(f" CV #{i + 1} with size < 100")
                continue
            if i==2: ## to test 
                break  
            logging.info(f"Processing CV #{i + 1}")

            # Traiter le CV
            try:
                total_months = processor.run_workflow(cv_text, i, generation_params)
                logging.info(f"Total months for CV #{i + 1}: {total_months}")

                # Sauvegarder l'état de la progression après chaque CV traité
                progress["processed_count"] = i + 1
                save_progress(progress_file, progress)              
            except Exception as cv_error:
                logging.error(f"Error processing CV #{i + 1}: {cv_error}")
                # Optionnel : sauvegarder l'erreur pour chaque CV dans un log ou un fichier de résultat
                break
                #continue  # Passe au CV suivant si une erreur se produit pour un CV

        logging.info("All CVs processed successfully.")
        #del processor
    except Exception as e:
        logging.error(f"Error during processing: {e}")

if __name__ == "__main__":
    run()