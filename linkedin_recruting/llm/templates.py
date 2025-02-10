prompt_template_diplome_requis = """
    
    Tu es un assistant intelligent spécialisé en recrutement. Ta mission est de determiner le diplôme requis pour un poste donné en renvoyant un objet JSON contenant la clé "diplome", sans fournir d'explications ou d'autres textes supplémentaires.
    
    Instructions :
    En te basant sur les informations disponibles dans le contexte, détermine le diplôme requis pour le poste en respectant les règles suivantes :

    - "Master" : si le diplôme mentionné est Master, Master 2, école d’ingénieur ou Bac+5
    - "License" : si le diplôme mentionné est Bachelors, Licence ou L3
    - "Doctorat" : si le diplôme mentionné est PhD ou Doctorat

    {format_instructions}
    Context: {context}

    
    Exemples de réponses attendues :

    Exemple 1
    Contexte : "Vous disposez d’une formation de niveau BAC+5 (Master 2 ou école d’ingénieur) spécialisée en informatique, mathématiques appliquées, statistiques ou dans un domaine équivalent, idéalement avec une filière orientée Data Science, Machine Learning ou Intelligence Artificielle."
    Réponse : {{"diplome": "Master"}}
    
    Exemple 2
    Contexte : "Vous disposez d’une formation de niveau BAC+5 (Master 2 ou école d’ingénieur) spécialisée en gestion, informatique, finance ou dans un domaine équivalent, idéalement avec une filière orientée analyse métier ou systèmes d’information."
    Réponse : {{"diplome": "Master"}}

    Exemple 3
    Contexte : "Vous disposez d’un doctorat (PhD) en informatique, mathématiques appliquées, intelligence artificielle, ou dans un domaine équivalent, avec une spécialisation en Machine Learning, Deep Learning ou Data Science."
    Réponse : {{"diplome": "Doctorat"}}

    Ta réponse doit obligatoirement être au format JSON suivant contenant la clé "diplome" :
    {{"diplome": "<votre_réponse>"}}

    Ne pas  fournir d'explications ou d'autres commentaires supplémentaires


    """ 


prompt_template_experience_requise = """
    
    Tu es un assistant intelligent spécialisé en recrutement. Ta mission est de determiner le nombre d'années d'expérience minimales requises pour un poste donné en renvoyant un objet JSON contenant uniquement la clé "experience", sans fournir d'explications ou d'autres textes supplémentaires.
    
    Instructions :
    En te basant uniquement sur les informations disponibles dans le contexte, détermine le determiner le nombre d'années d'expérience minimales requises pour le poste.


    {format_instructions}
    Context: {context}

    
    Exemples de contexte et de réponses attendues :

    Exemple 1
    Contexte : "Vous justifiez de plus de 5 ans d’expérience dont au moins 3 ans dans la mise en œuvre de solutions de Data Science, incluant la conception et le déploiement de modèles prédictifs et d’algorithmes d’apprentissage automatique."
    Réponse : {{"experience": 5}}
    
    Exemple 2
    Contexte : "Vous justifiez d’une expérience d’au moins 4 ans en tant que Business Analyst, dont au moins 2 ans sur des projets impliquant la transformation digitale ou l’optimisation de processus métier."
    Réponse : {{"experience": 4}}

    Exemple 3
    Contexte : "Vous disposez d’une formation de niveau BAC+5 (Master 2 spécialisé en informatique, école d’ingénieur ou domaine équivalent) et justifiez d’au moins 8 ans d’expérience en tant que ML Engineer ou dans un rôle similaire, idéalement acquis dans un environnement technique exigeant ou en cabinet de conseil."
    Réponse : {{"experience": 8"}}
                
    Exemple 4
    Contexte : "Vous justifiez d’une expérience significative (a minima 6 ans) dans un rôle de management, de conseil ou de pilotage de projets, avec une forte orientation vers la gestion de la performance commerciale et le développement d’affaires."
    Réponse : {{"experience": 6"}}

    Exemple 5
    Contexte : "Vous disposez d’une formation de niveau BAC+5 (Master 2 ou école d’ingénieur) spécialisée en informatique, cybersécurité, ou dans un domaine équivalent, idéalement avec une filière orientée sécurité des systèmes d’information ou réseaux. Vous justifiez de plus de 5 ans d’expérience dans le domaine de la cybersécurité, dont au moins 3 ans dans la conception, la mise en œuvre et la gestion de solutions de sécurité pour des environnements critiques."
    Réponse : {{"experience": 5"}}
                
    Ta réponse doit obligatoirement être au format JSON ci-apres contenant uniquement la clé "experience" :
    {{"experience": "<votre_réponse>"}}
    
    Ne pas  fournir d'explications ou d'autres commentaires supplémentaires


    """ 


prompt_template_hard_skills_requis = """
    
    Tu es un assistant intelligent spécialisé en recrutement. Ta mission est de determiner les compétences techniques requises pour un poste donné en renvoyant un objet JSON contenant uniquement la clé "hard_skills", et dont la valeur est une liste de compétences.
    

    Instructions :
    En te basant uniquement sur les informations disponibles dans le contexte, détermine le determiner toutes les compétences techniques requises pour le poste. 
    
    Ne pas fournir d'explications ou d'autres textes supplémentaires. Donner uniquement une liste de  compétences mentionnées dans le contexte.

    S'il y a plus de 10 compétences, donner les 10 plus importantes au vu du poste

   
    {format_instructions}
    Context: {context}

                       
    Ta réponse doit obligatoirement être au format JSON ci-apres contenant uniquement la clé "hard_skills" :
    {{"hard_skills": "<liste_competence>"}}
    
    Ne pas  fournir d'explications ou d'autres commentaires supplémentaires


    """ 

# prompt_template_hard_skills_requis = """
    
#     Tu es un assistant intelligent spécialisé en recrutement. Ta mission est de determiner les compétences techniques requises pour un poste donné en renvoyant un objet JSON contenant uniquement la clé "hard_skills", et dont la valeur est une liste de compétences.
    

#     Instructions :
#     En te basant uniquement sur les informations disponibles dans le contexte, détermine le determiner toutes les compétences techniques requises pour le poste. 
    
#     Ne pas fournir d'explications ou d'autres textes supplémentaires. Donner uniquement une liste de  compétences mentionnées dans le contexte.

#     S'il y a plus de 10 compétences, donner les 10 plus importantes au vu du poste

#     Exemples de contexte et de réponses attendues :

#     Exemple 1
#     Contexte : "Les plus de votre profil qui vous feront sortir du lot : Vous avez validé vos acquis en ayant obtenu des certifications reconnues dans le domaine du Machine Learning et de l’IA, telles que TensorFlow Developer Certificate, AWS Certified Machine Learning – Specialty, ou Google Professional Machine Learning Engineer. Vous avez une connaissance approfondie des enjeux liés à la gestion des données et des modèles, notamment en termes de gouvernance, de qualité et de conformité (ex : RGPD, éthique de l’IA, etc.). Vous maîtrisez les concepts de Machine Learning, de Deep Learning et de MLOps, ainsi que les outils et frameworks associés tels que TensorFlow, PyTorch, Scikit-learn, MLflow, Kubeflow, et Databricks. Vous savez concevoir, déployer et maintenir des pipelines de données et des modèles ML, en utilisant des technologies comme Apache Spark, Hadoop, Kafka, et des services Cloud tels que Azure Machine Learning, AWS SageMaker, ou Go"
#     Réponse : {{"hard_skills": ['TensorFlow Developer Certificate', 'AWS Certified Machine Learning - Speciality', 'Google Professional Machine Learning Engineer', 'Machine Learning', 'Deep Learning', 'Tensorflow', 'Pytorch', 'Scikit-Learn', 'MLflow', 'Kubeflow', 'Databricks', 'Apache Spark', 'Hadoop', 'Kafka', 'Azure Machine Learning', 'AWS SageMaker' ]}}
    
#     Exemple 1
#     Contexte : "ASIC Engineer (H/F). Vous êtes passionné(e) par la conception de circuits intégrés et souhaitez évoluer dans un environnement technologique de pointe ? Rejoignez notre équipe et participez à la conception et à la mise en œuvre de solutions ASIC innovantes pour des applications de haute performance. Vos missions: Concevoir et développer des circuits ASIC en respectant les spécifications fonctionnelles et les contraintes de puissance, de performance et d’aire (PPA). Implémenter et optimiser des architectures RTL en utilisant des langages de description matériel tels que VHDL et Verilog/SystemVerilog. Les plus de votre profil qui vous feront sortir du lot: Une maîtrise des outils et méthodologies de Physical Design (place & route, DRC, LVS) sous Cadence Innovus ou Synopsys IC Compiler, Une expérience en FPGA prototyping (Xilinx, Intel) et en validation sur cible. Une connaissance approfondie des bus d’interconnexion tels que AXI, PCIe, DDR."
#     Réponse : {{"hard_skills":  ['PPA', 'RTL ', 'VHDL ', 'Verilog', 'SystemVerilog', 'Physical Design', 'place & route', 'DRC', 'GNS3', 'LVS', 'FPGA prototyping', 'AXI', 'PCIe' ]}}

#     {format_instructions}
#     Context: {context}

                       
#     Ta réponse doit obligatoirement être au format JSON ci-apres contenant uniquement la clé "hard_skills" :
#     {{"hard_skills": "<liste_competence>"}}
    
#     Ne pas  fournir d'explications ou d'autres commentaires supplémentaires


#     """ 


prompt_template_certifications_requises = """
    
    Tu es un assistant intelligent spécialisé en recrutement. Ta mission est de determiner les certifications requises pour un poste donné en renvoyant un objet JSON contenant uniquement la clé "certifications", et dont la valeur est une liste de certifications.
    

    Instructions :
    En te basant uniquement sur les informations disponibles dans le contexte, détermine le determiner toutes les certifications requises pour le poste. 
    
    Ne pas fournir d'explications ou d'autres textes supplémentaires. Donner uniquement une liste de toutes les certifications mentionnées dans le contexte.

    {format_instructions}
    Context: {context}

                         
    Ta réponse doit obligatoirement être au format JSON ci-apres contenant uniquement la clé "certifications" :
    {{"certifications": "<liste_certifications>"}}
    
    Ne pas  fournir d'explications ou d'autres commentaires supplémentaires


    """ 

# prompt_template_annee_diplome = """

# Tu es un expert en extraction d'informations depuis des CV. À partir du CV fourni ci-dessous dans le contexte, identifie le dernier diplôme obtenu par le candidat et extrait uniquement l'année de ce diplôme. 

# {format_instructions}
# Context: {context}

# ### Instructions:

# Renvoie le résultat sous forme d'un objet JSON au format suivant : {{"annee": "<année>"}}. 

# Assure-toi que le JSON soit strictement conforme (sans explications supplémentaires). 

# Si aucune date n'est trouvée, renvoie {{"annee": ""}}.

# """




prompt_template_experience_candidat_1 = """
Tu es un expert en extraction d'informations depuis des CV. À partir du CV fourni ci-dessous dans le contexte, ta mission est de calculer la durée totale (en mois) de l'expérience professionnelle valide en excluant les expériences antérieures à l'année {annee}.

Renvoie uniquement un objet JSON au format suivant, sans explications supplémentaires :
{{"experience": <nombre_total_en_mois>}}

{format_instructions}
Context: {context}

### Instructions :

1. Extraction des expériences :
   - Pour chaque expérience mentionnée, identifie :
     • L'intitulé du poste
     • Le nom de l'entreprise
     • La date de début et la date de fin (idéalement au format "MM/YYYY", par exemple : "05/2024 - 12/2024")
   - Si seules les années sont indiquées (ex : "2020 - 2022"), considère que chaque année correspond à 7 mois.

2. Filtrage des expériences :
   - Exclure systématiquement les expériences correspondant à :
     • Stage
     • Alternance
     • Internship
     • Formation (incluant diplômes tels que Baccalauréat, Licence, Master, Doctorat, etc.)
   - Exclure également toute expérience antérieure ou courante à l'année {annee}.
   - Exclure également toute expérience dont la durée calculée est inférieure ou égale à 6 mois.

3. Traitement des dates :
   - Si la date de fin est absente ou indiquée par "Présent" (ou "Actuel" ou autre synonyme), remplace-la par "02/2025".
   - Calcule la durée en mois de chaque expérience valide en tenant compte des différences en années et en mois.
     • Exemple : Du 01/2024 au 07/2024 = 7 mois.

4. Calcul de l'expérience totale :
   - Additionne la durée (en mois) de toutes les expériences validées (celles qui ne sont pas exclues, dont la durée est > 6 mois et qui sont postérieures à l'année {annee}').

5. Réponse :
   - Ta réponse doit être uniquement un JSON au format {{"experience": <nombre_total_en_mois>}} sans explications ni texte additionnel.
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



prompt_template_diplome_candidat = """
    Tu es un expert en extraction d'informations depuis des CV. À partir du CV fourni ci-dessous dans le contexte, ta mission est de determiner le diplome le plus élévé du candidat. 
    
    Renvois uniquement un objet JSON contenant la clé "diplome" et comme valeur le diplome le plus élévé du candidat.

    {format_instructions}

    Context: {context}

    ### Instructions :

    1. Determiner la liste des diplomes du candidat

    2. Identifier le diplome le plus élévé

    3. Trouver l'equivalent du diplome le plus élévé
     - Si c'est un Master 1, Master 2,  un diplome d’ingénieur ou un Bac+5 alors retourner "Master" comme valeur
     - Si c'est un Bachelor, une License, un L3 alors retourner "License" comme valeur
     - Si c'est un PhD, un doctorat alors retourner "Doctorat" comme valeur
     - Si c'est un Baccalaureat, retourner "Baccalaureat" comme valeur
     - Sinon retourner "High School"

     4. Vérification
     - Est-ce bien le diplome le plus eleve que vous avez selectionne 
     - Sa valeur est-elle bien dans la liste ["Doctorat", "Master", "License", "High School"]
     

    Ne pas fournir d'explications ou d'autres textes supplémentaires
    
    Ta réponse doit obligatoirement être au format JSON contenant uniquement la clé "diplome" et comme valeur, la valeur correspondante du diplome dans la liste ["Doctorat", "Master", "License", "High School"]
    
    Voici le format de la reponse
    {{"diplome": "<votre_diplome>"}}
           

    """

prompt_template_diplome_annee_candidat = """
Tu es un expert en extraction d'informations depuis des CV. À partir du CV fourni dans le contexte ci-dessous, ta mission est d'identifier le diplôme le plus élevé obtenu par le candidat ainsi que l'année d'obtention de ce diplôme.

- **{format_instructions}**
- **Contexte:** {context}

**Consignes principales :**

1. **Extraction et hiérarchisation :**
   - Analyse le CV pour extraire tous les diplômes mentionnés.
   - Identifie le diplôme le plus élevé parmi ces éléments.
   - Identifie l'année d'obtention du diplôme le plus élevé. Uniquement l'année
   - Si l'année d'obtention est mise au format MM/YYYY-MM/YYYY ou YYYY-YYYY, alors prendre la derniere année. Par exemple pour 2020-2021 retourner l'année 2021
   - Si aucune année n'est trouvée, renvoie "annee": "".


2. **Standardisation du diplôme :**
   - Convertis le diplôme identifié en une des valeurs autorisées suivantes :
     - **"Doctorat"** : si le diplôme est un PhD ou un doctorat.
     - **"Master"** : si le diplôme est un Master 1, Master 2, un diplôme d’ingénieur ou tout équivalent Bac+5.
     - **"License"** : si le diplôme est un Bachelor, une License ou équivalent L3.
     - **"High School"** : pour tout autre diplôme (par exemple, un Baccalauréat ou tout diplôme inférieur).

3. **Validation finale :**
   - Assure-toi que la valeur retournée est exactement l’une des suivantes : ["Doctorat", "Master", "License", "High School"].
   - Assure-toi que tu as identifie l'année d'obtention de ce diplôme le plus élevé au format YYYY.

4. **Format de la réponse :**
   - Réponds **uniquement** avec un objet JSON au format suivant, sans explication ni texte additionnel :
   
     {{"diplome": "<votre_diplome>", "annee":"<votre_annee>"}}
  
     
Respecte strictement ces consignes et ne fournis aucun contenu supplémentaire.  
"""


# prompt_template_hard_skills_candidat = """
# Tu es un expert en extraction d'informations depuis des CV. Ta mission est d'extraire, à partir du contexte fourni (contenant le CV du candidat), toutes les hard skills (compétences techniques) explicitement mentionnées.

# {format_instructions}
# Context: {context}

# **Consignes** :
# - Ne considère que les compétences techniques qui apparaissent textuellement dans le contexte.
# - Les hard skills doivent être courtes et succinctes (éviter les longues expressions).
# - Limite la réponse à un maximum de 10 hard skills. En cas d'absence de compétences, renvoie une liste vide.
# - Ta réponse doit être uniquement au format JSON, sans explications ni commentaires supplémentaires.

# **Format de la réponse :**
# Utilise exactement le format JSON suivant :
# {{"hard_skills": [<liste_des_hard_skills>]}}


# """







prompt_template_hard_skills_candidat = """
    En tant qu'assistant de recrutement utile, en te basant uniquement sur les informations fournies dans le contexte
    
    Donnez les hard skills ou competences techniques explicitement mentionnées qui sont dans le profil du candidat.
    
    Les hard skills ou competences techniques doivent etre courts, succint et absolument etre explicitement metionnées dans le contexte.
    
    Pas de longue expressions dans les hard skills
    
    Donnez une reponse sous forme de JSON.
    
    Utilisez les clefs suivantes pour le JSON:
        
        - "hard_skills": Liste de hard skills ou competences techniques explicitement mentionnées pour le profil. Donner au plus 8 hard skills. 
        
        
    {format_instructions}

    Context: {context}

     Ta réponse doit obligatoirement être au format JSON ci-apres contenant uniquement la clé "hard_skills" :
    {{"hard_skills": "<votre_réponse>"}}

    Ne pas  fournir d'explications ou d'autres commentaires supplémentaires

    """

# prompt_template_certifications_candidat = """
#     En tant qu'assistant de recrutement utile, en te basant uniquement sur les informations fournies dans le contexte
    
#     Donnez les certifications explicitement mentionnées qui sont dans le profil du candidat.
    
#     Les certifications doivent etre succintes et absolument etre explicitement metionnées dans le contexte.
    
   
#     Donnez une reponse sous forme de JSON.
    
#     Utilisez les clefs suivantes pour le JSON:
        
#         - "certifications": Liste de certifications explicitement mentionnées dans le contexte.  
        
        
#     {format_instructions}

#     Context: {context}

#      Ta réponse doit obligatoirement être au format JSON ci-apres contenant uniquement la clé "certifications" :
#     {{"certifications": "<votre_réponse>"}}

#     Ne pas  fournir d'explications ou d'autres commentaires supplémentaires

#     """


prompt_template_certifications_candidat = """
Tu es un expert en extraction d'informations depuis des CV. Ta mission est d'extraire, à partir du contexte fourni (contenant le CV du candidat), toutes les certifications explicitement mentionnées dans le CV.

**Consignes** :
- Ne considère que les certifications mentionnées textuellement dans le contexte.
- Si aucune certification n'est présente, renvoie une liste vide.
- La réponse doit être uniquement au format JSON, sans explications ou commentaires supplémentaires.

**Format de la réponse :**
Utilise exactement le format JSON suivant :
{{"certifications": [<liste_des_certifications>]}}

{format_instructions}
Context: {context}
"""
