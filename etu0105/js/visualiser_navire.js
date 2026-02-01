// ==========================
// Configuration de l'application
// ==========================
const CONFIG = {
    refreshInterval: 30000,        // Intervalle de rafraîchissement des données (en ms)
    mapCenter: [25.0, -90.0],      // Coordonnées initiales du centre de la carte
    mapZoom: 5                     // Niveau de zoom initial de la carte
};

// ==========================
// État global de l'application
// ==========================
const state = {
    shipsData: [],                 // Tableau des données des navires
    selectedShipId: null,          // MMSI du navire sélectionné
    map: null,                     // Instance de la carte Leaflet
    colorMap: {},                  // Association MMSI => couleur unique
    filters: { shipName: '', status: '' },  // Filtres appliqués (nom, statut)
    lastLoadedMmsi: null           // MMSI du dernier navire dont les trajectoires ont été chargées
};

// ==========================
// Initialisation de la carte Leaflet
// ==========================
/**
 * Initialise la carte Leaflet dans l'élément HTML #shipMap.
 * @function
 */
function initMap() {
    // Crée l'instance de la carte Leaflet avec le centre et le zoom initial
    state.map = L.map('shipMap', {
        scrollWheelZoom: false
    }).setView(CONFIG.mapCenter, CONFIG.mapZoom);

    // Ajout des tuiles OpenStreetMap
    L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
        // Niveau de zoom maximum
        maxZoom: 18,
        // Mention légale
        attribution: '  OpenStreetMap'
    }).addTo(state.map);
}

// ==========================
// Chargement des données navires depuis le serveur
// ==========================
/**
 * Charge les données des navires depuis le serveur.
 * Met à jour l'état de l'application avec les navires reçus
 * et applique les filtres actifs avant de mettre à jour l'affichage.
 * @async
 */
async function loadShips() {
    try {
        const res = await fetch('php/request_visualiser.php?action=getShips');
        const data = await res.json();
        state.shipsData = data.ships;  // Stocke les navires reçus

        // Applique les filtres et met à jour l'affichage
        applyFilters();
    } catch (err) {
        console.error('Erreur:', err);
    }
}

// ==========================
// Filtrage des navires selon les critères sélectionnés
// ==========================
/**
 * Applique les filtres actifs aux données des navires.
 * Met à jour la liste filtrée des navires, le tableau HTML
 * et recharge les trajectoires des navires visibles.
 */
function applyFilters() {
    // Filtre les navires en fonction des filtres appliqués
    state.filteredShips = state.shipsData.filter(matchesFilters);

    // Met à jour la table HTML des navires avec la liste filtrée
    updateShipTable();

    // Charge et affiche les trajectoires des navires filtrés/sélectionnés
    loadTrajectories();
}

// Vérifie si un navire correspond aux filtres actifs
/**
 * Vérifie si les données d'un navire correspondent aux filtres actifs.
 * @param {Object} ship - Les données du navire
 * @returns {boolean} True si le navire correspond aux filtres, false sinon
 */
function matchesFilters(ship) {
    const { shipName, status } = state.filters;
    // Vérifie si le nom du navire contient le texte de recherche (insensible à la casse)
    // et si le statut du navire correspond au filtre de statut (ou est vide)
    return (!shipName || ship.vesselName?.toLowerCase().includes(shipName.toLowerCase())) &&
           (!status || getStatus(ship.status).description === status);
}

// ==========================
// Génération du HTML d'une ligne de navire dans la table
// ==========================
/**
 * Génère le HTML d'une ligne de navire dans la table.
 * @param {Object} ship - Les données du navire
 * @returns {string} Le HTML de la ligne
 */
function shipRow(ship) {
    const isSelected = state.selectedShipId === ship.mmsi;
    const color = getColor(ship.mmsi);
    return `
        <tr data-mmsi="${ship.mmsi}" class="${isSelected ? 'selected' : ''}">
            <td class="radio-column">
                <!-- Bouton radio pour sélectionner le navire -->
                <input type="radio" name="selectedShip" value="${ship.mmsi}" ${isSelected ? 'checked' : ''}>
            </td>
            <td>
                <!-- Indicateur de couleur (unique par navire) -->
                <span class="color-dot" style="background-color: ${color}"></span>
                ${ship.mmsi}
            </td>
            <td>${formatDate(ship.BaseDateTime)}</td>
            <td>${formatCoord(ship.latitude)}</td>
            <td>${formatCoord(ship.longitude)}</td>
            <td>${formatNumber(ship.sog, 1)}</td>
            <td>${formatNumber(ship.cog, 1)}°</td>
            <td>${ship.vesselName || 'Inconnu'}</td>
            <td>${getStatus(ship.status).description}</td>
            <td>${formatNumber(ship.Length, 1)}m</td>
            <td>${formatNumber(ship.Width, 1)}m</td>
            <td>${formatNumber(ship.Draft, 1)}m</td>
        </tr>`;
}

// ==========================
// Mise à jour du tableau HTML des navires
// ==========================
/**
 * Met à jour le tableau HTML des navires en fonction de la liste filtrée.
 * Génère le HTML de chaque ligne en utilisant la fonction shipRow, puis ajoute
 * les événements sur chaque ligne pour gérer la sélection d'un navire.
 */
function updateShipTable() {
    const tbody = document.querySelector('#shipTable tbody');
    tbody.innerHTML = state.filteredShips.map(shipRow).join('');
    tbody.querySelectorAll('tr').forEach(setupRowEvents);  // Ajoute événements sur chaque ligne
}

// ==========================
// Configuration des événements sur une ligne (sélection du navire)
// ==========================
/**
 * Configure les événements sur une ligne de la table des navires.
 * @param {HTMLElement} row - L'élément <tr> de la ligne de la table
 */
function setupRowEvents(row) {
    const radio = row.querySelector('input[type="radio"]');

    // Fonction pour gérer la sélection d'un navire
    /**
     * Fonction appelée lorsque le navire est sélectionné (ou dé-sélectionné).
     * Met à jour l'état de l'application, les classes CSS des lignes de la table
     * et recharge les trajectoires du navire sélectionné.
     */
    const selectRow = () => {
        state.selectedShipId = radio.value;
        // Mise à jour visuelle des lignes sélectionnées
        document.querySelectorAll('#shipTable tr').forEach(r => r.classList.toggle('selected', r === row));
        loadTrajectories();  // Recharge les trajectoires du navire sélectionné
    };

    radio.onchange = selectRow;

    // Clic sur la ligne active aussi la sélection radio (sauf si clic sur l'input lui-même)
    row.onclick = e => {
        if (e.target.tagName !== 'INPUT') {
            radio.checked = true;
            radio.dispatchEvent(new Event('change'));
        }
    };
}

// ==========================
// Chargement et affichage des trajectoires des navires filtrés / sélectionnés
// ==========================
/**
 * Charge les trajectoires des navires filtrés/sélectionnés et les affiche sur la carte.
 * Les trajectoires sont filtrées en fonction des navires visibles et sélectionnés.
 * Si un navire est sélectionné, seules les trajectoires de ce navire sont affichées.
 * Si aucun navire n'est sélectionné, toutes les trajectoires sont affichées.
 * La fonction essaie de charger les données via un appel AJAX, puis filtre les trajectoires
 * en fonction des navires visibles/sélectionnés et les ajoute sur la carte.
 * @async
 */
async function loadTrajectories() {
    try {
        // Évite de recharger si les données sont déjà chargées pour ce navire
        if (state.selectedShipId && state.lastLoadedMmsi === state.selectedShipId) return;

        state.lastLoadedMmsi = state.selectedShipId || null;

        const res = await fetch('php/request_visualiser.php?action=getTrajectories');
        const data = await res.json();
        if (!data.success) return;

        // Suppression des anciennes trajectoires de la carte
        state.map.eachLayer(layer => {
            if (layer instanceof L.Polyline) state.map.removeLayer(layer);
        });

        // Filtrage des trajectoires selon les navires visibles/sélectionnés
        const filtered = getFilteredTrajectories(data.trajectories);
        const visiblePoints = [];

        // Ajout des nouvelles trajectoires sur la carte
        for (const [mmsi, points] of Object.entries(filtered)) {
            const coords = points.map(p => [p.LAT, p.LON]);
            visiblePoints.push(...coords);

            // Recherche des infos navire pour popup
            const ship = state.shipsData.find(s => String(s.mmsi) === mmsi);

            // Création d'une ligne colorée sur la carte
            const line = L.polyline(coords, { color: getColor(mmsi), weight: 3 }).addTo(state.map);

            // Ajout popup infos sur trajectoire
            line.bindPopup(`
                <div class="ship-popup">
                    <div><strong>MMSI :</strong> ${mmsi}</div>
                    <div><strong>Nom :</strong> ${ship.vesselName}</div>
                    <div><strong>Longueur :</strong> ${formatNumber(ship.Length, 1)}m</div>
                    <div><strong>Largeur :</strong> ${formatNumber(ship.Width, 1)}m</div>
                    <div><strong>Tirant d'eau :</strong> ${formatNumber(ship.Draft, 1)}m</div>
                    <div><strong>Statut :</strong> ${getStatus(ship.status).description}</div>
                </div>
            `).on('click', () => {
        // 1. Met à jour l’état sélectionné
        state.selectedShipId = String(mmsi);

        // 2. Décoche tous les autres radios
        document.querySelectorAll('input[name="selectedShip"]').forEach(input => {
            input.checked = input.value === state.selectedShipId;
        });

        // 3. Met à jour visuellement les lignes
        document.querySelectorAll('#shipTable tr').forEach(r => {
            const isSelected = r.getAttribute('data-mmsi') === state.selectedShipId;
            r.classList.toggle('selected', isSelected);
        });

        // 4. Recharge les trajectoires
        loadTrajectories();
    });
        }

        // Ajuste la vue de la carte pour englober toutes les trajectoires visibles
        if (visiblePoints.length > 0) {
            state.map.fitBounds(L.latLngBounds(visiblePoints));
        }
    } catch (err) {
        console.error('Erreur:', err);
    }
}

// ==========================
// Filtrage des trajectoires à afficher selon sélection/filtres
// ==========================
/**
 * Filtre les trajectoires à afficher en fonction des navires visibles et sélectionnés.
 * @param {Object<string, Array<{LAT: number, LON: number}>>} allTrajectories - Trajectoires brutes issues du serveur
 * @returns {Object<string, Array<{LAT: number, LON: number}>>} - Trajectoires filtrées à afficher
 */
function getFilteredTrajectories(allTrajectories) {
    return Object.entries(allTrajectories).reduce((acc, [mmsi, points]) => {
        const ship = state.shipsData.find(s => String(s.mmsi) === mmsi);

        // Conditions :
        // - trajectoire non vide
        // - correspond au navire sélectionné ou tous
        // - navire existe
        // - correspond aux filtres
        if (points?.length && (!state.selectedShipId || String(mmsi) === String(state.selectedShipId)) && ship && matchesFilters(ship)) {
            acc[mmsi] = points;
        }
        return acc;
    }, {});
}

// ==========================
// Configuration des boutons d'action et leur comportement
// ==========================
/**
 * Configure les boutons d'action et leur comportement.
 * Les boutons sont liés à des fonctions qui nécessitent une sélection de navire.
 */
function setupButtons() {
    // Actions qui nécessitent une sélection de navire
    const actions = {
        // Bouton "Trajectoire"
        'btnTrajectoire': () => {
            const s = state.shipsData.find(ship => ship.mmsi === state.selectedShipId);
            if (!s) return alert('Navire introuvable');
            const params = new URLSearchParams({
                MMSI: s.mmsi,
                Length: s.Length, Width: s.Width,
                Draft: s.Draft || 0, Heading: s.heading || 0,
                LAT: s.latitude, LON: s.longitude,
                SOG: s.sog || 0, COG: s.cog || 0,
                VesselType: s.VesselType || 0
            });
            // Redirection vers la page de prédiction de trajectoire avec les paramètres
            redirectIfSelected(`prediction_trajectoire.php?${params}`);
        },

        // Bouton "Type"
        'btnType': () => {
            const s = state.shipsData.find(ship => ship.mmsi === state.selectedShipId);            
            if (!s) return alert('Navire introuvable');
            const params = new URLSearchParams({
                MMSI: s.mmsi, Status: s.status,
                Length: s.Length, Width: s.Width,
                Draft: s.Draft || 0, Heading: s.heading || 0
            });
            // Redirection vers la page de prédiction de type avec les paramètres
            redirectIfSelected(`prediction_type.php?${params}`);
        }
    };

    // Liaison des boutons nécessitant une sélection
    Object.entries(actions).forEach(([id, fn]) => {
        const btn = document.getElementById(id);
        if (btn) {
            // Si le bouton existe, on lie son événement onclick à la fonction associée
            btn.onclick = () => state.selectedShipId ? fn() : alert('Veuillez sélectionner un navire');
        }
    });

    // Bouton Cluster (pas besoin de sélection)
    const btnCluster = document.getElementById('btnCluster');
    if (btnCluster) {
        btnCluster.onclick = () => {
            fetch('php/export_csv.php', {
                method: 'GET'
            })
            .then(response => {
                if (!response.ok) {
                    throw new Error('Erreur serveur');
                }
                return response.text();
            })
            .then(data => {
                console.log('CSV généré :', data);
                // Redirection uniquement après réussite
                window.location.href = 'prediction_cluster.php';
            })
            .catch(error => {
                console.error('Erreur lors de la création du CSV :', error);
            });
        };
    }
}


/**
 * Redirection avec vérification qu'un navire est sélectionné
 * @param {string} url - URL de destination
 */
function redirectIfSelected(url) {
    // Vérifie si un navire est sélectionné
    if (!state.selectedShipId) {
        // Si non, affiche un message d'erreur
        alert('Veuillez sélectionner un navire');
    } else {
        // Si oui, redirige vers la page demandée
        window.location.href = url;
    }
}

// ==========================
// Configuration des filtres (nom et statut) avec écoute des événements de changement
// ==========================
/**
 * Configure les filtres de recherche pour le nom et le statut des navires.
 * Ajoute des gestionnaires d'événements pour détecter les changements et appliquer les filtres.
 */
function setupFilters() {
    const nameInput = document.getElementById('shipNameFilter');
    const statusInput = document.getElementById('statusFilter');

    // Ajoute un écouteur d'événement sur le champ de saisie du nom avec une fonction debounce
    // La fonction debounce limite la fréquence d'exécution de l'application des filtres à 300ms après la saisie
    nameInput.addEventListener('input', debounce(e => {
        state.filters.shipName = e.target.value;  // Met à jour le filtre de nom dans l'état
        applyFilters();  // Applique les filtres mis à jour
    }, 300));

    // Ajoute un écouteur d'événement sur le champ de sélection du statut
    statusInput.addEventListener('change', e => {
        state.filters.status = e.target.value || '';  // Met à jour le filtre de statut dans l'état
        applyFilters();  // Applique les filtres mis à jour
    });

    // Ajoute un écouteur d'événement pour déclencher l'application des filtres lors de l'appui sur la touche Entrée
    nameInput.addEventListener('keypress', e => {
        if (e.key === 'Enter') applyFilters();  // Applique les filtres si la touche Entrée est pressée
    });
}

// ==========================
// Fonctions utilitaires
// ==========================

/**
 * Génère une couleur unique pour chaque MMSI en fonction d'un hash simple.
 * @param {string} mmsi - MMSI du navire
 * @returns {string} Couleur unique au format HSL
 */
function getColor(mmsi) {
    // Si la couleur n'est pas encore générée, on la génère
    if (!state.colorMap[mmsi]) {
        // Calcul d'un hash simple à partir du MMSI
        const hash = String(mmsi).split('').reduce((a, c) => c.charCodeAt(0) + ((a << 5) - a), 0);
        // Conversion du hash en couleur HSL aléatoire
        state.colorMap[mmsi] = `hsl(${Math.abs(hash) % 360}, 80%, 50%)`;
    }
    // Retourne la couleur générée
    return state.colorMap[mmsi];
}

// Formatage date au format local français ou 'N/A' si invalide
const formatDate = d => isNaN(new Date(d).getTime()) ? 'N/A' : new Date(d).toLocaleString('fr-FR');

// Formatage nombre avec un certain nombre de décimales ou 'N/A'
const formatNumber = (n, d) => isNaN(parseFloat(n)) ? 'N/A' : parseFloat(n).toFixed(d);

// Formatage coordonnée à 4 décimales
const formatCoord = c => formatNumber(c, 4);

// ==========================
// Chargement des statuts depuis le serveur
// ==========================
let statusList = [];

async function loadStatuses() {
  try {
    const response = await fetch('php/request_status.php?action=getStatuses');
    const data = await response.json();
    if (data.success) {
      statusList = data.statuses; // <-- Ici on prend uniquement le tableau
      console.log("Statuts chargés :", statusList);
    } else {
      console.error("Erreur serveur :", data.error);
    }
  } catch (error) {
    console.error("Erreur lors du chargement des statuts :", error);
  }
}

function populateStatusFilter() {
    const statusSelect = document.getElementById('statusFilter');

    // Supprimer toutes les options sauf la première ("Tous les statuts")
    statusSelect.querySelectorAll('option:not([value=""])').forEach(opt => opt.remove());

    // Ajouter dynamiquement les statuts depuis statusList
    statusList.forEach(statusObj => {
        const option = document.createElement('option');
        option.value = statusObj.description;
        option.textContent = statusObj.description;
        statusSelect.appendChild(option);
    });
}


function getStatus(statusId) {
  const status = statusList.find(s => s.status === String(statusId));
  console.log("Recherche du statut pour l'ID :", statusId, "Résultat :", status);
  return status || { status: String(statusId), description: "Inconnu" };

}


/**
 * Fonction debounce pour limiter la fréquence d'exécution d'une fonction.
 * @param {function} fn - Fonction à exécuter avec un délai.
 * @param {number} delay - Délai d'exécution en millisecondes.
 * @returns {function} Fonction débouncée.
 */
function debounce(fn, delay) {
    let t;
    /**
     * Fonction débouncée.
     * @param {...*} args - Arguments à passer à la fonction fn.
     */
    return (...args) => {
        // Annule le délai précédent si il existe
        clearTimeout(t);
        // Définit un nouveau délai d'exécution
        t = setTimeout(() => fn(...args), delay);
    };
}

// ==========================
// Initialisation au chargement du DOM
// ==========================
document.addEventListener('DOMContentLoaded', async () => {
    const btn = document.getElementById('scrollToBottom');

    btn.onclick = () => {
        window.scrollTo({ top: document.body.scrollHeight, behavior: 'smooth' });
    };

    // Fonction pour vérifier si on est en bas de la page
    const checkScrollPosition = () => {
        const isAtBottom = window.innerHeight + window.scrollY >= document.body.scrollHeight - 2;
        btn.style.display = isAtBottom ? 'none' : 'block';
    };

    // Ajout de l'écouteur sur le scroll
    window.addEventListener('scroll', checkScrollPosition);

    // Appel initial pour cacher/montrer le bouton au chargement
    checkScrollPosition();
    
    initMap();       // Initialise la carte
    setupButtons();  // Configure les boutons d'action
    setupFilters();  // Configure les filtres
    await loadStatuses();
    populateStatusFilter();
    await loadShips();     // Charge les navires initiaux
    setInterval(loadShips, CONFIG.refreshInterval);  // Rafraîchit périodiquement les données
});