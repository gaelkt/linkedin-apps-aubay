"""Ce fichier de test permet de vérifier plusieurs aspects du fonctionnement de la classe CVProcessor, en particulier le bon enchaînement du workflow et la gestion des erreurs.
Les tests utilisent des mocks pour simuler les composants externes (comme le modèle ONNX, la génération de texte, et la sauvegarde de l'état), ce qui rend les tests rapides et isolés des dépendances externes."""

import unittest
from unittest.mock import patch, MagicMock
from src.cv_processing import CVProcessor
from src.utils import nettoyer_texte, sum_extraction
from src.prompts import prompt_resume_summary, prompt_classify_exp_part1, prompt_classify_exp_part2
from src.state_management import save_global_progress

class TestCVProcessor(unittest.TestCase):

    @patch("onnxruntime_genai.Model")
    @patch("transformers.AutoTokenizer")
    def setUp(self, MockTokenizer, MockModel):
        # Mock les dépendances externes pour ne pas appeler le modèle réel
        self.mock_model = MagicMock()
        self.mock_tokenizer = MagicMock()
        MockModel.return_value = self.mock_model
        MockTokenizer.from_pretrained.return_value = self.mock_tokenizer

        # Initialiser le processor avec un modèle mocké
        self.processor = CVProcessor(onnx_model_path="mock_model_path")

    @patch("src.cv_processing.CVProcessor.invoke_llm")
    @patch("src.cv_processing.save_global_progress")
    def test_run_workflow_success(self, MockSaveProgress, MockInvokeLLM):
        # Mock des résultats de génération pour simulateur de workflow réussi
        MockInvokeLLM.return_value = "Résumé généré avec succès"
        MockSaveProgress.return_value = None

        # Mock nettoyage du texte
        nettoyer_texte("text_cv") 

        # Mock la somme d'expériences incluses
        sum_experiences_included = 24  # 2 ans d'expérience
        MockSaveProgress.assert_called()

        # Test du workflow
        result = self.processor.run_workflow("Texte CV valide", "cv123", {"max_new_tokens": 50})
        
        # Vérifier que le résultat final est correct
        self.assertEqual(result, 24)  # On attend la somme des mois

    @patch("src.cv_processing.CVProcessor.invoke_llm")
    def test_run_workflow_error_summary(self, MockInvokeLLM):
        # Simuler un échec dans la génération du résumé
        MockInvokeLLM.return_value = None

        result = self.processor.run_workflow("Texte CV valide", "cv123", {"max_new_tokens": 50})
        
        # Vérifier le message d'erreur
        self.assertEqual(result, {"error": "Aucun résumé généré. Vérifiez le format du CV."})

    @patch("src.cv_processing.CVProcessor.invoke_llm")
    def test_run_workflow_error_classification(self, MockInvokeLLM):
        # Simuler un échec dans la classification des expériences
        MockInvokeLLM.return_value = None

        result = self.processor.run_workflow("Texte CV valide", "cv123", {"max_new_tokens": 50})
        
        # Vérifier le message d'erreur
        self.assertEqual(result, {"error": "Erreur dans la classification des expériences."})

    @patch("src.cv_processing.CVProcessor.invoke_llm")
    def test_run_workflow_error_sum_experience(self, MockInvokeLLM):
        # Simuler un échec dans le calcul de la somme des expériences
        MockInvokeLLM.return_value = "Expériences classées"

        # Simuler un résultat de somme des expériences incluses vide
        sum_experiences_included = None

        result = self.processor.run_workflow("Texte CV valide", "cv123", {"max_new_tokens": 50})
        
        # Vérifier le message d'erreur
        self.assertEqual(result, {"error": "Aucune expérience incluse ou erreur dans le calcul de la durée."})

if __name__ == "__main__":
    unittest.main()
