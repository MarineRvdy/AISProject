import joblib
import numpy as np
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score, calinski_harabasz_score, davies_bouldin_score
from pathlib import Path

from data_preparation import prepare_features


def train_clustering(
    csv_path: str,
    n_clusters: int = 8,
    model_out: str = "kmeans_model3clusters.joblib",
    processor_path: str = "preprocessors/preprocessor.joblib"
):
    X, processor = prepare_features(csv_path, processor_path)
    kmeans = KMeans(n_clusters=n_clusters, random_state=42)
    labels = kmeans.fit_predict(X)

    sil = silhouette_score(X, labels)
    ch = calinski_harabasz_score(X.toarray() if hasattr(X, "toarray") else X, labels)
    db = davies_bouldin_score(X, labels)

    print(f"Silhouette: {sil:.3f} | Calinski-Harabasz: {ch:.2f} | Davies-Bouldin: {db:.3f}")

    joblib.dump(kmeans, model_out)
    print(f"Model saved to {model_out}")
    return kmeans, labels


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("--csv_path", required=True)
    parser.add_argument("--n_clusters", type=int, default=8)
    parser.add_argument("--model_out", default="kmeans_model.joblib")
    parser.add_argument("--processor_out", default="preprocessor.joblib")
    args = parser.parse_args()

    train_clustering(
        args.csv_path,
        n_clusters=args.n_clusters,
        model_out=args.model_out,
        processor_path=args.processor_out,
    )
