<?php
// Titre de la page
$pageTitle = 'Ajouter un navire';

// Inclure l'en-tête
include('php/header.php');
?>
<body>
    <?php include('php/navbar.php'); ?>
    <div class="main-container">
        <h1 style="text-align: center; margin-bottom: 20px;">Ajouter un point de donnée</h1>
        <div class="form-container-ship">
            <form id="bababoy">
                <button class="btn form-ship-button" type="submit">Importer les données</button>
            </form>
            <form id="addShipForm">
                <label class="form-ship-label">MMSI</label>
                <input class="form-ship-input" id="mmsiInput" list="mmsiSuggestions" type="text" name="MMSI" pattern="\d{9}" title="9 chiffres requis" required>
                <datalist id="mmsiSuggestions"></datalist>
                
                <label class="form-ship-label">DATE</label>
                <input class="form-ship-input" type="text" name="BaseDateTime" pattern="\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}" title="Format ISO: 2023-05-24 22:07:27" required>

                <label class="form-ship-label">LAT</label>
                <input class="form-ship-input" type="number" name="LAT" min="-90" max="90" step="0.00001" required>

                <label class="form-ship-label">LON</label>
                <input class="form-ship-input" type="number" name="LON" min="-180" max="180" step="0.00001" required>

                <label class="form-ship-label">SOG</label>
                <input class="form-ship-input" type="number" name="SOG" min="0" step="0.1" required>

                <label class="form-ship-label">COG</label>
                <input class="form-ship-input" type="number" name="COG" min="0" max="359.99" step="0.1" required>

                <label class="form-ship-label">HEADING</label>
                <input class="form-ship-input" type="number" name="Heading" step="1" min="0" max="511" title="Entre 0 et 359 ou 511 si inconnu" required>

                <label class="form-ship-label">NOM</label>
                <input class="form-ship-input" type="text" name="VesselName" required>

                <label class="form-ship-label">STATUS</label>
                <select id="statusSelect" class="form-ship-select" name="Status" required>
                    <option value="">--</option>
                </select>
                </select>

                <label class="form-ship-label">LONGUEUR</label>
                <input class="form-ship-input" type="number" name="Length" min="1" step="0.1" required>

                <label class="form-ship-label">LARGEUR</label>
                <input class="form-ship-input" type="number" name="Width" min="1" step="0.1" required>

                <label class="form-ship-label">TIRANT D'EAU</label>
                <input class="form-ship-input" type="number" name="Draft" min="0" step="0.1" required>

                <button class="btn form-ship-button" type="submit">Ajouter</button>
            </form>
        </div>

    </div>
    
    
    <?php include('php/footer.php'); ?>
    <script src="js/ajout_navire.js"></script>
</body>
</html>
