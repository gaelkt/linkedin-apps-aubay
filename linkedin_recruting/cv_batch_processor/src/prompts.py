prompt_resume_summary = """
L'objectif de cette tâche est d'analyser et resumer strictement que les expériences professionnelles d'un candidat à partir de CV du Candidat. Pour chaque expérience professionnelle (en excluant les formations), veuillez fournir une présentation concise et structurée en suivant le format et l'ordre spécifié ci-dessous.

### CV du Candidat :
""
{cv_text}
""
---

### Instructions analyser et resumer les expériences professionnelles (en excluant les formations):
Pour chaque experience professionnelle:      
- Format de la réponse pour chaque expérience :
   - Type de poste : Titre de poste.
   - Type de poste : [Stage / Formation /Alternance / Freelance / Projet /CDI / CDD].
   - Durée : Dates de début et de fin de l’expérience.

- Évitez toute répétition des instructions précédentes, commentaires supplémentaires ou d'informations personnelles.
"""

prompt_classify_exp_part1 = """ L'objectif est de classifier les expériences professionnelles d'un candidat à partir de son résumé ci-dessous, en excluant les expériences de stage, formation, d'alternance, ainsi que celles ayant une durée inférieure à 8 mois. Ensuite, vous devrez calculer la somme des durées des expériences professionnelles retenues. Veuillez suivre les instructions suivantes :

### Résumé dexpériences professionnelles:
""
{resume_summary}
""
"""

prompt_classify_exp_part2 = """### 1. Critères d'Exclusion :
Exclure toute expérience qui correspond à l'une des catégories suivantes, indépendamment de sa durée :
- Stage, Alternance, Formation, Mission Freelance.
- Projet personnel ou projet académique.
- Durée inférieure à 8 mois.

### 2. Critères d'Inclusion :
Inclure toute expérience qui :
- Ne correspond à aucune des catégories exclues.
- A une durée supérieure à 8 mois.

### 3. Format de Réponse attendu pour chaque expérience :
- Type de poste : Indiquez le type d’expérience (Stage, Alternance, Formation, Freelance, Projet, CDI, CDD, etc.).
- Durée : Précisez les dates de début et de fin (format : Début – Fin).
- Statut : Indiquez si l’expérience est Incluse ou Exclue en fonction des critères d'inclusion et d'exclusion.

### 4. Calcul de la Somme des Durées des Expériences Incluses :
- Additionnez la durée des expériences incluses (en mois).
- Format attendu : `{sum_experiences_included: X mois}`.
- Si aucune expérience n'est incluse, retournez : `{sum_experiences_included: 0 mois}`.

### 5. Vérification Finale :
1. Assurez-vous que chaque expérience a été correctement analysée selon les critères d'exclusion et d'inclusion.
2. Vérifiez que la durée a bien été prise en compte pour déterminer l’inclusion ou l’exclusion.
3. Recalculez la somme des durées des expériences incluses et validez le format : `{sum_experiences_included: X mois}`.
"""

prompt_classify_exp_part2_v1 = """
### Instructions pour l’analyse des statuts des expériences:
1. Classifié chaque expérience :
   - Si l'expérience est un stage, une alternance, une formation ou une mission freelance, quelle que soit sa durée :  
     - Exclure cette expérience.
   - Si l'expérience est un projet formation, quelle que soit sa durée :  
     - Exclure cette expérience.
   - Si l'expérience est un projet personnel ou académique, quelle que soit sa durée :  
     - Exclure cette expérience.
   - Si l'expérience a une durée inférieure à 8 mois :
      - Exclure cette expérience.
   - Si l'expérience n'est pas un stage, une formation, une alternance, une mission freelance, un projet personnel ou académique et sa durée est supérieur à 8 mois:  
      - Inclure cette expérience.

2. Format de la réponse pour chaque expérience :
   - Type de poste : [Stage / Alternance / Formation/ Freelance / Projet /CDI / CDD]. Utilisez l'analyse de l'étape 1 pour indiquer si l'expérience est un stage, une formation, une alternance, une mission freelance, un projet personnel ou académique, un CDD, un CDI, ou tout autre type de contrat.
   - Durée : Dates de début et de fin de l’expérience.
   - Statut : Utilisez l'analyse de l'étape 1 pour déterminer si l'expérience est Incluse ou Exclue. Rappel: Une expérience est "Incluse" si elle n'est pas un stage, une formation, une alternance, une mission freelance, un projet personnel ou académique, et si sa durée est supérieur a 8 mois. Si la durée est inférieure à 8 mois, la réponse sera "Exclue"

3. Calcul de la somme des durées des expériences incluses :
   - Objectif : Après avoir analysé et classé chaque expérience professionnelle (en tenant compte des critères d'inclusion/exclusion), vous devez calculer la somme totale des durées des expériences incluses uniquement.
   - Méthode :
     I. Additionner les durées des expériences incluses : Seules les expériences ayant un statut "Incluse" doivent être prises en compte. Additionnez la durée de chaque expérience pertinente (exprimée en mois).
   - Format attendu : {sum_experiences_included: X mois}
   - Cas d'absence d'expériences incluses :
     - Si aucune expérience n'est incluse (c'est-à-dire si la somme des durées des expériences incluses est de 0), renvoyez la valeur suivante : {sum_experiences_included: 0 mois}

### Instruction finale :
- Vérification des critères d'inclusion/exclusion :
   - L’expérience est-elle un stage, une alternance, une formation, une mission freelance, un projet personnel ou académique ? (Si oui, exclure l'expérience, peu importe sa durée).
   - La durée de l’expérience a-t-elle été correctement prise en compte pour déterminer son inclusion/exclusion ? (Si la durée est inférieure à 8 mois, exclure).

-Vérification et recalcul (si besoin) de la somme des durées des expériences "incluses" :
   - Additionnez les durées des expériences marquées comme "incluses".
   - fournissez une validation pour la somme des durées des expériences incluses (si applicable), en suivant le format: {sum_experiences_included: X mois}.

- Évitez toute répétition des instructions précédentes, commentaires supplémentaires ou d'informations personnelles. La réponse doit être concise, conforme aux critères, structure et formats définis.     
"""
