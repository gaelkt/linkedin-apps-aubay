import logging
import onnxruntime_genai as og
from transformers import AutoTokenizer
from .utils import nettoyer_texte, sum_extraction
from .prompts import prompt_resume_summary, prompt_classify_exp_part1, prompt_classify_exp_part2
from .state_management import save_global_progress


logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


class CVProcessor:
    def __init__(self, onnx_model_path):
        logging.info('Loading model and tokenizer...')
        self.model = og.Model(onnx_model_path)
        self.tokenizer = AutoTokenizer.from_pretrained(onnx_model_path)

    def invoke_llm(self, prompt: str, generation_params: dict):
        """ Fonction pour générer la réponse du modèle """
        try:
            messages = [{"role": "user", "content": prompt}]
            prompt_auto = self.tokenizer.apply_chat_template(messages, tokenize=False, add_generation_prompt=True)

            # Tokenisation et génération
            input_tokens = self.tokenizer.encode(prompt_auto, add_special_tokens=False)
            logging.info(f"Tokenisation du prompt, longueur {len(input_tokens)}")

            search_options = {**generation_params, 'max_length': len(input_tokens) + generation_params['max_new_tokens']}
            del search_options['max_new_tokens']

            params = og.GeneratorParams(self.model)
            params.set_search_options(**search_options)
            params.input_ids = input_tokens
            generator = og.Generator(self.model, params)
            logging.info("Generator created")

            output_tokens = []
            logging.info("Running generation loop ...")
            while not generator.is_done():
                generator.compute_logits()
                generator.generate_next_token()
                output_tokens.append(generator.get_next_tokens()[0])

            output_text = self.tokenizer.decode(output_tokens, skip_special_tokens=True)
            logging.info("Génération terminée.")
            return output_text
        except Exception as e:
            logging.error(f"Error during inference: {e}")
            return "Error during inference"
    
    def run_workflow(self, text_cv: str, cv_id: str, generation_params: dict):
        """
        Workflow principal pour analyser et évaluer les expériences professionnelles d'un CV.
        
        Étapes :
        1. Nettoyer le texte du CV.
        2. Générer un résumé des expériences professionnelles.
        3. Classifier les expériences en fonction de critères spécifiques (incluses ou exclues).
        4. Calculer la somme totale des durées des expériences incluses.
        
        :param text_cv: Texte du CV à analyser.
        :return: La somme des durées des expériences incluses en mois, ou un message d'erreur en cas d'échec.
        """
        try:
            logging.info("Démarrage du workflow d'évaluation des expériences professionnelles.")

            # Étape 1 : Nettoyage du texte du CV
            logging.info("Étape 1 : Nettoyage du texte du CV.")
            cv_text_clean = nettoyer_texte(str(text_cv))
            save_global_progress(cv_id, "clean text", "completed")

            # Étape 2 : Génération du résumé des expériences professionnelles
            logging.info("Étape 2 : Génération du résumé des expériences professionnelles.")
            prompt_user_cv_text = prompt_resume_summary.format(cv_text=cv_text_clean)
            resume_summary = self.invoke_llm(prompt=prompt_user_cv_text, generation_params = generation_params)
            logging.info("Résumé des expériences professionnelles généré.")
            save_global_progress(cv_id, "resume summary", "completed", result=resume_summary)

            # Vérification de la validité du résumé
            if not resume_summary:
                logging.error("Aucun résumé généré à partir du CV.")
                return {"error": "Aucun résumé généré. Vérifiez le format du CV."}

            # Étape 3 : Classification des expériences professionnelles
            logging.info("Étape 3 : Classification des expériences professionnelles.")
            prompt_user_classify_exp = prompt_classify_exp_part1.format(resume_summary =resume_summary)+prompt_classify_exp_part2
            results_classif = self.invoke_llm(prompt_user_classify_exp, generation_params)

            if results_classif is None:
                logging.error("Erreur dans la classification des expériences professionnelles.")
                save_global_progress(cv_id, "classification", "failed")
                return {"error": "Erreur dans la classification des expériences."}
            
            save_global_progress(cv_id, "classification", "completed", result = results_classif)

            logging.info("Classification des expériences terminée.")

            # Étape 4 : Extraction et calcul de la somme des durées des expériences incluses
            logging.info("Étape 4 : Extraction et calcul de la somme des durées des expériences incluses.")
            sum_experiences_included = sum_extraction(results_classif)
            save_global_progress(cv_id, "sum_experiences_included", "completed", result=sum_experiences_included)

            # Vérification des résultats
            if sum_experiences_included is None:
                logging.error("Aucune expérience incluse trouvée ou erreur dans le calcul de la durée.")
                return {"error": "Aucune expérience incluse ou erreur dans le calcul de la durée."}

            logging.info(f"Sommation des durées des expériences incluses : {sum_experiences_included} mois.")
            return sum_experiences_included

        except Exception as e:
            logging.error(f"Erreur lors de l'exécution du workflow : {e}")
            return {"error": "Erreur lors de l'exécution du workflow."}