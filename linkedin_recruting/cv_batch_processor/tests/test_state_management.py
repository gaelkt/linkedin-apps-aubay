import unittest
from unittest import mock
import os
import json
from src.state_management import save_progress, load_progress, save_global_progress

class TestStateManagement(unittest.TestCase):

    @mock.patch("builtins.open", new_callable=mock.mock_open)
    @mock.patch("os.path.exists", return_value=False)  # Simuler l'absence de fichier
    def test_save_progress(self, mock_exists, mock_open):
        """Test de la fonction save_progress"""
        progress_data = {"cv_id": {"status": "in_progress", "steps": {}}}
        file_path = "./data/output/progress.json"

        # Appel de la fonction
        save_progress(file_path, progress_data)

        # Vérifier que open a été appelé avec le bon chemin et en mode écriture
        mock_open.assert_called_once_with(file_path, 'w')

        # Vérifier que json.dump() a bien été appelé pour écrire les données
        mock_open.return_value.write.assert_called_once_with(json.dumps(progress_data))

    @mock.patch("builtins.open", new_callable=mock.mock_open, read_data=json.dumps({"cv_id": {"status": "in_progress", "steps": {}}}))
    @mock.patch("os.path.exists", return_value=True)  # Simuler que le fichier existe
    def test_load_progress(self, mock_exists, mock_open):
        """Test de la fonction load_progress"""
        file_path = "./data/output/progress.json"

        # Appel de la fonction
        result = load_progress(file_path)

        # Vérifier que le fichier a bien été ouvert en mode lecture
        mock_open.assert_called_once_with(file_path, 'r')

        # Vérifier que la donnée retournée correspond à celle contenue dans le fichier JSON
        self.assertEqual(result, {"cv_id": {"status": "in_progress", "steps": {}}})

    @mock.patch("builtins.open", new_callable=mock.mock_open)
    @mock.patch("os.path.exists", return_value=True)  # Simuler que le fichier existe
    @mock.patch("json.load", return_value={})  # Simuler un fichier vide ou malformé
    def test_save_global_progress_new_cv(self, mock_json_load, mock_exists, mock_open):
        """Test de la fonction save_global_progress pour un nouveau CV"""
        # Données à tester
        cv_id = "cv_001"
        step = "clean text"
        status = "completed"
        result = "Texte nettoyé"
        
        global_progress_file = "./data/output/global_progress.json"

        # Appel de la fonction
        save_global_progress(cv_id, step, status, result)

        # Vérifier que le fichier global_progress.json a bien été ouvert en mode écriture
        mock_open.assert_called_once_with(global_progress_file, 'w', encoding='utf-8')

        # Vérifier que json.dump a bien été appelé avec un dictionnaire mis à jour
        updated_progress = {
            cv_id: {
                "status": "in_progress",
                "steps": {
                    step: {"status": status, "result": result}
                },
                "last_update": mock.ANY  # On ne vérifie pas la date exacte ici, juste qu'elle existe
            }
        }
        mock_open.return_value.write.assert_called_once_with(json.dumps(updated_progress, indent=4, ensure_ascii=False))

    @mock.patch("builtins.open", new_callable=mock.mock_open, read_data=json.dumps({"cv_001": {"status": "in_progress", "steps": {}}}))
    @mock.patch("os.path.exists", return_value=True)
    def test_save_global_progress_existing_cv(self, mock_exists, mock_open):
        """Test de la fonction save_global_progress pour un CV existant"""
        cv_id = "cv_001"
        step = "classification"
        status = "completed"
        result = "Classification terminée"
        
        global_progress_file = "./data/output/global_progress.json"

        # Appel de la fonction
        save_global_progress(cv_id, step, status, result)

        # Vérifier que json.dump() a bien été appelé pour mettre à jour l'état du CV
        updated_progress = {
            cv_id: {
                "status": "in_progress",
                "steps": {
                    step: {"status": status, "result": result}
                },
                "last_update": mock.ANY
            }
        }

        mock_open.return_value.write.assert_called_once_with(json.dumps(updated_progress, indent=4, ensure_ascii=False))

    @mock.patch("builtins.open", new_callable=mock.mock_open)
    @mock.patch("os.path.exists", return_value=False)
    def test_save_global_progress_create_directory(self, mock_exists, mock_open):
        """Test de la création du répertoire pour save_global_progress"""
        cv_id = "cv_001"
        step = "clean text"
        status = "completed"
        result = "Texte nettoyé"
        
        global_progress_file = "./data/output/global_progress.json"

        # Appel de la fonction
        save_global_progress(cv_id, step, status, result)

        # Vérifier que le répertoire a bien été créé
        mock_exists.assert_called_with(os.path.dirname(global_progress_file))

        # Vérifier que json.dump() a bien été appelé pour écrire les données dans le fichier
        mock_open.return_value.write.assert_called_once()

if __name__ == "__main__":
    unittest.main()