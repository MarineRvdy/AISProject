<?php
// Connexion à la base de données (modèle générique, à adapter)
function dbConnect() {
    include("constantes.php");
    try {
        $db = new PDO('mysql:host=' . $DB_SERVER . ';dbname=' . $DB_NAME . ';charset=utf8', $DB_USER, $DB_PASSWORD);
        $db->setAttribute(PDO::ATTR_ERRMODE, PDO::ERRMODE_EXCEPTION);
        return $db;
    } catch (PDOException $exception) {
        error_log('Connection error: ' . $exception->getMessage());
        return null;
    }
}
// Exemple de fonction générique pour requête SELECT (table et champs en variables)
function dbSelect($sql, $params = []) {
    $db = dbConnect();
    if (!$db) return [];
    $stmt = $db->prepare($sql);
    $stmt->execute($params);
    return $stmt->fetchAll(PDO::FETCH_ASSOC);
}
// Exemple de fonction générique pour requête INSERT
function dbInsert($table, $data, $where = '', $params = []) {
    $db = dbConnect();
    if (!$db) return false;
    $fields = implode(',', array_keys($data));
    $placeholders = ':' . implode(',:', array_keys($data));
    $sql = "INSERT IGNORE INTO $table ($fields) VALUES ($placeholders)";
    if ($where) $sql .= " WHERE $where";
    $stmt = $db->prepare($sql);
    return $stmt->execute($data);
} 

function dbUpdate($table, $data, $where = '', $params = []) {
    $db = dbConnect();
    if (!$db) return false;
    $setClause = implode(', ', array_map(function($key) {
        return "$key = :$key";
    }, array_keys($data)));
    $sql = "UPDATE $table SET $setClause";
    if ($where) {
        $sql .= " WHERE $where";
    }
    $allParams = array_merge($data, $params);
    $stmt = $db->prepare($sql);
    return $stmt->execute($allParams);
}