// Fonction pour charger les statuts depuis le serveur et remplir le <select name="Status">
async function populateStatusSelect() {
    try {
        const response = await fetch('php/request_status.php?action=getStatuses');
        const data = await response.json();
        console.log("📦 Réponse du serveur pour les statuts :", data);
        if (data.success) {
            const statusList = data.statuses;
            const select = document.querySelector('select[name="Status"]');

            // Vide les anciennes options sauf la première (placeholder)
            if (select) {
                select.length = 1; // garde l'option "--"

                statusList.forEach(status => {
                    const opt = document.createElement('option');
                    opt.value = status.status;            // valeur = id du statut
                    opt.textContent = status.description; // texte = description lisible
                    select.appendChild(opt);
                });
            }
        } else {
            console.error("Erreur serveur lors du chargement des statuts :", data.error);
        }
    } catch (error) {
        console.error("Erreur lors du chargement des statuts :", error);
    }
}

// Appel au chargement DOM pour remplir le select
document.addEventListener('DOMContentLoaded', () => {
    populateStatusSelect();
});

document.getElementById('bababoy').addEventListener('submit', async function (e) {
    e.preventDefault(); // Empêche le rechargement de la page
    console.log('📦 Début de l\'importation');

    try {
         const response = await fetch('php/import_csv.php', {
    method: 'POST'
    });
        if (!response.ok) throw new Error(`Erreur HTTP : ${response.status}`);

        const texte = await response.text(); // Lecture du retour du script PHP
        console.log("✅ Réponse du script Python via PHP :", texte);


    } catch (err) {
        console.error('❌ Erreur lors de l\'importation :', err);
        alert('Erreur lors de l\'importation. Voir la console pour plus de détails.');
    }
});

document.getElementById('mmsiInput').addEventListener('input', async function () {
    const term = this.value;

    if (term.length < 3) return; // Ne cherche qu'à partir de 3 caractères

    try {
        const response = await fetch(`php/navire.php?action=searchMmsi&term=${term}`);
        const data = await response.json();

        if (data.success) {
            const datalist = document.getElementById('mmsiSuggestions');
            datalist.innerHTML = ''; // Reset

            data.results.forEach(mmsi => {
                const option = document.createElement('option');
                option.value = mmsi;
                datalist.appendChild(option);
            });
        }
    } catch (error) {
        console.error('Erreur lors de la récupération des suggestions MMSI :', error);
    }
});

document.getElementById('addShipForm').addEventListener('submit', async function (e) {
    e.preventDefault();

    const errors = [];

    // Récupération des champs
    const MMSI = this.MMSI.value.trim();
    const BaseDateTime = this.BaseDateTime.value.trim();
    const LAT = parseFloat(this.LAT.value.trim());
    const LON = parseFloat(this.LON.value.trim());
    const SOG = parseFloat(this.SOG.value.trim());
    const COG = parseFloat(this.COG.value.trim());
    const Heading = parseFloat(this.Heading.value.trim());
    const VesselName = this.VesselName.value.trim();
    const Status = this.Status.value.trim();
    const Length = parseFloat(this.Length.value.trim());
    const Width = parseFloat(this.Width.value.trim());
    const Draft = parseFloat(this.Draft.value.trim());

    // Vérifications
    if (!/^\d{9}$/.test(MMSI)) {
        errors.push("Le MMSI doit contenir exactement 9 chiffres.");
    }

    if (!/^\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}$/.test(BaseDateTime)) {
        errors.push("La date doit être au format ISO 8601 (ex: 2023-05-24 22:07:27).");
    }

    if (isNaN(LAT) || LAT < -90 || LAT > 90) {
        errors.push("Latitude invalide (doit être entre -90 et 90).");
    }

    if (isNaN(LON) || LON < -180 || LON > 180) {
        errors.push("Longitude invalide (doit être entre -180 et 180).");
    }

    if (isNaN(SOG) || SOG < 0) {
        errors.push("SOG (vitesse) doit être un nombre positif.");
    }

    if (isNaN(Heading) || (Heading !== 511 && (Heading < 0 || Heading > 360))) {
    errors.push("Heading doit être entre 0 et 360, ou égal à 511 (valeur inconnue).");
}

    if (isNaN(Heading) || Heading < 0 || Heading > 360) {
        errors.push("Heading (direction) doit être entre 0 et 360.");
    }

    if (VesselName === "") {
        errors.push("Le nom du navire est requis.");
    }

    if (Status === "" || isNaN(Status) || Status < 0 || Status > 15) {
        errors.push("Le status doit être un nombre entre 0 et 15.");
    }

    if (isNaN(Length) || Length <= 0) {
        errors.push("La longueur doit être un nombre positif.");
    }

    if (isNaN(Width) || Width <= 0) {
        errors.push("La largeur doit être un nombre positif.");
    }

    if (isNaN(Draft) || Draft < 0) {
        errors.push("Le tirant d'eau doit être un nombre positif ou nul.");
    }

    // Affichage des erreurs
    if (errors.length > 0) {
        alert("Erreur(s) dans le formulaire :\n\n" + errors.join("\n"));
        return; // ne continue pas
    }

    // Données valides : envoi à PHP
    const data = {
        MMSI,
        BaseDateTime,
        LAT,
        LON,
        SOG,
        COG,
        Heading,
        VesselName,
        Status,
        Length,
        Width,
        Draft
    };

    try {
        const res = await fetch('php/navire.php', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(data)
        });

        const result = await res.json();
        if (result.success) {
            alert('Navire ajouté avec succès !');
            this.reset();
        } else {
            alert('Erreur lors de l\'ajout du navire :\n' + (result.message || 'Erreur inconnue.'));
        }
    } catch (err) {
        alert('Erreur réseau ou serveur : ' + err.message);
    }
});

document.querySelector('input[name="MMSI"]').addEventListener('change', function() {
    const mmsi = this.value;
    if (mmsi.length === 9) {  // vérifier que c'est bien 9 chiffres
        console.log(`🔍 Recherche navire pour MMSI: ${mmsi}`);
        fetch(`php/get_navire.php?MMSI=${mmsi}`)
            .then(response => response.json())
            .then(data => {
                if (data) {
                    document.querySelector('input[name="VesselName"]').value = data.VesselName || '';
                    document.querySelector('input[name="Length"]').value = data.Length || '';
                    document.querySelector('input[name="Width"]').value = data.Width || '';
                } else {
                    // Si pas trouvé, vider les champs (optionnel)
                    document.querySelector('input[name="VesselName"]').value = '';
                    document.querySelector('input[name="Length"]').value = '';
                    document.querySelector('input[name="Width"]').value = '';
                }
            })
            .catch(err => {
                console.error('Erreur récupération navire:', err);
            });
    }
});
