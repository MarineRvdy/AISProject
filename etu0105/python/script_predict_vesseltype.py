import argparse
import pickle
import pandas as pd

# Chemins vers les modèles sauvegardés
MODEL_PATH = '../ressources_calcul/rf_vessel_type_classifier.pkl'
PREPROCESSOR_PATH = '../ressources_calcul/preprocessor_vessel_type.pkl'

# Liste des features attendues
FEATURES = ['Status', 'Length', 'Width', 'Draft', 'Cargo', 'Heading']

def predict_vessel_type(input_dict):

    # Charger le modèle
    with open(MODEL_PATH, 'rb') as f:
        rf = pickle.load(f)

    # Charger le préprocesseur
    with open(PREPROCESSOR_PATH, 'rb') as f:
        preprocessor = pickle.load(f)
    
    # Créer le DataFrame d'entrée
    X_input = pd.DataFrame([input_dict], columns=FEATURES)
    X_processed = preprocessor.transform(X_input)
    prediction = rf.predict(X_processed)
    return prediction[0]

def main():
    parser = argparse.ArgumentParser(description="Prédire le type de navire à partir de ses caractéristiques.")
    parser.add_argument('--Status', type=int, required=True, help='Statut du navire')
    parser.add_argument('--Length', type=float, required=True, help='Longueur du navire')
    parser.add_argument('--Width', type=float, required=True, help='Largeur du navire')
    parser.add_argument('--Draft', type=float, required=True, help='Tirant d\'eau du navire')
    parser.add_argument('--Heading', type=float, required=True, help='Cap du navire')

    args = parser.parse_args()
    input_dict = {
        'Status': args.Status,
        'Length': args.Length,
        'Width': args.Width,
        'Draft': args.Draft,
        'Heading': args.Heading
    }
    vessel_type = predict_vessel_type(input_dict)
    print(vessel_type)

if __name__ == '__main__':
    main()