Système de Suivi de Navires
================================

Description
----------
Application web de suivi et d'analyse des mouvements de navires en temps réel avec fonctionnalités de prédiction de trajectoire et d'analyse par type de navire.

Prérequis
---------
- Serveur web (Apache/Nginx)
- PHP 7.4 ou supérieur
- MySQL 5.7 ou supérieur
- Python 3.8+ (pour les fonctionnalités d'analyse avancée)

Prérequis Python
---------------
Les dépendances Python requises sont listées dans le fichier `python/requirements.txt`. Pour les installer, exécutez :

```bash
pip install -r python/requirements.txt
```

### Bibliothèques principales
- numpy==2.0.2
- pandas==2.3.0
- scikit-learn==1.5.1
- joblib==1.5.1

### Visualisation
- folium==0.17.0
- plotly==5.18.0

### Base de données
- mysql-connector-python==8.0.33

### Traitement des données
- scipy==1.13.1

### Sérialisation
- pickle-mixin==1.0.2

Ces versions ont été vérifiées pour assurer la compatibilité avec les modèles existants.

Installation
------------
1. Extraire le contenu de l'archive ZIP
2. Dans le dossier extrait, vous trouverez un dossier `etu0105`
3. Copier le dossier `etu0105` dans le répertoire de votre serveur web (par exemple, dans `htdocs` ou `www`)

4. Configurer la base de données :
   - Créer une base de données MySQL
   - Accéder à la page d'ajout de navire
   - Cliquer sur le bouton "Importer les données" pour initialiser la base de données

5. Configurer la base de données :
   - Modifier le fichier `php/constantes.php` avec vos paramètres de connexion :
     ```php
     $DB_SERVER = 'localhost';
     $DB_NAME = 'votre_base_de_donnees';
     $DB_USER = 'votre_utilisateur';
     $DB_PASSWORD = 'votre_mot_de_passe';
     ```

Accès à l'application
---------------------
- Une fois installée, accédez à l'application via votre navigateur à l'adresse :
  ```
  http://localhost/etu0105
  ```
  (Assurez-vous que le dossier s'appelle bien `etu0105` sur votre serveur web)

Structure des dossiers
---------------------
- `/css` : Feuilles de style
  - `style.css` : Styles principaux de l'application

- `/js` : Scripts JavaScript
  - `ajout_navire.js` : Gestion de l'interface d'ajout de navires
  - `prediction_trajectoire.js` : Logique de prédiction de trajectoire
  - `prediction_type.js` : Gestion de la prédiction par type
  - `visualiser_navire.js` : Affichage des détails des navires

- `/php` : Scripts côté serveur
  - `constantes.php` : Configuration de la base de données
  - `database.php` : Gestion de la connexion à la base de données
  - `export_csv.php` : Export des données en format CSV
  - `footer.php` : Pied de page commun
  - `get_navire.php` : Récupération des données des navires
  - `header.php` : En-tête commun
  - `import_csv.php` : Import de données depuis des fichiers CSV
  - `navbar.php` : Barre de navigation
  - `navire.php` : Gestion des opérations sur les navires
  - `request_prediction.php` : Traitement des requêtes de prédiction
  - `request_status.php` : Requête de statut
  - `request_visualiser.php` : Requêtes pour la visualisation

- `/python` : Scripts d'analyse et de prédiction
  - `data_preparation.py` : Préparation des données pour l'analyse
  - `insert_data.py` : Insertion des données dans la base
  - `script_predict_trajectory.py` : Prédiction de trajectoire
  - `script_predict_vesseltype.py` : Prédiction du type de navire
  - `visualization_map.py` : Génération des visualisations cartographiques
  - `requirements.txt` : Listes des dépendances Python

- `/ressources_calcul` : Modèles et données pour les calculs
  - `kmeans_model3clusters_web.joblib` : Modèle de clustering K-means
  - `model_lat_5.pkl`, `model_lat_10.pkl`, `model_lat_15.pkl` : Modèles de prédiction de latitude
  - Autres modèles de prédiction (lon_5, lon_10, lon_15, sog_5, sog_10, sog_15)

- `/img` : Images et ressources graphiques
  - `Marine.jpg`, `eliott.jpg`, `guillaume.jpg` : Photos des développeurs
  - `Port.jpg` : Image d'arrière-plan ou d'illustration

- `/map` : Cartes interactives
  - `cluster_map.html` : Carte des clusters de navires
  - `single_vessel_prediction_absolute.html` : Carte de prédiction de trajectoire

- `/csv` : Données d'import/export
  - `navires.csv.zip` : Données des navires (compressé)
  - `positions.csv.zip` : Données de positionnement (compressé)
  - `status.csv.zip` : Données de statut (compressé)
  - `vessel-clean.csv` : Données nettoyées des navires

Fichiers principaux à la racine :
- `index.php` : Page d'accueil de l'application
- `ajout_navire.php` : Interface d'ajout de nouveaux navires
- `visualiser_navire.php` : Visualisation détaillée d'un navire
- `prediction_trajectoire.php` : Interface de prédiction de trajectoire
- `prediction_type.php` : Prédiction par type de navire
- `prediction_cluster.php` : Visualisation des clusters de navires

Fonctionnalités principales
--------------------------
- Visualisation en temps réel des positions des navires
- Prédiction de trajectoire
- Analyse par type de navire
- Gestion des données de navigation
- Système d'ajout de nouveaux navires
- Outils d'analyse avancée

Utilisation
-----------
1. Accéder à l'application via votre navigateur :
   ```
   http://localhost/etu0105
   ```
2. Utiliser la barre de navigation pour accéder aux différentes fonctionnalités :
   - Visualisation des navires en temps réel
   - Prédiction de trajectoire
   - Analyse par type de navire
   - Ajout de nouveaux navires
3. Utiliser le bouton "Importer les données" sur la page d'ajout de navire pour initialiser la base de données

Développement
-------------
- Le projet utilise principalement PHP pour le backend et JavaScript pour le frontend
- Les scripts Python sont utilisés pour les analyses avancées et les prédictions

Contributeurs
-------------
- Eliott COSQUER - Développeur
- Guillaume LE NESTOUR - Développeur
- Marine REVERDY - Développeur

Licence
-------
ISEN - Projet A3 - 2025