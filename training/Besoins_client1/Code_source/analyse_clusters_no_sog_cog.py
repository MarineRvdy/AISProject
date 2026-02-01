import pandas as pd

# Charger les données test et les clusters prédits
TEST_PATH = "csv/vessel_test.csv"
CLUSTERS_PATH = "csv/predicted_clusters_no_sog_cog_test.csv"
OUT_PATH = "csv/vessel_test_with_clusters.csv"

# 1. Charger les CSV
print("Chargement des données...")
df_test = pd.read_csv(TEST_PATH)
clusters = pd.read_csv(CLUSTERS_PATH)

# 2. Joindre la colonne cluster (si même ordre)
df_test["predicted_cluster"] = clusters["predicted_cluster"]

# 3. Sauvegarder le DataFrame enrichi
print(f"Sauvegarde du fichier enrichi : {OUT_PATH}")
df_test.to_csv(OUT_PATH, index=False)

# 4. Statistiques descriptives par cluster
print("\nStatistiques par cluster :")
print(df_test.groupby("predicted_cluster").describe(include="all"))

# 5. (Optionnel) Afficher la répartition des types de navires par cluster
if "VesselType" in df_test.columns:
    print("\nRépartition des types de navires par cluster :")
    print(df_test.groupby(["predicted_cluster", "VesselType"]).size())

print("\nAnalyse terminée. Vous pouvez maintenant explorer le fichier :", OUT_PATH)
