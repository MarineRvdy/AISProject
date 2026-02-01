############################################################
# Etude des corrélations entre variables                   #
# Eliott Cosquer                                           #
# 03/06/25                                                 #
############################################################



# ─────────────────────── Chargement des bibliothèques ───────────────────────────── #

packages <- c("tidyr", "dplyr", "readr", "leaflet", "mapview", "webshot")


# Installer uniquement les packages manquants
install_if_missing <- function(pkg) {
  if (!requireNamespace(pkg, quietly = TRUE)) {
    install.packages(pkg)
  }
}

invisible(lapply(packages, install_if_missing))

library(ggplot2)  # Pour l’analyse exploratoire de données (EDA)
library(dplyr)        # Pour la manipulation de données (pipeline %>%, filter, mutate, etc.)
library(readr)        # Pour l'importation/exportation rapide et efficace de fichiers (CSV, TSV, etc.)
library(leaflet)
library(mapview)
library(webshot)

# Initialiser PhantomJS pour les exports PNG
if (!webshot::is_phantomjs_installed()) {
  webshot::install_phantomjs()
}

# ───────────────────── Création des dossiers ───────────────────────── #

if (!dir.exists("visualisations")) {
  dir.create("visualisations")
}


# ────────────── Importation des données ─────────────────────────────

vessel_clean <- read.csv("vessel_clean.csv")


#----------- Heading ----------------------------------------------------------
# Filtre sur le cap 511 car ça signifie qu'il n'y a pas de donnée d'après l'AIS
# filtre pour avoir uniquement 8 signaux par jour et par bateau
# filtre sur les bateaux immobiles (1 ou 0 noeud)
# Étape 1 : Préparation et filtrage (bateaux en mouvement, heading connu)
vessel_heading_8pd <- vessel_clean %>%
  filter(!is.na(MMSI), !is.na(Heading), !is.na(VesselType), !is.na(BaseDateTime), !is.na(SOG)) %>%
  filter(SOG > 1, Heading != 511) %>%  # bateau en mouvement et heading valide
  mutate(BaseDateTime = as.POSIXct(BaseDateTime, format = "%Y-%m-%d %H:%M:%S", tz = "UTC"),
         day = as.Date(BaseDateTime)) %>%
  arrange(MMSI, day, BaseDateTime) %>%
  group_by(MMSI, day) %>%
  filter(n() >= 8) %>%
  slice(as.integer(round(seq(1, n(), length.out = 8)))) %>%
  ungroup()

# Étape 2 : Regroupement des heading en 4 classes
vessel_heading_8pd <- vessel_heading_8pd %>%
  mutate(HeadingClass = case_when(
    Heading >= 0   & Heading < 90   ~ "0–89",
    Heading >= 90  & Heading < 180  ~ "90–179",
    Heading >= 180 & Heading < 270  ~ "180–269",
    Heading >= 270 & Heading <= 360 ~ "270–360",
    TRUE ~ NA_character_
  )) %>%
  filter(!is.na(HeadingClass))

# Étape 3 : Tableau croisé
tab_heading_8pd <- table(vessel_heading_8pd$VesselType, vessel_heading_8pd$HeadingClass)

# Étape 4 : Test du chi²
test_heading_8pd <- chisq.test(tab_heading_8pd)
print(test_heading_8pd)

# Étape 5 : visualisations
mosaicplot(tab_heading_8pd,
           main = "Mosaic plot : VesselType vs Heading class (SOG > 1, heading ≠ 511)",
           shade = TRUE, las = 2)

# ---------------------------------- Status -------------------------------------
vessel_8pd <- vessel_clean %>%
  filter(!is.na(MMSI), !is.na(Status), !is.na(VesselType), !is.na(BaseDateTime)) %>%
  mutate(BaseDateTime = as.POSIXct(BaseDateTime, format = "%Y-%m-%d %H:%M:%S", tz = "UTC"),
         day = as.Date(BaseDateTime)) %>%
  arrange(MMSI, day, BaseDateTime) %>%
  group_by(MMSI, day) %>%
  filter(n() >= 8) %>%  # ne garde que les jours avec au moins 8 signaux
  slice(as.integer(round(seq(1, n(), length.out = 8)))) %>%  # 8 signaux espacés dans la journée
  ungroup()

vessel_8pd_clean <- vessel_8pd %>%
  filter(Status != "\\N") %>%
  mutate(Status = as.numeric(as.character(Status)))

# Étape 3 : Tableau croisé
tab_8pd <- table(vessel_8pd_clean$VesselType, vessel_8pd_clean$Status)

# Étape 4 : Test du Chi²
test_8pd <- chisq.test(tab_8pd)
print(test_8pd)

# Étape 5 : Mosaic plot
mosaicplot(tab_8pd,
           main = "Mosaic plot : VesselType vs Status (8 signaux par jour)",
           shade = TRUE, las = 2)

# ────────────────── Fin du script fct4 ─────────────────────────────────────────