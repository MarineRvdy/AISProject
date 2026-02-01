import mysql.connector
import zipfile
import io
import csv
import re

# Parse les constantes PHP depuis constantes.php
def lire_constantes_php(fichier):
    variables = {}
    with open(fichier, 'r') as f:
        contenu = f.read()
        matches = re.findall(r'\$([A-Z_]+)\s*=\s*\'([^\']*)\'', contenu)
        for cle, valeur in matches:
            variables[cle] = valeur
    return variables

# Récupérer les constantes
constantes = lire_constantes_php('constantes.php')

# Connexion MySQL avec les constantes
conn = mysql.connector.connect(
    host=constantes['DB_SERVER'],
    user=constantes['DB_USER'],
    password=constantes['DB_PASSWORD'],
    database=constantes['DB_NAME']
)
cursor = conn.cursor()

# Configuration des tables
tables = {
    'navires': {
        'zip': '../csv/navires.csv.zip',
        'columns': ['MMSI', 'VesselName', 'VesselType', 'Length', 'Width'],
        'primary': ['MMSI']
    },
    'status' : {
        'zip': '../csv/status.csv.zip',
        'columns': ['Status',  'Description'],
        'primary': ['Status']
    },
    'positions': {
        'zip': '../csv/positions.csv.zip',
        'columns': ['MMSI', 'BaseDateTime', 'LAT', 'LON', 'SOG', 'COG', 'Heading', 'Status', 'Draft'],
        'primary': ['id']
    }
    
}

# Créer une table si elle n'existe pas
def create_table(name, columns, primary_keys):
    if name == 'positions':
        sql = """
        CREATE TABLE IF NOT EXISTS positions (
            id INT AUTO_INCREMENT PRIMARY KEY,
            MMSI INT(10),
            BaseDateTime DATETIME,
            LAT DECIMAL(9,6),
            LON DECIMAL(9,6),
            SOG DECIMAL(3,1),
            COG DECIMAL(4,1),
            Heading DECIMAL(4,1),
            Status TINYINT,
            Draft DECIMAL(3,1),
            FOREIGN KEY (MMSI) REFERENCES navires(MMSI)
            ON DELETE SET NULL
            ON UPDATE CASCADE,
            FOREIGN KEY (Status) REFERENCES status(Status)
            ON DELETE SET NULL
            ON UPDATE CASCADE
        )
        """
        cursor.execute(sql)
        return
    col_defs = ', '.join(
        f"{col} {'DATETIME' if col == 'BaseDateTime' else 'DECIMAL(9,6)' if col in ['LAT', 'LON'] else 'DECIMAL(3,1)' if col in ['SOG', 'Draft'] else 'DECIMAL(4,1)' if col in ['COG', 'Heading'] else 'DECIMAL(5,2)' if col in ['Length', 'Width'] else 'INT(10)' if col in ['MMSI'] else 'SMALLINT' if col in ['VesselType'] else 'TINYINT' if col in ['Status'] else 'VARCHAR(50)'}"
        for col in columns
    )
    pk = ', '.join(primary_keys)
    sql = f"CREATE TABLE IF NOT EXISTS {name} ({col_defs}, PRIMARY KEY ({pk}))"
    cursor.execute(sql)

# Vérifier si une table est vide
def is_table_empty(name):
    cursor.execute(f"SELECT COUNT(*) FROM {name}")
    return cursor.fetchone()[0] == 0

# Importation depuis zip → MySQL
def import_from_zip(table, path, columns):
    print(f"📦 Importation de {path} → {table}...")
    with zipfile.ZipFile(path) as z:
        with z.open(z.namelist()[0]) as csv_file:
            decoded = io.TextIOWrapper(csv_file, encoding='utf-8')
            reader = csv.reader(decoded)
            header = next(reader)  # Ignorer en-tête
            placeholders = ', '.join(['%s'] * len(columns))
            col_names = ', '.join(columns)
            sql = f"INSERT IGNORE INTO {table} ({col_names}) VALUES ({placeholders})"

            count = 0
            for row in reader:
                if len(row) == len(columns):
                    cursor.execute(sql, row)
                    count += 1
                    if count % 10000 == 0:
                        print(f"  {count} lignes insérées...")
            conn.commit()
    print(f"✅ {table} terminé : {count} lignes insérées.")

# Lancer l'importation
for name, config in tables.items():
    create_table(name, config['columns'], config['primary'])
    if is_table_empty(name):
        import_from_zip(name, config['zip'], config['columns'])
    else:
        print(f"⏩ {name} non vide, importation ignorée.")

# Nettoyage
cursor.close()
conn.close()