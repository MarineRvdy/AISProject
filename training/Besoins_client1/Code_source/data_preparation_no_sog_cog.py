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
    """
    df = pd.read_csv(csv_path)
    df.replace({"\\N": np.nan}, inplace=True)
    numeric_features = ["Heading", "Length", "Width", "Draft"]  # SANS SOG, COG
    df[numeric_features] = df[numeric_features].apply(pd.to_numeric, errors="coerce")
    return df

def build_preprocessor(df: pd.DataFrame):
    numeric_features = ["Heading", "Length", "Width", "Draft"]  # SANS SOG, COG
    categorical_features = ["VesselType", "TransceiverClass"]
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

def prepare_features(csv_path: str, save_path: str = None, fit=True):
    df = load_data(csv_path)
    processor = build_preprocessor(df)
    if fit:
        X = processor.fit_transform(df)
        if save_path:
            # On sauvegarde dans preprocessor/<script>_preprocessor.joblib
            script_name = Path(__file__).stem
            save_dir = Path(__file__).parent / "preprocessor"
            save_dir.mkdir(exist_ok=True)
            unique_save_path = save_dir / f"{script_name}_preprocessor.joblib"
            joblib.dump(processor, unique_save_path)
            print(f"Processor saved to {unique_save_path}")
    else:
        # Mode test : on charge le préprocesseur déjà fit
        script_name = Path(__file__).stem
        load_path = Path(__file__).parent / "preprocessor" / f"{script_name}_preprocessor.joblib"
        processor = joblib.load(load_path)
        X = processor.transform(df)
    return X, processor

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--csv_path", required=True)
    parser.add_argument("--test_only", action="store_true", help="Utiliser le préprocesseur déjà entraîné pour transformer uniquement (pas de fit)")
    parser.add_argument("--out_processor", default="preprocessor_no_sog_cog.joblib")
    args = parser.parse_args()

    if args.test_only:
        # Mode test : transform uniquement, pas de fit, pas de sauvegarde
        X, _ = prepare_features(args.csv_path, None, fit=False)
        print("Test set transformed (no fit, no save)")
    else:
        X, _ = prepare_features(args.csv_path, args.out_processor, fit=True)
        print("Preprocessing completed and saved.")

