<?php
require_once('database.php');
header('Content-Type: application/json');
$method = $_SERVER['REQUEST_METHOD'];
if ($method === 'POST') {
    // Ajout navire
    $data = json_decode(file_get_contents('php://input'), true);
    // Variables template à adapter selon la structure SQL
    $navire1 = [
        'MMSI' => $data['MMSI'],
        'BaseDateTime' => $data['BaseDateTime'],
        'LAT' => $data['LAT'],
        'LON' => $data['LON'],
        'SOG' => $data['SOG'],
        'COG' => $data['COG'],
        'Heading' => $data['Heading'],
        'Status' => $data['Status'],
        'Draft' => $data['Draft']
    ];
    $ok = dbInsert('positions', $navire1);
    $navire2 = [
        'MMSI' => $data['MMSI'],
        'VesselName' => $data['VesselName'],
        'Length' => $data['Length'],
        'Width' => $data['Width']
    ];
    $ok = dbInsert('navires', $navire2);
    echo json_encode(['success' => $ok]);
    exit;
}

$action = isset($_GET['action']) ? $_GET['action'] : '';
if ($action === 'searchMmsi' && isset($_GET['term'])) {
    $term = $_GET['term'] . '%'; // Commence par

    $query = "
        SELECT DISTINCT MMSI 
        FROM positions 
        WHERE MMSI LIKE :term 
        ORDER BY MMSI 
        LIMIT 10;
    ";

    $results = dbSelect($query, [':term' => $term]);

    $mmsiList = array_map(function($row) {
        return $row['MMSI'];
    }, $results);

    echo json_encode([
        'success' => true,
        'results' => $mmsiList
    ]);
    exit;
}

if ($method === 'GET') {
    // Liste navires
    $navires = dbSelect('navires');
    echo json_encode($navires);
    exit;
} 
echo json_encode(['error' => 'Méthode non supportée']);