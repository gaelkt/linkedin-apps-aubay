from setuptools import setup, find_packages
from pathlib import Path

# Lire les dépendances depuis le fichier requirements.txt
with open(Path(__file__).parent / 'requirements.txt') as f:
    required = f.read().splitlines()

setup(
    name="cv-processing-project",
    version="0.1",
    description="Un projet pour traiter et analyser des CV avec le modèle Phi3.5 ONNX",
    packages=find_packages(),
    install_requires= required,
    entry_points={
        'console_scripts': [
            'cv-process = src.main:main',  # Exemple d'entrée pour une commande CLI
        ],
    },
    author='Abdelaziz Jaddi',
    author_email='ajaddi@aubay.com',    
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
)
