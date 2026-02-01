<?php
// Titre de la page
$pageTitle = 'Visualiser Navire';

// Inclure l'en-tête
include('php/header.php');
?>
<body>
<?php include('php/navbar.php'); ?>

<div class="main-container">
  <h1 style="text-align: center; margin-bottom: 20px;">Visualisation des Navires</h1>

  <!-- Carte Leaflet -->
  <div class="table-card" style="margin-bottom: 30px;">
    <div class="card-header">Carte des Trajectoires</div>
    <div class="card-body">
      <div id="shipMap"></div>
    </div>
    <div class="card-footer">
      ℹ️ Cliquez sur un point pour voir les détails
    </div>
  </div>

  <!-- Filtres -->
  <div class="table-card" style="margin-bottom: 20px;">
    <div class="card-header">Filtres</div>
    <div class="card-body">
      <div class="filter-container">
        <div class="filter-group">
          <label for="shipNameFilter">Nom du navire :</label>
          <input type="text" id="shipNameFilter" class="filter-input" placeholder="Rechercher par nom...">
        </div>
        
        <div class="filter-group">
          <label for="statusFilter">Statut :</label>
          <select id="statusFilter" class="filter-select">
            <option value="">Tous les statuts</option>
          </select>

        </div>
      </div>
    </div>
  </div>

  <!-- Tableau -->
  <div class="table-card">
    <div class="card-header">Liste des Bateaux</div>
    <div class="card-body">
      <div class="table-container">
        <table id="shipTable">
          <thead>
            <tr>
              <th class="radio-column">Sélection</th>
              <th>MMSI</th>
              <th>Date</th>
              <th>Latitude</th>
              <th>Longitude</th>
              <th>Vitesse</th>
              <th>Cap</th>
              <th>Nom</th>
              <th>État</th>
              <th>Longueur</th>
              <th>Largeur</th>
              <th>Tirant d'eau</th>
            </tr>
          </thead>
          <tbody>
            <!-- Données injectées par JS -->
          </tbody>
        </table>
      </div>
    </div>
  </div>

  <!-- Boutons -->
  <div class="btn-group">
    <button id="btnCluster" class="btn">Prédire les clusters</button>
    <button id="btnType" class="btn">Prédire le type</button>
    <button id="btnTrajectoire" class="btn">Prédire la trajectoire</button>
  </div>
</div>
<button id="scrollToBottom" class="back-to-bottom">
    <svg class="arrow-icon" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" aria-hidden="true" focusable="false">
    <polyline points="6 9 12 15 18 9" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
  </svg>
</button>

<?php include('php/footer.php'); ?>

<!-- Leaflet -->
<script src="https://unpkg.com/leaflet/dist/leaflet.js"></script>
<!-- JS personnalisé -->
<script src="js/visualiser_navire.js"></script>


</body>
</html>
