<?php
include 'database.php';

if (!isset($_GET['MMSI'])) {
    http_response_code(400);
    echo json_encode(null);
    exit;
}

$mmsi = $_GET['MMSI'];

// Requête pour récupérer les infos du navire
$data = dbSelect('SELECT * FROM navires WHERE MMSI = :mmsi', ['mmsi' => $mmsi]);

if (count($data) > 0) {
    // On renvoie la première ligne en JSON
    header('Content-Type: application/json');
    echo json_encode($data[0]);
} else {
    // Rien trouvé
    http_response_code(404);
    echo json_encode(null);
}
?>