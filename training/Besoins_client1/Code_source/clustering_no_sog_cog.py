import joblib
import numpy as np
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score, calinski_harabasz_score, davies_bouldin_score
from pathlib import Path
from data_preparation_no_sog_cog import prepare_features

def train_clustering(
    train_csv_path: str,
    n_clusters: int = 8,
    model_out: str = "kmeans_model_no_sog_cog.joblib",
    processor_path: str = "preprocessor_no_sog_cog.joblib",
    test_csv_path: str = None,
    predict_out: str = None
):
    X_train, processor = prepare_features(train_csv_path, processor_path, fit=True)
    kmeans = KMeans(n_clusters=n_clusters, random_state=42)
    labels_train = kmeans.fit_predict(X_train)

    sil = silhouette_score(X_train, labels_train)
    ch = calinski_harabasz_score(X_train.toarray() if hasattr(X_train, "toarray") else X_train, labels_train)
    db = davies_bouldin_score(X_train, labels_train)

    print(f"Silhouette: {sil:.3f} | Calinski-Harabasz: {ch:.2f} | Davies-Bouldin: {db:.3f}")

    save_dir = Path(__file__).parent / "kmeans"
    save_dir.mkdir(exist_ok=True)
    unique_model_out = save_dir / "clustering_no_sog_cog_kmeans_model.joblib"
    joblib.dump(kmeans, unique_model_out)
    print(f"Model saved to {unique_model_out}")

    if test_csv_path:
        # Prédiction sur le jeu de test
        import pandas as pd
        X_test, _ = prepare_features(test_csv_path, None, fit=False)
        y_pred = kmeans.predict(X_test)
        if predict_out:
            pd.DataFrame({'predicted_cluster': y_pred}).to_csv(predict_out, index=False)
        print(f"Test set predictions saved to {predict_out}")

    return kmeans, labels_train

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("--csv_path", required=True)
    parser.add_argument("--n_clusters", type=int, default=8)
    parser.add_argument("--test_only", action="store_true", help="Prédire sur le jeu de test sans fit")
    parser.add_argument("--predict_out", default=None, help="Fichier de sortie des prédictions sur le test")
    parser.add_argument("--model_out", default="kmeans_model_no_sog_cog.joblib")
    parser.add_argument("--processor_out", default="preprocessor_no_sog_cog.joblib")
    args = parser.parse_args()

    if args.test_only:
        # Mode test : prédire uniquement, ne pas fitter ni le préprocesseur ni le modèle
        import pandas as pd
        from pathlib import Path

        # Charger le préprocesseur déjà fit
        script_name = "data_preparation_no_sog_cog"
        preproc_path = Path(__file__).parent / "preprocessor" / f"{script_name}_preprocessor.joblib"
        preprocessor = joblib.load(preproc_path)

        # Charger le modèle déjà fit
        model_path = Path(__file__).parent / "kmeans" / "clustering_no_sog_cog_kmeans_model.joblib"
        kmeans = joblib.load(model_path)

        # Transformer et prédire
        df = pd.read_csv(args.csv_path)
        X_test = preprocessor.transform(df)
        y_pred = kmeans.predict(X_test)
        if args.predict_out:
            pd.DataFrame({'predicted_cluster': y_pred}).to_csv(args.predict_out, index=False)
        print(f"Test set predictions saved to {args.predict_out}")
    else:
        train_clustering(
            train_csv_path=args.csv_path,
            n_clusters=args.n_clusters,
            model_out=args.model_out,
            processor_path=args.processor_out,
        )
