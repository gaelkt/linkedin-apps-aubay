import re
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def nettoyer_texte(texte):
    # Enlever les retours à la ligne inutiles (les conserver uniquement entre les sections)
    texte = re.sub(r'\n+', '\n', texte)
    
    # Enlever les espaces au début et à la fin
    texte = texte.strip()

    return texte
    
def sum_extraction(text):
    # Expression régulière pour capturer le nombre d'années et de mois avec "et"
    pattern_annees_et_mois = r"\{sum_experiences_included:\s*(\d+)\s*ans?\s*et\s*(\d+)\s*mois?\}"
    pattern_mois_seul = r"\{sum_experiences_included:\s*(\d+)\s*mois?\}"

    # Tentative de correspondance avec le texte pour les années et mois
    match = re.search(pattern_annees_et_mois, text.lower())

    if match:
        years = int(match.group(1))  # Extraire le nombre d'années
        months = int(match.group(2))  # Extraire le nombre de mois
        total_months = years * 12 + months  # Calcul de la durée totale en mois
        logging.info(f"Correspondance trouvée: {years} ans et {months} mois, soit {total_months} mois au total.")
    else:
        # Si aucune correspondance pour les années et mois, on cherche uniquement les mois
        match = re.search(pattern_mois_seul, text.lower())
        if match:
            months = int(match.group(1))  # Extraire le nombre de mois
            total_months = months  # Si il n'y a pas d'années, la durée totale est le nombre de mois
            logging.info(f"Correspondance trouvée: {months} mois, soit {total_months} mois au total.")
        else:
            logging.info("Aucune correspondance trouvée.")  # Débogage
        
    return total_months if match else None