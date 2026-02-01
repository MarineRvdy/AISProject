import pandas as pd
import joblib
import plotly.express as px
from data_preparation import build_preprocessor
from pathlib import Path


def visualize_clusters(
    csv_path: str,
    model_path: str = "kmeans/kmeans_model3clusters.joblib",
    processor_path: str = "preprocessor/preprocessor.joblib",
    output_html: str = "maps/cluster_map.html",
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
    parser.add_argument("--model_path", default="kmeans/kmeans_model3clusters.joblib")
    parser.add_argument("--processor_path", default="preprocessor/preprocessor.joblib")
    parser.add_argument("--output_html", default="maps/cluster_map.html")
    args = parser.parse_args()

    visualize_clusters(
        args.csv_path,
        model_path=args.model_path,
        processor_path=args.processor_path,
        output_html=args.output_html,
    )
