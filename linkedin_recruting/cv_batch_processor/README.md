# CV Processing Project

## Description

Ce projet permet de traiter et d'analyser des CV en utilisant le modèle gen ai Phi3.5 ONNX. L'objectif est d'extraire des informations utiles, comme la durée des expériences professionnelles, les compétences, et plus encore. Le traitement des CV se fait de manière automatisée et permet de gérer un grand nombre de fichiers via un pipeline par lots.

### Fonctionnalités principales :
- **Traitement par lots de CV** : Analyser plusieurs CV à la fois à partir de fichiers CSV.
- **Nettoyage et validation des CV** : Vérification des formats et nettoyage des textes des CV avant analyse.
- **Extraction d'informations** : Extraction de données comme la durée des expériences professionnelles, les compétences, etc.
- **Gestion de la progression** : Sauvegarde de la progression du traitement pour éviter les erreurs et permettre la reprise du processus en cas d’interruption.

## Structure du dépôt

La structure du projet est organisée de manière modulaire pour faciliter son évolution et son utilisation.

```
cv-processing-project/
├── src/                         # Code source du projet
│   ├── __init__.py
│   ├── utils.py                 # Fonctions utilitaires
│   ├── prompts.py               # Contient les prompts pour le modèle
│   ├── cv_processing.py         # Traitement des CV
│   ├── state_management.py      # Gestion de l'état du traitement
│   └── config/                  # Fichiers de configuration
│       ├── __init__.py
│       ├── config.py            # Configuration Python
│       └── config.yaml          # Configuration YAML
├── tests/                       # Dossier pour les tests
│   ├── __init__.py
│   ├── test_utils.py            # Tests des fonctions utilitaires
│   ├── test_cv_processing.py    # Tests du traitement des CV
│   ├── test_state_management.py # Tests de la gestion de l'état
│   └── test_model.py            # Tests de l'interaction avec le modèle
├── models/                      # Modèles ONNX
├── data/                        # Données d'entrée et de sortie
├── main.py                      # Point d'entrée du projet
├── requirements.txt             # Dépendances du projet
├── setup.py                     # Installation du projet
├── README.md                    # Documentation du projet
├── .gitignore                   # Fichiers à ignorer par Git
```

## Installation

1. Clonez le projet :

```bash
git clone https://github.com/votre-repository/cv-processing-project.git
```

2. Installez les dépendances :

```bash
pip install -r requirements.txt
```

## Utilisation

### Télécharger le modèle Phi3.5

1. Vous devez télécharger le modèle Phi3.5 en ONNX depuis le dépôt Microsoft. Suivez le tutoriel officiel pour cela :
   
   [Télécharger le modèle Phi3.5 - Tutoriel Microsoft](https://github.com/microsoft/onnxruntime-genai/blob/main/examples/python/phi-3-tutorial.md)

2. Une fois téléchargé, placez le modèle dans le dossier `models/`.

### Configurer le chemin du modèle dans `config.yaml`

3. Après avoir téléchargé le modèle, ajoutez le chemin d'accès à ce modèle dans le fichier de configuration `config/config.yaml` sous la clé `onnx_model_path`. Le contenu de `config.yaml` devrait ressembler à ceci :

```yaml
# Exemple de configuration pour Phi3.5
# Paramètres du modèle
model:
  onnx_model_path: "./models/Phi-3.5-mini-instruct-onnx"
```

### Préparer les données

1. Placez vos fichiers de CV (en format CSV) dans le dossier `data/raw/`. Assurez-vous que la colonne contenant les textes des CV est nommée `Texte_CV` (ou ajustez le code en conséquence).

### Lancer le traitement
 
Pour commencer à traiter les CV, exécutez le script `main.py` :

```bash
python main.py
```

### Fichiers de sortie

Les résultats du traitement seront stockés dans le dossier `data/output/` sous forme de fichiers JSON, contenant les informations extraites des CV (durée des expériences professionnelles, compétences, etc.).

## Configuration

Les paramètres du modèle et du traitement sont définis dans les fichiers `config/config.py` et `config/config.yaml`. Vous pouvez ajuster ces fichiers pour modifier les comportements du projet, comme les chemins d'accès ou les paramètres du modèle.