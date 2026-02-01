# Prédiction des Positions Futures de Navires

**Date** : 11 Juin 2025  
**Auteur** : Marine REVERDY  
**Promotion** : A3 ISEN

---

Ce projet permet de prédire les positions futures (latitude et longitude) de navires à différents horizons temporels (5, 10 et 15 minutes) à partir de données AIS historiques. Il utilise des modèles de régression Random Forest entraînés sur des données nettoyées et normalisées.

---

## Installation et prérequis


1. Installer les dépendances Python (exemple avec pip) :

```bash
pip install pandas numpy scikit-learn joblib folium argparse
```

## Contenu du projet

- `notebook_entrainement.ipynb` :  
  Jupyter Notebook pour le pré-traitement des données, création des features/targets, entraînement des modèles de régression, évaluation des performances et sauvegarde des modèles/scalers.

- `script_traitement.py` :  
  Script Python qui permet, à partir d’une entrée manuelle des caractéristiques d’un navire à un instant donné, de prédire ses positions futures selon les modèles entraînés, puis de visualiser ces prédictions sur une carte interactive Folium.

  Les données à prédire sont à renseigner dans le fichier `navire_input.json` présent dans le dossier `data`
  
  Ensuite exécuter cette commande : `python script_traitement.py --input_file data/navire_input.json`
  
  Exemple de données dans le fichier :

      {
      "LAT": 26.09687,
      "LON": -96.39664,
      "SOG": 5.0,
      "COG": 90.0,
      "Heading": 85.0,
      "VesselType": 70,
      "Length": 200.0,
      "Width": 32.0,
      "Draft": 11.8
      }

    Après exécution la carte généré est disponible dans le dossier courant sous le nom `single_vessel_prediction_absolute.html`
    

- `export_IA.csv` :  
  Dataset initial contenant les données AIS nettoyées.

- Modèles sauvegardés :  
  - `model_lat_5.pkl`, `model_lat_10.pkl`, `model_lat_15.pkl`  
  - `model_lon_5.pkl`, `model_lon_10.pkl`, `model_lon_15.pkl`

- Scaler sauvegardé :  
  - `scaler.pkl`

---

