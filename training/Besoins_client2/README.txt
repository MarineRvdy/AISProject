# Projet de Prédiction du Type de Navire

## Commande
installation des librairies
pip install pandas numpy==2.0.0 scikit-learn==1.7.0 seaborn

exécution du script seul
python script_predict_vesseltype.py --Status 15 --Length 100 --Width 12 --Draft 6.8 --Cargo 70 --Heading 249

## Avant utilisation
Penser à importer les fichiers `vessel_sampled.csv` et `script_predict_vesseltype.py` pour qu'il soit lisible par `Projet_S6_IA_client_2.ipynb` (exemple : sous google colab cliquer sur l'icone de dossier sur la barre à gauche de l'écran puis sur importer et enfin importer les deux fichiers).

## Utilisation
Executer les cellules de `Projet_S6_IA_client_2.ipynb` dans l'ordre.



## Présentation
Ce projet vise à prédire le type de navire (`VesselType`) à l'aide de techniques de machine learning, à partir de données AIS. Le pipeline inclut le prétraitement des données, l'entraînement du modèle, l'optimisation des hyperparamètres, l'évaluation, ainsi qu'un script pour effectuer des prédictions sur de nouveaux navires.

## Variables utilisées
- Status (catégorielle)
- Length (numérique)
- Width (numérique)
- Draft (numérique)
- Cargo (catégorielle)
- Heading (numérique)

## Déroulement du projet
1. **Préparation des données** : Nettoyage et filtrage du jeu de données, sélection des variables pertinentes, gestion des classes rares.
2. **Prétraitement** : Encodage des variables catégorielles, normalisation des variables numériques. Le préprocesseur est sauvegardé au format `.pkl`.
3. **Découpage** : Séparation des données par groupe MMSI en ensembles d'entraînement, de test (et éventuellement de validation) pour éviter toute fuite de données.
4. **Entraînement du modèle** : Entraînement d'un RandomForestClassifier. Les hyperparamètres sont optimisés grâce à GridSearchCV avec validation croisée.
5. **Sauvegarde du modèle** : Le modèle entraîné et le préprocesseur sont sauvegardés au format `.pkl` pour une utilisation ultérieure.
6. **Script de prédiction** : Un script CLI (`script_predict_vesseltype.py`) permet de prédire le type de navire à partir de caractéristiques passées en ligne de commande, en chargeant le modèle et le préprocesseur sauvegardés.

## Fichiers
- `vessel_sampled.csv` : Jeu de données échantillonné et nettoyé
- `preprocessor_vessel_type.pkl` : Préprocesseur sauvegardé
- `rf_vessel_type_classifier.pkl` : Modèle Random Forest sauvegardé
- `script_predict_vesseltype.py` : Script CLI pour la prédiction
- `Projet_S6_IA_client_2.ipynb` : Notebook pour l'analise des données et le développement du modèle


## Auteur
Guillaume Le Nestour
