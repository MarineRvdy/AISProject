import pandas as pd
import joblib
from data_preparation import build_preprocessor
import argparse


def predict_and_compare(csv_path: str, mmsi: int, model_path: str, processor_path: str, global_clusters_path: str = None):
    df = pd.read_csv(csv_path)
    row = df[df["MMSI"] == mmsi]
    if row.empty:
        raise ValueError("MMSI not found in dataset")
    kmeans = joblib.load(model_path)
    preprocessor = joblib.load(processor_path)
    X = preprocessor.transform(row)
    cluster_pred = kmeans.predict(X)[0]
    print(f"MMSI {mmsi} - Cluster prédit par le modèle du train : {cluster_pred}")

    if global_clusters_path:
        # On suppose que le fichier contient au moins les colonnes MMSI et cluster
        df_global = pd.read_csv(global_clusters_path)
        row_global = df_global[df_global["MMSI"] == mmsi]
        if not row_global.empty:
            cluster_global = row_global.iloc[0]["cluster"]
            print(f"MMSI {mmsi} - Cluster issu du clustering global : {cluster_global}")
            if cluster_pred == cluster_global:
                print("Concordance : OUI")
            else:
                print("Concordance : NON")
        else:
            print(f"MMSI {mmsi} non trouvé dans le fichier de clusters globaux.")
    else:
        print("Aucun fichier de clusters globaux fourni, comparaison impossible.")

# Ancienne fonction conservée pour compatibilité éventuelle

def predict_single(csv_path: str, mmsi: int, model_path: str, processor_path: str):
    df = pd.read_csv(csv_path)
    row = df[df["MMSI"] == mmsi]
    if row.empty:
        raise ValueError("MMSI not found in dataset")
    kmeans = joblib.load(model_path)
    preprocessor = joblib.load(processor_path)
    X = preprocessor.transform(row)
    cluster = kmeans.predict(X)[0]
    print(f"MMSI {mmsi} belongs to cluster {cluster}")


from scipy.optimize import linear_sum_assignment
from sklearn.metrics import confusion_matrix
import numpy as np

def align_and_compare_clusters(csv_path, predicted_clusters_path, global_clusters_path):
    # Charger les clusters prédits et globaux
    df_pred = pd.read_csv(predicted_clusters_path)
    df_global = pd.read_csv(global_clusters_path)

    # Forcer le type int sur MMSI
    df_pred['MMSI'] = df_pred['MMSI'].astype(int)
    df_global['MMSI'] = df_global['MMSI'].astype(int)

    # Supprimer les doublons sur MMSI (garde le premier)
    df_pred = df_pred.drop_duplicates(subset='MMSI', keep='first')
    df_global = df_global.drop_duplicates(subset='MMSI', keep='first')

    print(f"Nb MMSI uniques prédits : {len(df_pred)}")
    print(f"Nb MMSI uniques globaux : {len(df_global)}")

    # Fusion sur MMSI
    df = df_pred.merge(df_global, on="MMSI", suffixes=("_pred", "_global"))
    print(f"Nb de MMSI communs : {len(df)}")

    # Vérifier les noms de colonnes
    pred_col = "predicted_cluster" if "predicted_cluster" in df.columns else "cluster_pred"
    global_col = "cluster" if "cluster" in df.columns else "cluster_global"
    # Matrice de confusion
    from sklearn.metrics import confusion_matrix
    from scipy.optimize import linear_sum_assignment
    conf_mat = confusion_matrix(df[global_col], df[pred_col])
    row_ind, col_ind = linear_sum_assignment(-conf_mat)
    mapping = {col: row for row, col in zip(row_ind, col_ind)}
    print("Correspondance optimale des clusters (prédits -> globaux) :", mapping)
    # Remapper les clusters prédits
    df["predicted_cluster_aligned"] = df[pred_col].map(mapping)
    concordance = (df["predicted_cluster_aligned"] == df[global_col]).mean()
    print(f"Taux de concordance après alignement : {concordance*100:.2f}%")
    print("\nEffectifs par cluster global :\n", df[global_col].value_counts().sort_index())
    print("Effectifs par cluster prédit (après alignement) :\n", df["predicted_cluster_aligned"].value_counts().sort_index())

# ------------------------------------------------------------
# Fonction script_final déplacée dans script_final.py
# ------------------------------------------------------------
from script_final import script_final

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--csv_path", required=True)
    parser.add_argument("--mmsi", type=int, required=False, help="MMSI du navire à prédire (requis sauf avec --align_all)")
    parser.add_argument("--model_path", default="kmeans_model_no_sog_cog.joblib")
    parser.add_argument("--processor_path", default="preprocessor_no_sog_cog.joblib")
    parser.add_argument("--global_clusters_path", default=None, help="Fichier CSV contenant les clusters globaux pour comparaison (doit contenir MMSI et cluster)")
    parser.add_argument("--predicted_clusters_path", default=None, help="Fichier CSV avec les clusters prédits (doit contenir MMSI et predicted_cluster)")
    parser.add_argument("--align_all", action="store_true", help="Active l'alignement global des clusters sur tout le test")
    args = parser.parse_args()

    if args.align_all:
        if args.predicted_clusters_path is None or args.global_clusters_path is None:
            print("--predicted_clusters_path et --global_clusters_path sont requis avec --align_all")
        else:
            align_and_compare_clusters(args.csv_path, args.predicted_clusters_path, args.global_clusters_path)
    else:
        if args.mmsi is None:
            parser.error("--mmsi est requis sauf si --align_all est passé.")
        predict_and_compare(
            csv_path=args.csv_path,
            mmsi=args.mmsi,
            model_path=args.model_path,
            processor_path=args.processor_path,
            global_clusters_path=args.global_clusters_path
        )

    # Ancienne fonction single, à retirer si inutile
    # predict_single(
    #     args.csv_path,
    #     args.mmsi,
    #     args.model_path,
    #     args.processor_path,
    # )
    processor_path=args.processor_path,
