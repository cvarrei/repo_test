# Application ImmoPred - Prédiction de la Valeur Foncière en France

![Alt text](assets/logo.png) 

Venez l'essayer sur : https://immopred-app.onrender.com/

## Contexte

L'Application ImmoPred est une application développée pour explorer les données de ventes immobilières en France entre 2018 et 2021. Ces données ont été enrichies avec des données en libre accès (OPENDATA) pour créer un modèle de prédiction de la valeur foncière de biens immobiliers en fonction de certaines informations clés. Tout le développement de l'application a été réalisé en Python en utilisant les packages listés dans le fichier `requirements.txt`.

## Fonctionnalités

- **Exploration de Données Immobilières** : L'application vous permet d'explorer les données de ventes immobilières en France, offrant des informations précieuses sur les tendances du marché immobilier.

- **Modèle de Prédiction** : Utilisez notre modèle de prédiction pour estimer la valeur foncière de n'importe quel bien immobilier en fournissant quelques informations essentielles. Obtenez des estimations précises pour vos futurs investissements ou l'évaluation de biens immobiliers existants.

- **Tableaux de Bord Graphiques** : L'interface Dash de l'application propose une variété de tableaux de bord graphiques (KPI) pour visualiser les données clés du marché immobilier en France. Suivez les tendances des prix, l'évolution des quartiers, les taux de location et bien plus encore.

## Comment Utiliser l'Application

1. **Configuration de l'Environnement** :
   - Assurez-vous d'avoir Python installé sur votre système.
   - Utilisez `pip` pour installer les dépendances en exécutant `pip install -r requirements.txt`.

2. **Lancement de l'Application** :
   
   - [En LOCAL] Créer un environnement virtuel et s'assurer que les librairies ont bien été installées.
   - [En LOCAL] Activer l'environnement virtuel et se positioner dans le dossier de l'application.
   - [En LOCAL] Exécutez l'application en utilisant `python app_v4.py` en ligne de commande en s'assurant que le fichier de l'application se trouve bien dans un dossier similaire à celui sur Github.
   - [En LOCAL] Accédez à l'application en ouvrant un navigateur web et en visitant l'URL `http://127.0.0.1:8050`.
   
   - [En LIGNE] L'application a été déployé sur Render.com:  https://immopred-app.onrender.com/

4. **Explorer les Données** :
   - Utilisez les tableaux de bord pour explorer les données immobilières en France.
   - Sélectionnez différentes visualisations pour obtenir des informations pertinentes sur le marché.

5. **Faire des Prédictions** :
   - Accédez à l'espace de prédiction et fournissez les informations requises pour estimer la valeur foncière d'un bien immobilier.

## Technologies Utilisées

- Python
- Dash (Framework pour les applications web interactives)
- Autres packages listés dans `requirements.txt`

## Auteur

Ce projet a été développé par Adrien CASTEX, Clovis VARANGOT-REILLE et Victor SIGOGNEAU.

## Licence
Opensource 

N'hésitez pas à contribuer ou à signaler des problèmes en créant une issue. Nous espérons que l'Application ImmoPred vous sera utile pour explorer le marché immobilier en France et pour effectuer des prédictions de valeur foncière.
