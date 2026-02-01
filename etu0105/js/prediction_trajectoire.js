
// ==========================
// Fonctions utilitaires
// ==========================

// Récupère et valide les paramètres d'URL pour un navire
/**
 * Retrieves and validates ship parameters from the URL
 * @returns {Object} An object containing ship parameters
 * @throws Will throw an error if MMSI is missing or if any parameter is NaN
 */
function getShipParams() {
    const params = new URLSearchParams(location.search);

    // Récupère le MMSI, identifiant obligatoire du navire
    const MMSI = params.get('MMSI');

    // Liste des clés numériques à parser
    const keys = ['Length', 'Width', 'Draft', 'Heading', 'SOG', 'COG', 'LAT', 'LON', 'VesselType'];

    // Conversion des valeurs en float
    const parsed = Object.fromEntries(keys.map(k => [k, parseFloat(params.get(k))]));

    // Validation : MMSI présent et pas de NaN dans les valeurs
    if (!MMSI || Object.values(parsed).some(isNaN)) {
        throw new Error('Paramètres invalides ou manquants');
    }

    // Retourne un objet contenant le MMSI et les paramètres convertis
    return { MMSI, ...parsed };
}

// Injecte dynamiquement du HTML dans un élément identifié
/**
 * Replaces the content of an element with the given HTML
 * @param {string} id - The id of the element to replace
 * @param {string} html - The HTML to inject
 * @param {string} [className] - The class to apply to the element (optional)
 */
function setHTML(id, html, className = '') {
    const el = document.getElementById(id);
    if (el) {
        el.className = className;
        el.innerHTML = html;
    }
}

/**
 * Displays the ship's data in a table
 * @param {Object} data - The data to display
 * @param {string} data.MMSI - The ship's MMSI
 * @param {number} data.LAT - The ship's latitude
 * @param {number} data.LON - The ship's longitude
 * @param {number} data.Length - The ship's length
 * @param {number} data.Width - The ship's width
 * @param {number} data.Draft - The ship's draft
 * @param {number} data.Heading - The ship's heading
 * @param {number} data.SOG - The ship's speed
 * @param {number} data.COG - The ship's course over ground
 * @param {string} data.VesselType - The ship's type
 */
function displayShipData({ MMSI, LAT, LON, Length, Width, Draft, Heading, SOG, COG, VesselType }) {
    setHTML('shipData', `
        <table class="data-table">
            <tr><th>MMSI</th><td>${MMSI}</td></tr>
            <tr><th>Longueur</th><td>${Length.toFixed(1)} m</td></tr>
            <tr><th>Largeur</th><td>${Width.toFixed(1)} m</td></tr>
            <tr><th>Tirant d'eau</th><td>${Draft.toFixed(1)} m</td></tr>
            <tr><th>Cap</th><td>${Heading.toFixed(1)}°</td></tr>
            <tr><th>Latitude</th><td>${LAT.toFixed(1)}°</td></tr>
            <tr><th>Longitude</th><td>${LON.toFixed(1)}°</td></tr>
            <tr><th>Vitesse</th><td>${SOG.toFixed(1)} nœuds</td></tr>
            <tr><th>Cap vrai</th><td>${COG.toFixed(1)}°</td></tr>
            <tr><th>Type de navire</th><td>${VesselType}</td></tr>
        </table>
    `, 'data-container');
}

// Appelle le backend PHP pour prédire la trajectoire d'un navire
/**
 * Calls the PHP backend to predict a ship's trajectory
 * @param {Object} payload - The data to send to the backend
 * @returns {Promise<Object>} The response from the backend with the prediction data
 */
async function predictShipTrajectory(payload) {
    
    const res = await fetch('php/request_prediction.php?trajectoire', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(payload)
    });

    const text = await res.text(); // Récupération brute
    console.log('Réponse brute du serveur:', text); // Debug
    const data = text ? JSON.parse(text) : {}; // Tentative de parsing JSON
    if (!res.ok) throw new Error(data.error || `Erreur HTTP ${res.status}`);

    return data;
}


// Affiche la trajectoire de navire prédit par l'IA
/**
 * Displays the predicted ship trajectory by the AI
 * @param {Object} data - The response from the backend with the prediction data
 */
function displayPredictionResult(data) {
    const mapFile = data.mapFile || 'map/single_vessel_prediction_absolute.html';
    setHTML('trajectoryPrediction', `
       <div class="map-container" style="width:100%; max-width:900px; margin:auto;">
           <iframe src="${mapFile}" width="100%" height="600" style="border:none; border-radius:10px;"></iframe>
       </div>
    `, 'prediction-result');
}


/**
 * Displays an error message to the user with an option to retry
 * @param {Error} error - The Error object returned by the rejected promise
 */
function displayError(error) {
    // Format the error message and inject into the HTML
    setHTML('trajectoryPrediction', `
        <h3>Erreur lors de l'analyse</h3>
        <p>${error.message || 'Une erreur inattendue est survenue'}</p>
        <p>Assurez-vous que les données sont correctes et que le serveur est accessible</p>
        <p><button onclick="document.location.reload()">Réessayer</button></p>
    `, 'error-message');
}

// ==========================
// Point d'entrée principal
// ==========================

document.addEventListener('DOMContentLoaded', async () => {
    try {
        const payload = getShipParams();     // Lecture des données URL
        displayShipData(payload);            // Affichage de ces données

        setHTML('trajectoryPrediction', `
            <div class="loading">
                <div class="spinner"></div>
                <p>Analyse des données en cours...</p>
            </div>
        `);

        const result = await predictShipTrajectory(payload); // Appel au backend
        displayPredictionResult(result);   // <-- Passe `result` ici

    } catch (err) {
        displayError(err);
    }
});

