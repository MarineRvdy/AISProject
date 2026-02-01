# AIS Project - Système de Suivi et d'Analyse de Navires

Projet complet d'analyse et de suivi de navires utilisant les données AIS (Automatic Identification System) avec des fonctionnalités de prédiction de trajectoire, clustering et analyse en temps réel.

## 🚢 Vue d'ensemble

Ce projet combine une application web de suivi de navires avec des pipelines de traitement de données et des modèles de machine learning pour l'analyse des trajectoires maritimes.

## 📁 Structure du Projet

```
AISProject/
├── etu0105/                    # Application web principale
│   ├── README.md               # Documentation détaillée de l'application
│   ├── index.php               # Page d'accueil
│   ├── ajout_navire.php        # Interface d'ajout de navires
│   ├── visualiser_navire.php   # Visualisation détaillée
│   ├── prediction_*.php        # Interfaces de prédiction
│   ├── css/                    # Styles
│   ├── js/                     # Scripts JavaScript
│   ├── php/                    # Backend PHP
│   ├── python/                 # Scripts d'analyse Python
│   ├── ressources_calcul/      # Modèles ML pré-entraînés
│   ├── map/                    # Cartes interactives
│   └── csv/                    # Données d'import/export
├── pre-processing/             # Pipeline de nettoyage des données (R)
│   ├── f1.R                    # Exploration et description des données
│   ├── f2.R                    # Nettoyage et préparation
│   ├── f3.R                    # Analyse statistique
│   ├── f4.R                    # Visualisations
│   ├── f5.R                    # Export des données nettoyées
│   └── vessel_*.csv            # Jeux de données traités
└── training/                   # Entraînement des modèles ML
    ├── Besoins_client1/        # Modèles de clustering
    │   └── Code_source/        # Scripts Python
    ├── Besoins_client2/        # Notebooks d'analyse
    └── Besoins_client3/        # Expérimentations
```

## 🛠 Technologies Utilisées

### Backend Web
- **PHP 7.4+** : Application web principale
- **MySQL 5.7+** : Base de données des navires
- **Apache/Nginx** : Serveur web

### Data Science & ML
- **Python 3.8+** : Analyse et machine learning
- **R** : Prétraitement statistique des données
- **scikit-learn** : Modèles de clustering et prédiction
- **pandas/numpy** : Manipulation des données
- **folium/plotly** : Visualisations interactives

### Frontend
- **JavaScript** : Interactivité et cartes
- **CSS** : Style et responsive design
- **HTML5** : Structure des pages

## 🚀 Installation Rapide

### 1. Application Web
```bash
# Copier le dossier etu0105 dans votre serveur web
cp -r etu0105 /var/www/html/

# Configurer la base de données
# Modifier php/constantes.php avec vos credentials MySQL

# Accéder à l'application
http://localhost/etu0105
```

### 2. Dépendances Python
```bash
cd etu0105/python
pip install -r requirements.txt
```

### 3. Environnement R (pour le prétraitement)
```r
# Installer les packages requis
install.packages(c("funModeling", "dplyr", "tidyr", "corrplot", "readr", "geosphere"))
```

## 📊 Fonctionnalités Principales

### Application Web (etu0105/)
- **Suivi en temps réel** : Visualisation des positions des navires
- **Prédiction de trajectoire** : Prévisions sur 5/10/15 minutes
- **Clustering intelligent** : Groupement des navires par comportement
- **Analyse par type** : Étude des patterns par catégorie de navire
- **Gestion des données** : Import/export CSV, ajout de navires

### Pipeline de Prétraitement (pre-processing/)
- **Nettoyage des données AIS** : Suppression des anomalies et valeurs aberrantes
- **Analyse exploratoire** : Statistiques descriptives et corrélations
- **Visualisations** : Graphiques et cartes des données brutes
- **Export structuré** : Génération de datasets propres pour l'entraînement

### Modèles de Machine Learning (training/)
- **Clustering K-means** : Identification des patterns de navigation
- **Prédiction de trajectoire** : Modèles de régression pour lat/lon/vitesse
- **Classification par type** : Catégorisation automatique des navires
- **Notebooks d'analyse** : Expérimentations et visualisations

## 🎯 Cas d'Usage

### Pour les Opérateurs Maritimes
- Surveillance des flottes en temps réel
- Détection d'anomalies de navigation
- Optimisation des routes maritimes

### Pour les Analystes de Données
- Exploration des patterns de trafic maritime
- Études comportementales par type de navire
- Prédictions pour la planification logistique

### Pour la Recherche
- Développement de nouveaux algorithmes de prédiction
- Analyse des impacts environnementaux
- Études sur la sécurité maritime

## 📈 Données Utilisées

Le projet utilise des données AIS réelles comprenant :
- **Positions GPS** : Latitude, longitude, timestamp
- **Caractéristiques navires** : Longueur, largeur, tirant d'eau
- **Informations voyage** : Vitesse (SOG), cap (COG), heading
- **Métadonnées** : Type de navire, classe de transceiver, MMSI

## 🔧 Développement

### Structure Modulaire
- Chaque composant est indépendant et réutilisable
- API REST pour la communication frontend/backend
- Modèles ML sérialisés pour le déploiement

### Tests et Validation
- Validation croisée des modèles de prédiction
- Tests de performance sur données historiques
- Interface utilisateur testée sur navigateurs modernes

## 👥 Équipe de Développement

- **Eliott COSQUER** 
- **Guillaume LE NESTOUR**
- **Marine REVERDY**

## 📄 Licence

Projet académique ISEN A3 - 2025

---

## 📚 Documentation Complémentaire

- **Application Web** : Voir `etu0105/README.md` pour les détails techniques
- **Prétraitement** : Commentaires détaillés dans les scripts R
- **Modèles ML** : Documentation dans les notebooks Jupyter
- **API** : Documentation des endpoints dans `php/`

## 🤝 Contribution

Ce projet est open source pour la communauté maritime et data science. N'hésitez pas à proposer des améliorations ou à signaler des issues.
