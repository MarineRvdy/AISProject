<?php
require_once 'database.php';
header('Content-Type: application/json');

$action = $_GET['action'] ?? null;

try {
    $db = dbConnect();

    switch ($action) {
        case 'getStatuses':
            echo json_encode([
                'success' => true,
                'statuses' => getStatuses($db)
            ]);
            break;

        default:
            http_response_code(400);
            echo json_encode([
                'success' => false,
                'error' => 'Action invalide. Utiliser action=getStatuses.'
            ]);
    }

} catch (Exception $e) {
    http_response_code(500);
    echo json_encode([
        'success' => false,
        'error' => 'Erreur serveur : ' . $e->getMessage()
    ]);
}

// --- FONCTION ---

/**
 * @param PDO $db
 * @return array
 *
 * Récupère la liste des statuts depuis la table Status.
 * Chaque élément contient :
 *   - code : entier représentant le code de statut (ex: 5)
 *   - label : chaîne décrivant le statut (ex: "En navigation")
 */
function getStatuses(PDO $db): array {
    $query = "SELECT Status AS status, Description AS description FROM status ORDER BY Status ASC";
    $stmt = $db->query($query);
    return $stmt->fetchAll(PDO::FETCH_ASSOC);
}
