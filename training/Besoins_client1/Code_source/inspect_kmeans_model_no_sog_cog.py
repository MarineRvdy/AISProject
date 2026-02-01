import pandas as pd
import joblib

# --- Paramètres ---
CSV_PATH = "csv/vessel_test.csv"
MODEL_PATH = "kmeans/kmeans_model_no_sog_cog.joblib"
PROCESSOR_PATH = "preprocessor/preprocessor_no_sog_cog.joblib"

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

print("\n--- Statistiques descriptives Heading par cluster ---")
print(df.groupby("cluster")["Heading"].describe())

print("\n--- Moyennes des variables numériques par cluster ---")
print(df.groupby("cluster").mean(numeric_only=True))

