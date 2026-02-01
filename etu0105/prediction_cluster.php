<?php
// Titre de la page
$pageTitle = 'Prédiction cluster';

// Inclure l'en-tête
include('php/header.php');
?>
<body>
    <?php include('php/navbar.php'); ?>
    <div class="main-container">
  <h1 style="text-align: center; margin-bottom: 20px;">Cluster des navires</h1>
    <?php
        if (isset($_POST['run_cluster'])) {
            $script = __DIR__ . '/python/visualization_map.py';
            $csv = __DIR__ . '/csv/vessel-clean.csv';
            $cmd = "python3 $script --csv_path $csv 2>&1";
            $output = shell_exec($cmd);
            // Affiche la sortie du script (optionnel)
           //if (!empty(trim($output))) {
             //   echo "<div class='python-output'><pre>" . htmlspecialchars($output) . "</pre></div>";
           //}
            // Affiche la carte générée dans un iframe
            echo '<div class="map-container" style="width:100%; max-width:900px; margin:auto;">
                <iframe src="map/cluster_map.html" width="100%" height="600" style="border:none; border-radius:10px;"></iframe>
            </div>';
        }
    ?>
        <form method="post">
            <button type="submit" name="run_cluster" class="btn form-ship-button">
                Prédire les clusters
            </button>
        </form>
    </div>
    <?php include('php/footer.php'); ?>
    <!-- <script src="js/prediction_cluster.js"></script> -->
</body>
</html>
