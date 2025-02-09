import unittest
from src.utils import nettoyer_texte, sum_extraction

# Test de la fonction nettoyer_texte
class TestUtils(unittest.TestCase):
    
    def test_texte_avec_retour_ligne(self):
        texte = "Bonjour\n\nJe suis développeur.\n\n\nMerci."
        texte_attendu = "Bonjour\nJe suis développeur.\nMerci."
        self.assertEqual(nettoyer_texte(texte), texte_attendu)

    def test_texte_avec_espaces(self):
        texte = "   Bonjour, je suis développeur.   "
        texte_attendu = "Bonjour, je suis développeur."
        self.assertEqual(nettoyer_texte(texte), texte_attendu)

    def test_texte_sans_modification(self):
        texte = "Bonjour, je suis développeur."
        self.assertEqual(nettoyer_texte(texte), texte)

    def test_texte_vide(self):
        texte = ""
        texte_attendu = ""
        self.assertEqual(nettoyer_texte(texte), texte_attendu)

#   def test_texte_avec_retour_ligne_et_espaces(self):
#        texte = "   Bonjour, \n\nje suis développeur.   \n\nMerci."
#        texte_attendu = "Bonjour, \nje suis développeur. \nMerci."
#        self.assertEqual(nettoyer_texte(texte), texte_attendu)

# Test de la fonction sum_extraction
class TestSumExtraction(unittest.TestCase):

    def test_avec_annees_et_mois(self):
        texte = "{sum_experiences_included: 3 ans et 5 mois}"
        result = sum_extraction(texte)
        self.assertEqual(result, 41)  # 3 ans * 12 + 5 mois = 41 mois

    def test_avec_juste_mois(self):
        texte = "{sum_experiences_included: 7 mois}"
        result = sum_extraction(texte)
        self.assertEqual(result, 7)  # 7 mois

    def test_sans_experience(self):
        texte = "Pas d'expérience mentionnée ici."
        result = sum_extraction(texte)
        self.assertIsNone(result)  # Pas de correspondance trouvée

    def test_avec_majuscule(self):
        texte = "{sum_experiences_included: 2 ans et 8 mois}"
        result = sum_extraction(texte)
        self.assertEqual(result, 32)  # 2 ans * 12 + 8 mois = 32 mois

    def test_avec_format_incorrect(self):
        texte = "{sum_experiences_included: 2ans et 8mois}"
        result = sum_extraction(texte)
        self.assertEqual(result, 32)  # Format incorrect, mais extrcation correct

if __name__ == "__main__":
    unittest.main()