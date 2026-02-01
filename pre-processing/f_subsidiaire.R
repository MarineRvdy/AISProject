############################################################
# Etude des corrélations entre variables                   #
# Eliott Cosquer                                           #
# 05/06/25                                                 #
############################################################



# ─────────────────────── Chargement des bibliothèques ───────────────────────────── #

packages <- c("tidyr", "dyplr", "readr", "htmlwidgets", "webshot2")

# Installer uniquement les packages manquants
install_if_missing <- function(pkg) {
  if (!requireNamespace(pkg, quietly = TRUE)) {
    install.packages(pkg)
  }
}

invisible(lapply(packages, install_if_missing))

library(readr)
library(dplyr)
library(tidyr)
library(htmlwidgets)
library(webshot2)

# ─────────────────────  Création des dossiers ───────────────────────── #

if (!dir.exists("visualisations")) {
  dir.create("visualisations")
}


# ────────────── Importation des données et séparer suivant draft ─────────────────────

vessel_clean <- read.csv("vessel_clean.csv")

vessel_clean <- vessel_clean %>% distinct(MMSI, LAT, LON, BaseDateTime, .keep_all = TRUE) # Retire les doublons

# Définir les seuils pour faible et fort tirant d'eau
low_threshold <- quantile(vessel_clean$Draft, 1/3)
high_threshold <- quantile(vessel_clean$Draft, 2/3)

# Séparer en deux jeux de données
df_low <- vessel_clean %>% filter(Draft <= low_threshold)
df_high <- vessel_clean %>% filter(Draft >= high_threshold)


# ────────────── Carte : Tirant d’eau faible ───────────────────────

heatmap_low <- leaflet(data = df_low) %>%
  addProviderTiles("CartoDB.Positron") %>%
  addHeatmap(lng = ~LON, lat = ~LAT,
             blur = 20, max = 0.05, radius = 8) %>%


#afficher dans R
print(heatmap_low)

#exporter en html
saveWidget(heatmap_low, "heatmap_low.html", selfcontained = TRUE)
webshot2::webshot("heatmap_low.html", "visualisations/heatmap_low.png")

# ────────────── Carte : Tirant d’eau élevé ───────────────────────

heatmap_high <- leaflet(data = df_high) %>%
  addProviderTiles("CartoDB.Positron") %>%
  addHeatmap(lng = ~LON, lat = ~LAT,
             blur = 16, max = 0.05, radius = 8) %>%

#afficher dans R
print(heatmap_high)

#exporter en html
saveWidget(heatmap_high, "heatmap_high.html", selfcontained = TRUE)
webshot2::webshot("heatmap_high.html", "visualisations/heatmap_high.png")

# ────────────────── Fin du script fct_subsidiaire ─────────────────────────────────────────