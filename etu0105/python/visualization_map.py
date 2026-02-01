import importlib
import sys
import subprocess

def install_and_import(package, import_name=None):
    import_name = import_name or package
    try:
        importlib.import_module(import_name)
    except ImportError:
        subprocess.check_call([sys.executable, "-m", "pip", "install", package])

install_and_import("pandas")
install_and_import("joblib")
install_and_import("plotly")
install_and_import("pathlib")
install_and_import("numpy")

import pandas as pd
import joblib
import plotly.express as px
from data_preparation import build_preprocessor
from pathlib import Path


def visualize_clusters(
    csv_path: str,
    model_path: str = "ressources_calcul/kmeans_model3clusters_web.joblib",
    processor_path: str = "ressources_calcul/preprocessor_web.joblib",
    output_html: str = "map/cluster_map.html",
):
    df = pd.read_csv(csv_path, na_values="\\N", low_memory=False)
    # Load models
    kmeans = joblib.load(model_path)
    preprocessor = joblib.load(processor_path)

    X = preprocessor.transform(df)
    labels = kmeans.predict(X)

    df["cluster"] = labels

    fig = px.scatter_mapbox(
        df,
        lat="LAT",
        lon="LON",
        color="cluster",
        hover_data=["MMSI"],
        hover_name="VesselName",
        zoom=4,
        height=700,
    )
    # Rendre les points plus fins et transparents
    fig.update_traces(marker=dict(size=3, opacity=0.6))
    fig.update_layout(mapbox_style="open-street-map")
    fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
    fig.write_html(output_html)
    print("Map saved to", output_html)


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("--csv_path", required=True)
    parser.add_argument("--model_path", default="ressources_calcul/kmeans_model3clusters_web.joblib")
    parser.add_argument("--processor_path", default="ressources_calcul/preprocessor_web.joblib")
    parser.add_argument("--output_html", default="map/cluster_map.html")
    args = parser.parse_args()

    visualize_clusters(
        args.csv_path,
        model_path=args.model_path,
        processor_path=args.processor_path,
        output_html=args.output_html,
    )
