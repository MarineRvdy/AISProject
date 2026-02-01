############################################################
# visualisations des données sur des graphiques             #
# Marine REVERDY                                           #
# 03/06/25                                                 #
############################################################


# ──────────── 1. Chargement des bibliothèques ───────────── #

packages <- c("leaflet", "dplyr", "mapview", "webshot")

# Installer uniquement les packages manquants
install_if_missing <- function(pkg) {
  if (!requireNamespace(pkg, quietly = TRUE)) {
    install.packages(pkg)
  }
}

invisible(lapply(packages, install_if_missing))

library(leaflet)  # Pour l’analyse exploratoire de données (EDA)
library(dplyr)        # Pour la manipulation de données (pipeline %>%, filter, mutate, etc.)
library(mapview) # Pour export de leaflet au format png
library(webshot)

# Installation de PhantomJS si non présent
if (!webshot::is_phantomjs_installed()) {
  webshot::install_phantomjs()
}

# ─────────── 2. Création du dossier de visualisations ─────── #
if (!dir.exists("visualisations")) {
  dir.create("visualisations")
}

# ───────────── 3. Chargement des données ───────────── #
vessels <- read.csv("vessel_clean.csv")

# ────── 4. Répartition des navires par catégorie ────── #
# On ne garde qu'une ligne par navire unique
unique_vessels <- vessels[!duplicated(vessels$MMSI), ]

# Catégorisation des navires selon le VesselType
unique_vessels$Category <- sapply(unique_vessels$VesselType, function(type) {
  if (type >= 70 & type <= 79) "Cargos"
  else if (type >= 80 & type <= 89) "Tankers"
  else if (type >= 60 & type <= 69) "Passagers"
  else "Autres"
})

# Comptage des navires par catégorie
counts <- sort(table(unique_vessels$Category), decreasing = TRUE)

# Définition des colors associées à chaque catégorie
colors <- c("Cargos" = "orange", "Tankers" = "red", "Passagers" = "blue", "Autres" = "gray")

# Affichage d’un diagramme en barres
png("visualisations/barplot_categories.png", width = 800, height = 600)
bar_types <- barplot(counts,
                  main = "Répartition des navires par catégorie",
                  xlab = "Catégorie de navire",
                  ylab = "Nombre de navires",
                  col = colors[names(counts)],
                  las = 1,
                  ylim = c(0, max(counts) * 1.1))

# Ajout des valeurs au-dessus des barres
text(x = bar_types, y = counts, label = counts, pos = 3, cex = 0.8, col = "gray")
dev.off()

# ─────── 5. Histogramme des longueurs ─────── #
png("visualisations/histogramme_longueurs.png", width = 800, height = 600)
length_hist = hist(unique_vessels$Length,
                   main = "Histogramme de la longueur des navires",
                   xlab = "Longueur des navires (en mètres)",
                   ylab = "Nombre de navires",
                   col = "lightgreen",
                   breaks = 20)

text(x = length_hist$mids, y = length_hist$counts - 4,
     labels = length_hist$counts, pos = 3, cex = 0.8, col = "darkgreen")
dev.off()

# ─────── 6. Histogramme des largeurs ─────── #
png("visualisations/histogramme_largeurs.png", width = 800, height = 600)
width_hist <- hist(unique_vessels$Width,
                    main = "Histogramme de la largeur des navires",
                    xlab = "Longueur des navires (en mètres)",
                    ylab = "Nombre de navires",
                    col = "lightgreen",
                    breaks = 20)

text(x = width_hist$mids, y = width_hist$counts - 4,
     labels = width_hist$counts, pos = 3, cex = 0.8, col = "darkgreen")
dev.off()

# ─────── 7. Histogramme des vitesses ─────── #
png("visualisations/histogramme_vitesses.png", width = 800, height = 600)
hist(vessels$SOG,
     main = "Histogramme de la vitesse des navires",
     xlab = "Vitesse (en noeuds)",
     ylab = "Nombres de navires",
     col = "lightblue",
     breaks = 20)
dev.off()

# ─────── 8. Transceiver par type de navire ─────── #
# Groupe de navires basé sur le type
unique_vessels$VesselGroup <- cut(unique_vessels$VesselType,
                              breaks = c(-Inf, 59, 69, 79, 89, Inf),
                              labels = c("Autres", "Passagers (60-69)", "Cargos (70-79)", "Tankers (80-89)", "Autres"))

# Tableau croisé entre groupe de navires et classe de transceiver
tranceiver_by_vessel_group <- table(unique_vessels$VesselGroup, unique_vessels$TransceiverClass)

# Diagramme en barres empilées
png("visualisations/barplot_transceivers.png", width = 1000, height = 600)
barplot(tranceiver_by_vessel_group,
        main = "Répartition des classes de transceiver par type de navire",
        xlab = "Classe de transceiver",
        ylab = "Nombre de navires",
        col = c("gray", "blue", "orange", "red", "darkgray"),
        legend = rownames(tranceiver_by_vessel_group))
dev.off()

# ─────── 9. Longueurs selon transceiver ─────── #
# Classes de longueur par tranches de 50 m
unique_vessels$LengthGroup <- cut(unique_vessels$Length,
                                      breaks = seq(0, max(unique_vessels$Length, na.rm = TRUE) + 50, by = 50),
                                      right = FALSE)

# Table croisée : classe de transpondeur en ligne, classe de longueur en colonne
length_tab <- table(unique_vessels$TransceiverClass, unique_vessels$LengthGroup)

# colors pour les longueurs
classes <- colnames(length_tab)
length_colors <- colorRampPalette(c("lightblue", "blue"))(length(classes))
names(length_colors) <- classes

# Barplot empilé des longueurs en fonction des transpondeurs
png("visualisations/barplot_longueurs_transceivers.png", width = 1000, height = 600)
barplot(t(length_tab),
        main = "Répartition des longueurs selon les transpondeurs",
        xlab = "Classe de transpondeur",
        ylab = "Nombre de navires",
        col = length_colors,
        legend = TRUE,
        args.legend = list(title = "Longueur (m)", x = "topright", cex = 0.8),
        las = 1)
dev.off()

# ─────── 10. Analyse des ports utilisés ─────── #
# Navires à l’arrêt (vitesse quasi nulle et status = 5)
stop_vessels <- vessels[vessels$SOG <= 0.5 & vessels$Status == 5, ]

# Arrondi des positions pour regrouper les ports proches
stop_vessels$LAT_round <- round(stop_vessels$LAT, 1)
stop_vessels$LON_round <- round(stop_vessels$LON, 1)

# Filtrage par type
cargos <- stop_vessels[stop_vessels$VesselType %in% 70:79, ]
tankers <- stop_vessels[stop_vessels$VesselType %in% 80:89, ]
passagers <- stop_vessels[stop_vessels$VesselType %in% 60:69, ]

# Fonction d’analyse des 10 ports les plus utilisés
ports_finder <- function(donnees) {
  donnees %>%
  # Regroupement des données par nom de navire et port (coordonnées arrondies) puis comptage des occurrences
    group_by(MMSI, LAT_round, LON_round) %>%
    summarise(nb_obs = n(), .groups = "drop") %>%
    # Regroupement par port uniquement (coordonnées)
    group_by(LAT_round, LON_round) %>%
    summarise(vessel_number = n_distinct(MMSI), .groups = "drop") %>%
    arrange(desc(vessel_number)) %>%
    head(10)
}

# Analyse par type
top_ports_cargos <- ports_finder(cargos)
top_ports_tankers <- ports_finder(tankers)
top_ports_passagers <- ports_finder(passagers)

# Ajout du type
top_ports_cargos$Type <- "Cargo"
top_ports_tankers$Type <- "Tanker"
top_ports_passagers$Type <- "Passager"

# Fusion des résultats
top_ports <- bind_rows(top_ports_cargos, top_ports_tankers, top_ports_passagers)

# Carte interactive
map_colors <- colorFactor(c("orange", "red", "blue"), domain = c("Cargo", "Tanker", "Passager"))

map_ports = leaflet(data = top_ports) %>%
  addTiles() %>% # Ajout du fond de carte
  # Ajout de marqueurs circulaires sur la carte pour chaque port
  addCircleMarkers(
    ~LON_round, ~LAT_round,
    radius = ~vessel_number * 2,
    color = ~map_colors(Type),
    popup = ~paste("Type:", Type, "<br>Latitude:", LAT_round,"<br>Longitude:", LON_round,"<br>Nombre de navires:", vessel_number)
  ) %>%
  # Centrage de la carte autour de la moyenne des positions GPS des 10 ports
  setView(lng = mean(top_ports$LON_round), lat = mean(top_ports$LAT_round), zoom = 5)


# Exporter la carte au format PNG
mapview::mapshot(map_ports, file = "visualisations/top_ports_map.png")
# ─────────────────────────── Fin du script fct2 ──────────────────────────────────── #
