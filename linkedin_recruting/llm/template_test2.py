# -*- coding: utf-8 -*-
"""
Created on Sun Feb  9 21:03:14 2025

@author: gaelk
"""

prompt_template_experience_candidat_1 = """
Tu es un expert en extraction d'informations depuis des CV. Ta mission est de calculer, en mois, la durée totale de l'expérience professionnelle pertinente d'un candidat, en te basant sur le CV fourni dans le contexte.

**Critères de filtrage :**
1. **Date :**
   - Exclure toute expérience dont la période (début ou fin) est antérieure ou égale à l'année {annee}.
   
2. **Type d'expérience :**
   - Exclure systématiquement les expériences correspondant à :
     - Stage
     - Alternance
     - Internship
     - Formations (incluant les diplômes tels que Baccalauréat, Licence, Master, Doctorat, etc.)

3. **Durée :**
   - Exclure toute expérience dont la durée est inférieure ou égale à 6 mois.

**Calcul :**
- Additionne la durée (en mois) de toutes les expériences qui ne sont pas exclues.

**Sortie :**
- Réponds uniquement par un objet JSON, sans aucun commentaire ni explication.
- Le JSON doit contenir une unique clé "experience" avec pour valeur un entier représentant la durée totale en mois.


{format_instructions}
Context: {context}



"""
prompt_template_experience_candidat_0 = """
Tu es un expert en extraction d'informations depuis des CV. À partir du CV fourni ci-dessous dans le contexte, ta mission est de calculer la durée totale (en mois) de l'expérience professionnelle valide.

Renvois uniquement un objet JSON contenant la clé "experience" et comme valeur un nombre entier representant la duree totale de l'experience professionnelle du candidat.
{format_instructions}
Context: {context}

### Instructions pour le calcul:
    
 1. Filtrage selon la date
 Exclure toute expérience antérieure ou courante à l'année {annee}.

 2. Filtrage selon le type d'expériences :
   - Exclure systématiquement les expériences correspondant à des:
     • Stage
     • Alternance
     • Internship
     • Formations (incluant diplômes tels que Baccalauréat, Licence, Master, Doctorat, etc.)
     
 3. Filtrage selon la duree :
   - Exclure également toute expérience dont la durée est inférieure ou égale à 6 mois.



4. Calcul de l'expérience totale :
   - Additionne la durée (en mois) de toutes les expériences non exclues .

5. Réponse :
 Ne fournis pas  d'explications supplémentaires. Ta réponse doit obligatoirement être au format JSON contenant uniquement la clé "experience" et comme valeur un nombre entier representant la duree de l'experience en mois.
 
 Voici le format de la reponse
 {{"experience": "<votre_réponse>"}}
"""

prompt_template_experience_candidat_2 = """
   Tu es un expert en extraction d'informations depuis des CV. À partir du CV fourni ci-dessous dans le contexte, ta mission est de calculer la duree de l'expérience professionnelle valide du candidat en excluant les expériences antérieures à l'année {annee}..
    Renvois uniquement un objet JSON contenant la clé "experience" et comme valeur un nombre entier representant la duree totale de l'experience professionnelle du candidat.

            
    {format_instructions}
    Context: {context}
    
    ### Instructions pour le calcul :
    En te basant uniquement sur les informations disponibles dans le contexte, extrait la date de debut et de fin de chaque experience, l'intitulé du poste et le nom de la compagnie. Exclure les periode de stages, d'alternances et de formation.
    

    1. Type de poste :
    - S'il s'agit d'un stage, d'une alternance, d'un diplome (comme par exemple Baccalaureat, License, Master ou Doctorat) ou d'une autre formation, exclure systematiquement cette experience du calcul.

    2. Extraction des dates de début et de fin de chaque experience :
    Pour chaque expérience, identifiez la date de début et la date de fin au format suivant :
    - MOIS/ANNEE
    - Exemple de format : 05/2024 - 12/2024.
    - Si la date de fin n'est pas mentionée ou si c'est ecrit "Present" a la place de la date de fin, la remplacer par "02/2025"
    
    3. Exclusion des experiences trop anciennes
    
    - Si la periode de l'expérience est antérieure ou courante à l'année {annee} alors la maqrquer comme non valide.
    


    3. Calcul de la durée en mois :
    - Prenez en compte uniquement les années et les mois pour calculer la durée de chaque expérience.
    - Exemple : Si la date de début est janvier 2024 et la date de fin est juin 2024, la durée est de 6 mois.
    - Si les mois de debut et de fin ne sont pas mentionés, alors calculer la durée année a année. Par exemple la durée 2020-2022 correspond a une durée de 24 mois, 2023-2024 correspond a une durée de 12 mois
    - Si la duree est <= 6 mois marquer le poste comme non valide.
    - Si la duree est > à 6 mois, marquer le poste comme valide
    
    
    4. Vérification des critères d'analyse :
        Avant de finaliser le calcul, assurez-vous que les critères suivants ont été respectés pour chaque poste :

  - Le poste est-il un stage, une alternance, un diplome ou une formation ? (Si oui, le marquer comme non valide.)
  - La durée est-elle inférieure à 6 mois ? (Si oui, marquer le poste comme non valide.)
  - Les dates de début et de fin ont-elles été extraites et sont-elles correctes ?
  - L'expérience est-elle antérieure ou courante à l'année {annee}. Si oui la marquer comme non valide
  - La durée a-t-elle été calculée correctement en mois ?
    
    
    5. Calcul de la somme des durées des expériences:
    Après avoir extrait chaque expérience, calculez la somme totale de la durée des expériences valides. 

    Ne pas fournir d'explications ou d'autres textes supplémentaires
    
    Ta réponse doit obligatoirement être au format JSON contenant uniquement la clé "experience" et comme valeur un nombre entier representant la duree de l'experience pertinente.
    
    Voici le format de la reponse
    {{"experience": "<votre_réponse>"}}
    
                          
    """ 



prompt_template_diplome_annee_candidat = """
Tu es un expert en extraction d'informations depuis des CV. À partir du CV fourni dans le contexte ci-dessous, ta mission est d'identifier l'année d'obtention du diplôme le plus haut.

- **{format_instructions}**
- **Contexte:** {context}



4. **Format de la réponse :**
   - Réponds **uniquement** avec un objet JSON au format suivant, sans explication ni texte additionnel :
   
     {{"annee":"<votre_annee>"}}
  
     
Respecte strictement ces consignes et ne fournis aucun contenu supplémentaire.  
"""

