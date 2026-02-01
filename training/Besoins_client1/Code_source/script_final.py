"""Script pour prédire le cluster d'un navire à partir de ses caractéristiques.

Utilisation en ligne de commande :

    python script_final.py \
        --length 100 \
        --width 20 \
        --draft 7 \
        --heading 45 \
        --vessel_type Tanker \
        --transceiver_class A \
        --predicted_clusters_path clusters_pred.csv \
        --global_clusters_path clusters_global.csv

Si aucun argument n'est fourni, les valeurs par défaut (1ᵉʳ quartile du jeu de test) sont utilisées.
"""

import argparse
from pathlib import Path
from typing import Any

import joblib
import pandas as pd
from scipy.optimize import linear_sum_assignment
from sklearn.metrics import confusion_matrix
import numpy as np

# Valeurs par défaut (~25 % quartile test)
DEFAULTS: dict[str, Any] = {
    "length": 85.0,
    "width": 14.0,
    "draft": 6.0,
    "heading": 90.0,
    "vessel_type": "Cargo",
    "transceiver_class": "A",
}

MODEL_PATH = "kmeans/clustering_no_sog_cog_kmeans_model.joblib"
PROCESSOR_PATH = "preprocessor/data_preparation_no_sog_cog_preprocessor.joblib"


def _compute_cluster_mapping(pred_csv: str, global_csv: str) -> dict[int, int]:
    """Calcule la correspondance optimale (Hungarian) entre clusters prédits et globaux."""
    import pandas as pd

    df_pred = pd.read_csv(pred_csv)
    df_global = pd.read_csv(global_csv)

    # assurer types et unicité
    df_pred["MMSI"] = df_pred["MMSI"].astype(int)
    df_global["MMSI"] = df_global["MMSI"].astype(int)
    df_pred = df_pred.drop_duplicates(subset="MMSI", keep="first")
    df_global = df_global.drop_duplicates(subset="MMSI", keep="first")

    df = df_pred.merge(df_global, on="MMSI", suffixes=("_pred", "_global"))
    pred_col = "predicted_cluster" if "predicted_cluster" in df.columns else "cluster_pred"
    global_col = "cluster" if "cluster" in df.columns else "cluster_global"

    conf_mat = confusion_matrix(df[global_col], df[pred_col])
    row_ind, col_ind = linear_sum_assignment(-conf_mat)
    return {col: row for row, col in zip(row_ind, col_ind)}


def script_final(
    Length: float = DEFAULTS["length"],
    Width: float = DEFAULTS["width"],
    Draft: float = DEFAULTS["draft"],
    Heading: float = DEFAULTS["heading"],
    VesselType: str = DEFAULTS["vessel_type"],
    TransceiverClass: str = DEFAULTS["transceiver_class"],
    model_path: str = MODEL_PATH,
    processor_path: str = PROCESSOR_PATH,
    predicted_clusters_path: str | None = None,
    global_clusters_path: str | None = None,
) -> int:
    """Prédit le cluster associé à un navire à partir de ses caractéristiques."""

    # Crée un DataFrame avec une seule ligne
    df_input = pd.DataFrame(
        {
            "Heading": [Heading],
            "Length": [Length],
            "Width": [Width],
            "Draft": [Draft],
            "VesselType": [VesselType],
            "TransceiverClass": [TransceiverClass],
        }
    )

    # Chargement des artefacts
    preprocessor = joblib.load(processor_path)
    kmeans = joblib.load(model_path)

    # Transformation + prédiction
    X = preprocessor.transform(df_input)
    cluster_pred: int = int(kmeans.predict(X)[0])

    # Mapping vers cluster global si demandé
    mapped_cluster = None
    if predicted_clusters_path and global_clusters_path:
        try:
            mapping = _compute_cluster_mapping(predicted_clusters_path, global_clusters_path)
            mapped_cluster = mapping.get(cluster_pred)
        except Exception as e:  # pragma: no cover
            print("[WARN] Impossible de calculer la correspondance des clusters :", e)

    # Affichage résultat
    print("Caractéristiques du navire :", df_input.iloc[0].to_dict())
    print("Cluster prédit (train) :", cluster_pred)
    if mapped_cluster is not None:
        print("Cluster global correspondant :", mapped_cluster)
    return mapped_cluster if mapped_cluster is not None else cluster_pred


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Prédit le cluster d'un navire")
    parser.add_argument("--length", type=float, default=DEFAULTS["length"], help="Longueur du navire")
    parser.add_argument("--width", type=float, default=DEFAULTS["width"], help="Largeur du navire")
    parser.add_argument("--draft", type=float, default=DEFAULTS["draft"], help="Tirant d'eau (draft)")
    parser.add_argument("--heading", type=float, default=DEFAULTS["heading"], help="Cap (heading)")
    parser.add_argument("--vessel_type", default=DEFAULTS["vessel_type"], help="Type de navire")
    parser.add_argument("--transceiver_class", default=DEFAULTS["transceiver_class"], help="Classe du transpondeur (A/B)")
    parser.add_argument("--model_path", default=MODEL_PATH, help="Chemin vers le modèle KMeans")
    parser.add_argument("--processor_path", default=PROCESSOR_PATH, help="Chemin vers le préprocesseur")
    parser.add_argument("--predicted_clusters_path", default=None, help="CSV contenant les clusters prédits (avec MMSI)")
    parser.add_argument("--global_clusters_path", default=None, help="CSV contenant les clusters globaux (avec MMSI)")

    args = parser.parse_args()

    script_final(
        Length=args.length,
        Width=args.width,
        Draft=args.draft,
        Heading=args.heading,
        VesselType=args.vessel_type,
        TransceiverClass=args.transceiver_class,
        model_path=args.model_path,
        processor_path=args.processor_path,
        predicted_clusters_path=args.predicted_clusters_path,
        global_clusters_path=args.global_clusters_path,
    )
