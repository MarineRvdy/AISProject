############################################################
# Trajectoires de navires et routes principales            #
# Eliott Cosquer                                           #
# 03/06/25                                                 #
############################################################

# ──────────────── 1. Préparation ──────────────────── #

packages <- c("data.table", "dplyr", "sf", "leaflet","ggplot2", "ggspatial", "viridis", "leaflet.extras", "lwgeom", "mapview", "webshot", "webshot2", "htmlwidgets" )

# Installer uniquement les packages manquants
install_if_missing <- function(pkg) {
  if (!requireNamespace(pkg, quietly = TRUE)) {
    install.packages(pkg)
  }
}

invisible(lapply(packages, install_if_missing))

library(data.table)  # chargement rapide des CSV volumineux
library(dplyr)       # Manipulation de données avec une syntaxe fluide
library(sf)          # objets géospatiaux
library(leaflet)     # carte interactive
library(ggplot2)     # carte statique + densité
library(ggspatial)   # échelle & north arrow
library(viridis)     # palette de couleurs
library(leaflet.extras) # carte de chaleur
library(lwgeom) # fonctions géospatiales avancées 
library(mapview) #export de la carte en png
library(webshot) #export de la carte en png
library(webshot2)
library(htmlwidgets)

# Installation de PhantomJS si non présent
if (!webshot::is_phantomjs_installed()) {
  webshot::install_phantomjs()
}

# ───────────────────── 2. Création des dossiers ───────────────────────── #

if (!dir.exists("visualisations")) {
  dir.create("visualisations")
}


# ────────────── 3. Importation des données ─────────────────────────────

vessel_map <- read.csv("vessel_clean.csv")

# ────────────── 4. Trajectoires interactives (Leaflet) ─────────────────
# 3.1 Création d’un objet sf “points”
pts_sf <- st_as_sf(vessel_map, coords = c("LON", "LAT"), crs = 4326, remove = FALSE)
#crs = 4326 : définit le système de coordonnées (WGS 84), standard GPS

# 3.2 Création de lignes par navire
routes_sf <- pts_sf %>%
  arrange(VesselName, BaseDateTime) %>%          # ordre chronologique
  group_by(VesselName) %>%
  summarise(do_union = FALSE) %>%                # évite fusion des lignes
  st_cast("LINESTRING")

# 3.3 Carte interactive toutes trajectoires
map_all <- leaflet() %>%
  addProviderTiles("CartoDB.Positron") %>%
  addPolylines(data = routes_sf,
               color = "#444444", weight = 1,
               popup = ~VesselName,
               group = "Trajectoires")

# Affichage dans RStudio
print(map_all)

# export en png
mapshot(map_all, file = "visualisations/map_tout_trajet.png")

# ────────────── 5. Trajectoire d’un navire par son nom ─────────────────
# Fonction helper
trace_vessel <- function(vessel_name, vessel_name2, vessel_name3) {
  # Extraire les lignes pour chaque navire
  v_line1 <- routes_sf %>% filter(VesselName == vessel_name)
  v_line2 <- routes_sf %>% filter(VesselName == vessel_name2)
  v_line3 <- routes_sf %>% filter(VesselName == vessel_name3)
  
  if (nrow(v_line1) == 0 | nrow(v_line2) == 0 | nrow(v_line3) == 0) {
    message("Un ou plusieurs navires sont introuvables")
    return(invisible(NULL))
  }
  
  # Construction de la carte
  leaflet() %>%
    addProviderTiles("CartoDB.Positron") %>%
    addPolylines(data = v_line1, color = "red", weight = 3, popup = vessel_name, group = "Trajectoire") %>%
    addPolylines(data = v_line2, color = "blue", weight = 3, popup = vessel_name2, group = "Trajectoire") %>%
    addPolylines(data = v_line3, color = "green", weight = 3, popup = vessel_name3, group = "Trajectoire")
  
}

# afficher la trajectoire du navire « STOLT LOTUS »
map <- trace_vessel("STOLT LOTUS", "MAERSK TENNESSEE", "STOLT ISLAND")
mapshot(map, file = "visualisations/map_solo.png")
# ────────────── 6. Routes commerciales communes ─────────────────

# 1. Densifier les lignes : un point tous les ~5 km
routes_points <- routes_sf %>%
  st_segmentize(dfMaxLength = units::set_units(5000, "m")) %>%
  st_cast("POINT")


# 2. Créer et stocker la carte dans un objet
heatmap_routes <- leaflet() %>%
  addProviderTiles("CartoDB.Positron") %>%
  addHeatmap(data = routes_points, 
             radius = 12, 
             blur = 20, 
             max = 0.05,
             intensity = rep(1, nrow(routes_points)))

print(heatmap_routes)


# Sauvegarder la carte Leaflet en HTML
saveWidget(heatmap_routes, "heatmap_routes.html", selfcontained = TRUE)

# Capture du fichier HTML en image PNG via webshot2
webshot2::webshot("heatmap_routes.html", "visualisations/heatmap_routes.png")

# ────────────────── Fin du script fct3 ─────────────────────────────────────────


