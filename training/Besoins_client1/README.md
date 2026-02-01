# Auteur
Eliott Cosquer CIR3
12/06/2025

# Dépendances

# Toutes les commandes sont faîtes pour le windows powershell !!!

au tout début, activez venv pour eviter les problèmes entre les versions de python
(pas obligatoire mais c'est mieux)
cette commande est à lancer dans ../Client_1

```bash
venv\Scripts\activate
```

puis allez dans Code_source pour executer toutes les commandes suivantes
```bash
cd Code_source
```
Ce projet nécessite Python 3.8+ et les packages suivants :

```bash
pip install -r requirements.txt
```

# PARTIE RENDU

Script demandé au rendu (avec des valeures de base):
```bash
 python script_final.py `
--predicted_clusters_path csv/vessel_test_with_clusters.csv `
--global_clusters_path csv/vessel_clusters_no_sog_cog.csv
```
Script demandé au rendu (avec des valeures personnalisées):
```bash
python script_final.py `
  --length 120 `
  --width 22 `
  --draft 8.5 `
  --heading 135 `
  --vessel_type Tanker `
  --transceiver_class A `
  --predicted_clusters_path csv/vessel_test_with_clusters.csv `
  --global_clusters_path csv/vessel_clusters_no_sog_cog.csv
```

# PARTIE EXPERIMENTALE

## Versions du workflow

- **Avec SOG/COG** : permet de visualiser les ports grâce aux changements de cluster selon le mouvement du navire, mais la prédiction n'est pas pertinente (un même navire peut changer de cluster selon sa vitesse/cap).
- **Sans SOG/COG (`no_sog_cog`)** : la prédiction de cluster sur de nouveaux navires/test est cohérente et pertinente.

# **Avec SOG/COG**

Cette partie permet de regrouper des navires selon leurs schémas de navigation (clustering non-supervisé) et de visualiser ces groupes sur deux cartes interactives.


```bash
# 1. Prétraitement + clustering
python data_preparation.py --csv_path csv/vessel_clean.csv
python clustering.py --csv_path csv/vessel_clean.csv --n_clusters 3

# 2. Visualisation carte
python visualization_map.py --csv_path csv/vessel_clean.csv

# 3. Inspecter le modèle
python inspect_kmeans_model.py

```

# Workflow de Clustering et Prédiction AIS

Cette partie vise à regrouper les navires AIS en clusters à l'aide de KMeans mais sans les variables de vitesse et de cap sur fonds, puis à prédire et comparer les clusters sur des données de test de façon robuste et automatisée.

## Étapes du workflow `no_sog_cog`

### 1. Prétraitement et entraînement sur le train
```bash
python data_preparation_no_sog_cog.py --csv_path csv/vessel_train.csv
python clustering_no_sog_cog.py --csv_path csv/vessel_train.csv --n_clusters 3
```
- Entraîne le préprocesseur et le modèle KMeans uniquement sur le train.

### 2. Application sur le test (prédiction)
```bash
python data_preparation_no_sog_cog.py --csv_path csv/vessel_test.csv --test_only
python clustering_no_sog_cog.py --csv_path csv/vessel_test.csv --test_only --predict_out csv/predicted_clusters_no_sog_cog_test.csv
```
- Transforme le test avec le préprocesseur du train et prédit les clusters avec le modèle du train.
- Les clusters prédits sont sauvegardés dans `csv/predicted_clusters_no_sog_cog_test.csv`.

### 3. Fusion et analyse des clusters
```bash
python analyse_clusters_no_sog_cog.py
```
- Fusionne les clusters prédits avec le DataFrame test.
- Affiche des statistiques descriptives par cluster et la répartition des types de navires.
- Le fichier enrichi est sauvegardé dans `csv/vessel_test_with_clusters.csv`.

### 4. Alignement et validation des clusters (démarche récente)
Pour garantir que les labels de clusters KMeans (arbitraires) sont bien alignés entre la prédiction (modèle du train) et le clustering global (sur tout le test), on utilise un alignement automatique basé sur l'algorithme d'assignation optimale (Hungarian algorithm).

**Commandes :**
```bash
python predict_cluster.py --csv_path csv/vessel_test.csv --align_all --predicted_clusters_path csv/vessel_test_with_clusters.csv --global_clusters_path csv/vessel_clusters_no_sog_cog.csv
```
- Affiche la correspondance optimale entre labels prédits et globaux, le taux de concordance après alignement, et les effectifs par cluster.
- Permet de valider la cohérence du modèle et du workflow sur les MMSI communs.

### 5. Analyse avancée (optionnelle)
- Utilisez `inspect_kmeans_model_no_sog_cog.py` pour explorer la répartition des types de navires, statistiques descriptives, etc. sur les clusters globaux.

---

## Points importants de la démarche
- **Robustesse** : Nettoyage automatique des doublons et gestion dynamique des noms de colonnes pour éviter toute erreur lors des comparaisons.
- **Alignement automatique** : Les clusters prédits sont toujours remappés pour correspondre au mieux aux clusters globaux, rendant la comparaison fiable même si les labels sont arbitraires.
- **Validation** : Un taux de concordance de 100 % sur les MMSI communs valide la cohérence du workflow.
- **Limite** : La prédiction de cluster n’est pertinente que pour la version sans SOG/COG.

---

## Exemple d’utilisation pour comparer et aligner les clusters
```bash
python predict_cluster.py --csv_path csv/vessel_test.csv --align_all --predicted_clusters_path csv/vessel_test_with_clusters.csv --global_clusters_path csv/vessel_clusters_no_sog_cog.csv
```

---


