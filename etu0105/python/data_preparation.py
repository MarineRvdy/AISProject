import pandas as pd
import numpy as np
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.impute import SimpleImputer
import joblib
from pathlib import Path

def load_data(csv_path: str) -> pd.DataFrame:
    """
    Read CSV and clean missing markers like '\\N'. Convert numeric columns.
    Filter by vessel_type (default: 'Cargo').
    """
    df = pd.read_csv(csv_path)
    # Replace '\\N' strings with NaN
    df.replace({"\\N": np.nan}, inplace=True)

    numeric_features = ["SOG", "COG", "Heading", "Length", "Width", "Draft"]
    # Force numeric conversion, set errors to NaN
    df[numeric_features] = df[numeric_features].apply(pd.to_numeric, errors="coerce")


    return df

def build_preprocessor(df: pd.DataFrame):
    numeric_features = ["SOG", "COG", "Heading", "Length", "Width", "Draft"]
    categorical_features = ["VesselType"]
    # fill missing numeric with median
    numeric_transformer = Pipeline(
        steps=[
            ("imputer", SimpleImputer(strategy="median")),
            ("scaler", StandardScaler()),
        ]
    )
    categorical_transformer = Pipeline(
        steps=[
            ("imputer", SimpleImputer(strategy="most_frequent")),
            ("onehot", OneHotEncoder(handle_unknown="ignore")),
        ]
    )

    preprocessor = ColumnTransformer(
        transformers=[
            ("num", numeric_transformer, numeric_features),
            ("cat", categorical_transformer, categorical_features),
        ]
    )
    return preprocessor

def prepare_features(csv_path: str, save_path: str = None):
    df = load_data(csv_path)
    processor = build_preprocessor(df)
    X = processor.fit_transform(df)
    if save_path:
        joblib.dump(processor, save_path)
        print(f"Processor saved to {save_path}")
    return X, processor

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("--csv_path", required=True)
    parser.add_argument("--out_processor", default="preprocessor_web.joblib")
    args = parser.parse_args()

    X, _ = prepare_features(args.csv_path, args.out_processor)
    # La sauvegarde sera faite automatiquement dans le dossier du script avec un nom unique
    # donc on ne passe plus args.out_processor
    # On laisse l'appel pour compatibilité mais il sera ignoré

