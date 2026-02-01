<?php
// Titre de la page
$pageTitle = 'Prédiction Trajectoire';

// Inclure l'en-tête
include('php/header.php');
?>
<body>
    <?php include('php/navbar.php'); ?>

    <div class="main-container">
  <h1 style="text-align: center; margin-bottom: 20px;">Prédiction trajectoire du navire</h1>

        <div class="prediction-card">
            <div class="card-header">
                <svg viewBox="0 0 24 24" width="20" height="20" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                    <circle cx="12" cy="12" r="10"></circle>
                    <line x1="12" y1="16" x2="12" y2="12"></line>
                    <line x1="12" y1="8" x2="12.01" y2="8"></line>
                </svg>
                Caractéristiques du navire
            </div>
            <div class="card-body">
                <div id="shipData">
                    <div class="loading">
                        <div class="spinner"></div>
                        <p>Chargement des données du navire...</p>
                    </div>
                </div>
            </div>
        </div>

        <div class="prediction-card">
            <div class="card-header">
                <svg viewBox="0 0 24 24" width="20" height="20" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                    <line x1="18" y1="20" x2="18" y2="10"></line>
                    <line x1="12" y1="20" x2="12" y3="4"></line>
                    <line x1="6" y1="20" x2="6" y2="14"></line>
                </svg>
                Résultat de la prédiction
            </div>
            <div class="card-body">
                <div id="trajectoryPrediction" class="loading">
                    <div class="spinner"></div>
                    <p>Analyse des données en cours...</p>
                </div>
            </div>
            <div class="card-footer">
                <small>Analyse effectuée le <?php echo date('d/m/Y à H:i'); ?></small>
                <a href="visualiser_navire.php" class="btn">
                    <svg viewBox="0 0 24 24" width="16" height="16" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                        <line x1="19" y1="12" x2="5" y2="12"></line>
                        <polyline points="12 19 5 12 12 5"></polyline>
                    </svg>
                    Retour à la liste
                </a>
            </div>
        </div>
    </div>

    <?php include('php/footer.php'); ?>

    <script src="js/prediction_trajectoire.js"></script>
</body>
</html>