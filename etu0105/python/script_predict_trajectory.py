# -*- coding: utf-8 -*-
# Script pour prédire les positions futures d'un navire à partir de ses caractéristiques
# Auteur : Marine REVERDY
# Date : 11/06/2025
# Licence : A3 ISEN
## Ce script prend en entrée les caractéristiques d'un navire à un instant donné et prédit sa position future à 5, 10 et 15 minutes.

import numpy as np
import pandas as pd
import joblib
import folium
import argparse
import json


# --- Argument parser ---
parser = argparse.ArgumentParser(description="Prédiction de trajectoire AIS à partir de données saisies.")
parser.add_argument('--LAT', type=float, required=True, help="Latitude")
parser.add_argument('--LON', type=float, required=True, help="Longitude")
parser.add_argument('--SOG', type=float, required=True, help="Speed Over Ground")
parser.add_argument('--COG', type=float, required=True, help="Course Over Ground")
parser.add_argument('--Heading', type=float, required=True, help="Cap du navire")
parser.add_argument('--VesselType', type=int, required=True, help="Type de navire")
parser.add_argument('--Length', type=float, required=True, help="Longueur du navire")
parser.add_argument('--Width', type=float, required=True, help="Largeur du navire")
parser.add_argument('--Draft', type=float, required=True, help="Tirant d'eau du navire")

args = parser.parse_args()

# --- Préparation des données ---
input_data = {
    'LAT': args.LAT,
    'LON': args.LON,
    'SOG': args.SOG,
    'COG': args.COG,
    'Heading': args.Heading,
    'VesselType': args.VesselType,
    'Length': args.Length,
    'Width': args.Width,
    'Draft': args.Draft
}

df_input = pd.DataFrame([input_data])
X_input = df_input[['LAT', 'LON', 'SOG', 'COG', 'Heading', 'VesselType', 'Length', 'Width', 'Draft']]


scaler = joblib.load("../ressources_calcul/scaler.pkl")
X_scaled = scaler.transform(X_input)

# --- Prédictions ---
horizons = [5, 10, 15]
models_lat = {h: joblib.load(f"../ressources_calcul/model_lat_{h}.pkl") for h in horizons}
models_lon = {h: joblib.load(f"../ressources_calcul/model_lon_{h}.pkl") for h in horizons}

predictions = {}
for h in horizons:
    pred_lat = models_lat[h].predict(X_scaled)[0]
    pred_lon = models_lon[h].predict(X_scaled)[0]
    predictions[h] = (pred_lat, pred_lon)
    print(f"Horizon +{h} minutes : LAT = {pred_lat:.6f}, LON = {pred_lon:.6f}")

# --- Carte Folium ---
center_lat = input_data['LAT']
center_lon = input_data['LON']
m = folium.Map(location=[center_lat, center_lon], zoom_start=8)

folium.CircleMarker(
    location=[center_lat, center_lon],
    radius=6,
    color='blue',
    fill=True,
    fill_opacity=0.7,
    popup='Position initiale'
).add_to(m)

colors = {5: 'red', 10: 'orange', 15: 'purple'}

for h, (lat, lon) in predictions.items():
    folium.CircleMarker(
        location=[lat, lon],
        radius=5,
        color=colors[h],
        fill=True,
        fill_opacity=0.7,
        popup=f'Prédiction +{h}min'
    ).add_to(m)
    folium.PolyLine(
        locations=[[center_lat, center_lon], [lat, lon]],
        color=colors[h],
        weight=2,
        dash_array='5'
    ).add_to(m)

m.save("../map/single_vessel_prediction_absolute.html")
print("Carte enregistrée dans 'single_vessel_prediction_absolute.html'")

# --- Comparaison distance théorique vs prédite ---
def haversine(lat1, lon1, lat2, lon2):
    R = 6371.0
    phi1 = np.radians(lat1)
    phi2 = np.radians(lat2)
    dphi = np.radians(lat2 - lat1)
    dlambda = np.radians(lon2 - lon1)
    a = np.sin(dphi / 2) ** 2 + np.cos(phi1) * np.cos(phi2) * np.sin(dlambda / 2) ** 2
    c = 2 * np.arctan2(np.sqrt(a), np.sqrt(1 - a))
    return R * c

speed_kmh = input_data['SOG'] * 1.852
time_minutes = horizons
time_hours = [t / 60 for t in time_minutes]
theoretical_distances = [speed_kmh * t for t in time_hours]

lat_init, lon_init = input_data['LAT'], input_data['LON']
actual_distances = [haversine(lat_init, lon_init, *predictions[h]) for h in time_minutes]

print("\n--- Comparaison distance théorique vs prédite ---")
for t, theo, actual in zip(time_minutes, theoretical_distances, actual_distances):
    ecart_relatif = 100 * abs(actual - theo) / theo if theo != 0 else 0
    print(f"Horizon +{t} min :")
    print(f"  Distance théorique : {theo:.3f} km")
    print(f"  Distance prédite   : {actual:.3f} km")
    print(f"  Écart relatif      : {ecart_relatif:.2f}%\n")
