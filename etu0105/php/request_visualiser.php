<?php
require_once 'database.php';
header('Content-Type: application/json');
ini_set('memory_limit', '2048M');

$action = $_GET['action'] ?? null;

try {
    $db = dbConnect();

    switch ($action) {
        case 'getShips':
            echo json_encode([
                'success' => true,
                'ships' => getShips($db),
                'lastUpdate' => date('Y-m-d H:i:s')
            ]);
            break;

        case 'getTrajectories':
            echo json_encode([
                'success' => true,
                'trajectories' => getTrajectories($db)
            ]);
            break;

        default:
            http_response_code(400);
            echo json_encode([
                'success' => false,
                'error' => 'Action invalide. Utiliser action=getShips ou action=getTrajectories.'
            ]);
    }

} catch (Exception $e) {
    http_response_code(500);
    echo json_encode([
        'success' => false,
        'error' => 'Erreur serveur : ' . $e->getMessage()
    ]);
}

// --- FONCTIONS ---

/**
 * @param PDO $db
 * @return array
 *
 * La fonction getShips prend en paramètre un objet PDO $db
 * représentant la connexion à la base de données.
 *
 * La fonction renvoie un tableau de 200 éléments maximum, correspondant
 * aux 200 dernières positions connues des navires. Chaque élément du
 * tableau est un tableau associatif contenant les éléments suivants :
 *   - 'mmsi' : le MMSI du navire
 *   - 'BaseDateTime' : la date et l'heure de la donnée
 *   - 'latitude' : la latitude de la donnée
 *   - 'longitude' : la longitude de la donnée
 *   - 'sog' : la vitesse sur le fond (null si inconnue)
 *   - 'cog' : la direction de route (null si inconnue)
 *   - 'heading' : l'orientation du navire (null si inconnue)
 *   - 'vesselName' : le nom du navire
 *   - 'status' : l'état du navire (null si inconnu)
 *   - 'Length' : la longueur du navire
 *   - 'Width' : la largeur du navire
 *   - 'VesselType' : le type de navire
 *   - 'Draft' : la tirant d'eau
 *
 * Les éléments du tableau sont triés par BaseDateTime décroissante.
 */
function getShips(PDO $db): array {
    $query = "
        SELECT  
    v.MMSI AS mmsi,
    v.BaseDateTime AS BaseDateTime,
    v.LAT AS latitude,
    v.LON AS longitude,
    v.SOG AS sog,
    v.COG AS cog,
    v.Heading AS heading,
    c.VesselName AS vesselName,
    v.Status AS status,
    c.Length AS Length,
    c.Width AS Width,
    c.VesselType,
    v.Draft AS Draft
FROM (
    SELECT MMSI, MAX(BaseDateTime) AS last_update 
    FROM positions
    GROUP BY MMSI
) AS latest
LEFT JOIN positions v ON v.MMSI = latest.MMSI AND v.BaseDateTime = latest.last_update
LEFT JOIN navires c ON c.MMSI = latest.MMSI
ORDER BY v.BaseDateTime DESC
LIMIT 200;

    ";

    $stmt = $db->query($query);
    return $stmt->fetchAll(PDO::FETCH_ASSOC);
}

    /**
     * @param PDO $db
     * @return array
     *
     * La fonction getTrajectories prend en paramètre un objet PDO $db
     * représentant la connexion à la base de données.
     *
     * La fonction renvoie un tableau associatif $trajectories dont les clés
     * sont les MMSI des navires, et les valeurs sont des tableaux de
     * trajectoires.
     *
     * Chaque trajectoire est un tableau associatif contenant les éléments
     * suivants :
     *   - 'BaseDateTime' : la date et l'heure de la donnée
     *   - 'LAT' : la latitude de la donnée
     *   - 'LON' : la longitude de la donnée
     *   - 'VesselName' : le nom du navire
     *   - 'Status' : l'état du navire (null si inconnu)
     *   - 'SOG' : la vitesse sur le fond (null si inconnue)
     *   - 'COG' : la direction de route (null si inconnue)
     *   - 'Draft' : la tirant d'eau (null si inconnue)
     *
     * Les trajectoires sont triées par BaseDateTime croissante.
     */
function getTrajectories(PDO $db): array {
    $query = "
        SELECT 
        v.MMSI AS MMSI,
        v.BaseDateTime AS BaseDateTime,
        v.LAT,
        v.LON,
        COALESCE(c.VesselName, '') AS VesselName,
        v.Status,
        v.SOG,
        v.COG,
        v.Draft
    FROM positions v
    LEFT JOIN navires c ON v.MMSI = c.MMSI
    ORDER BY v.MMSI, v.BaseDateTime;

    ";

    $results = $db->query($query);
    $trajectories = [];

    while ($row = $results->fetch(PDO::FETCH_NUM)) {
        $trajectories[$row[0]][] = [
            'BaseDateTime' => $row[1],
            'LAT'          => (float)$row[2],
            'LON'          => (float)$row[3],
            'VesselName'   => $row[4],
            'Status'       => $row[5] !== null ? (int)$row[5] : null,
            'SOG'          => $row[6] !== null ? (float)$row[6] : null,
            'COG'          => $row[7] !== null ? (float)$row[7] : null,
            'Draft'        => $row[8] !== null ? (float)$row[8] : null
        ];
    }

    return $trajectories;
}
