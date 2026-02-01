import pandas as pd
import joblib

# --- Paramètres ---
CSV_PATH = "csv/vessel_clean.csv"
MODEL_PATH = "kmeans/kmeans_model3clusters.joblib"
PROCESSOR_PATH = "preprocessor/preprocessor.joblib"
OUTPUT_CSV = "csv/vessel_clusters.csv"

# --- Chargement des données et modèles ---
df = pd.read_csv(CSV_PATH, na_values="\\N", low_memory=False)
kmeans = joblib.load(MODEL_PATH)
preprocessor = joblib.load(PROCESSOR_PATH)

X = preprocessor.transform(df)
df["cluster"] = kmeans.predict(X)

print("\n--- Effectif par cluster ---")
print(df["cluster"].value_counts())

print("\n--- Répartition des types de navires par cluster ---")
print(df.groupby("cluster")["VesselType"].value_counts())

print("\n--- Statistiques descriptives SOG (vitesse) par cluster ---")
print(df.groupby("cluster")["SOG"].describe())

print("\n--- Moyennes des variables numériques par cluster ---")
print(df.groupby("cluster").mean(numeric_only=True))

# Export CSV pour inspection
print(f"\nExport des données enrichies avec cluster dans {OUTPUT_CSV}")
df.to_csv(OUTPUT_CSV, index=False)
