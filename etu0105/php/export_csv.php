<?php
include 'database.php';

ini_set('memory_limit','1024M');

// ⚠️ On utilise ici une jointure entre var et const
$query = "
    SELECT 
        p.MMSI,
        p.BaseDateTime,
        p.LAT,
        p.LON,
        p.SOG,
        p.COG,
        p.Heading,
        p.Status,
        p.Draft,
        n.VesselName,
        n.VesselType,
        n.Length,
        n.Width
    FROM positions p
    LEFT JOIN navires n ON p.MMSI = n.MMSI
";

$data = dbSelect($query);

if (count($data) === 0) {
    die('Aucune donnée à exporter.');
}

// Chemin vers le dossier de destination
$folder = __DIR__ . '/../csv';
if (!is_dir($folder)) {
    mkdir($folder, 0755, true);
}

$filename = 'vessel-clean.csv';
$filepath = $folder . '/' . $filename;

// Écriture du CSV
$output = fopen($filepath, 'w');
$headers = array_keys($data[0]);
fputcsv($output, $headers);

foreach ($data as $row) {
    fputcsv($output, $row);
}

fclose($output);
header('Location: ../prediction_cluster.php');
exit;