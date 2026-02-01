// ==========================
// Configuration globale
// ==========================

// Icônes SVG utilisés dans l'interface
const ICONS = {
    arrowLeft: `<svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
        <line x1="19" y1="12" x2="5" y2="12"></line>
        <polyline points="12 19 5 12 12 5"></polyline>
    </svg>`
};

// ==========================
// Variables et fonctions pour gérer les statuts dynamiques
// ==========================

let statusList = [];

/**
 * Charge la liste des statuts depuis le serveur (endpoint PHP).
 */
async function loadStatuses() {
    try {
        const response = await fetch('php/request_status.php?action=getStatuses');
        const data = await response.json();
        if (data.success) {
            statusList = data.statuses; // Tableau d'objets { status: "0", description: "En route avec moteur" }, etc.
            console.log("Statuts chargés :", statusList);
        } else {
            console.error("Erreur serveur lors du chargement des statuts :", data.error);
        }
    } catch (error) {
        console.error("Erreur lors du chargement des statuts :", error);
    }
}

/**
 * Récupère la description du statut via son ID à partir de statusList.
 * @param {number|string} statusId - L'identifiant numérique du statut.
 * @returns {string} La description du statut ou "Inconnu".
 */
function getStatusDescription(statusId) {
    const statusStr = String(statusId);
    const statusObj = statusList.find(s => s.status === statusStr);
    if (statusObj) return statusObj.description;
    return "Inconnu";
}

// ==========================
// Fonctions utilitaires existantes
// ==========================

function getShipParams() {
    const params = new URLSearchParams(location.search);
    const MMSI = params.get('MMSI'); // Identifiant obligatoire

    const keys = ['Status', 'Length', 'Width', 'Draft', 'Heading'];
    const parsed = Object.fromEntries(keys.map(k => [k, parseFloat(params.get(k))]));

    if (!MMSI || Object.values(parsed).some(isNaN)) {
        throw new Error('Paramètres invalides ou manquants');
    }

    return { MMSI, ...parsed };
}

function setHTML(id, html, className = '') {
    const el = document.getElementById(id);
    if (el) {
        el.className = className;
        el.innerHTML = html;
    }
}

/**
 * Affiche les données du navire, en utilisant getStatusDescription pour le statut.
 */
function displayShipData({ MMSI, Status, Length, Width, Draft, Heading }) {
    const statusDescription = getStatusDescription(Status);
    setHTML('shipData', `
        <table class="data-table">
            <tr><th>MMSI</th><td>${MMSI}</td></tr>
            <tr><th>Statut</th><td>${statusDescription}</td></tr>
            <tr><th>Longueur</th><td>${Length.toFixed(1)} m</td></tr>
            <tr><th>Largeur</th><td>${Width.toFixed(1)} m</td></tr>
            <tr><th>Tirant d'eau</th><td>${Draft.toFixed(1)} m</td></tr>
            <tr><th>Cap</th><td>${Heading.toFixed(1)}°</td></tr>
        </table>
    `, 'data-container');
}

async function predictShipType(payload) {
    const res = await fetch('php/request_prediction.php?type', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(payload)
    });

    const text = await res.text();
    const data = text ? JSON.parse(text) : {};

    if (!res.ok) throw new Error(data.error || `HTTP Error ${res.status}`);

    return data;
}

function displayPredictionResult({ type, predicted_type }) {
    setHTML('typePrediction', `
        <h3>Type prédit : ${type || predicted_type || 'Inconnu'}</h3>
        <div class="prediction-details"><p>Basé sur l'analyse des caractéristiques du navire</p></div>
    `, 'prediction-result');
}

function displayError(error) {
    const html = `
        <h3>Erreur lors de l'analyse</h3>
        <p>${error.message || 'Une erreur inattendue est survenue'}</p>
        <button onclick="location.reload()" class="btn">${ICONS.arrowLeft} Réessayer</button>
    `;
    setHTML('typePrediction', html, 'error-message');
}

// ==========================
// Point d'entrée principal
// ==========================

document.addEventListener('DOMContentLoaded', async () => {
    try {
        // Charge d'abord les statuts depuis le serveur
        await loadStatuses();

        const payload = getShipParams();  // Récupère les paramètres URL

        displayShipData(payload);          // Affiche les données avec statuts dynamiques

        // Affiche un loader pendant la prédiction
        setHTML('typePrediction', `
            <div class="loading">
                <div class="spinner"></div>
                <p>Analyse des données en cours...</p>
            </div>
        `);

        const result = await predictShipType(payload); // Appel backend
        displayPredictionResult(result);                // Affiche résultat
    } catch (error) {
        displayError(error);
    }
});
