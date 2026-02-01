############################################################
# Description et exploration des données                   #
# Guillaume LE NESTOUR et Marine REVERDY                   #                           #
# 03/06/25                                                 #
############################################################

# ─────────────────────── Chargement des bibliothèques ───────────────────────────── #

packages <- c("funModeling", "dplyr", "tidyr", "corrplot", "readr", "geosphere")

# Installer uniquement les packages manquants
install_if_missing <- function(pkg) {
  if (!requireNamespace(pkg, quietly = TRUE)) {
    install.packages(pkg)
  }
}

invisible(lapply(packages, install_if_missing))

library(funModeling)  # Pour l’analyse exploratoire de données (EDA)
library(dplyr)        # Pour la manipulation de données (pipeline %>%, filter, mutate, etc.)
library(tidyr)        # Pour gérer les valeurs manquantes et manipuler les colonnes
library(corrplot)     # Pour visualiser les matrices de corrélation entre variables numériques
library(readr)        # Pour l'importation/exportation rapide et efficace de fichiers (CSV, TSV, etc.)
library(geosphere)    # Pour les calculs de distance géographique (ex : distance entre deux points GPS)

# ───────────────────── Création des dossiers ───────────────────────── #

if (!dir.exists("visualisations")) {
  dir.create("visualisations")
}

# ─────────────────────── Importation et nettoyage de base ───────────────────────── #

vessel <- read.csv("vessel-total-clean.csv")  # Import du fichier CSV dans un data frame nommé vessel

vessel[vessel == "\\N"] <- NA  # Remplacement des valeurs "\N" par NA pour identifier les données manquantes

# Suppression des doublons (en ignorant la première colonne, souvent un identifiant unique)
vessel <- vessel[!duplicated(vessel[,-1]), ]

# ──────────────── Conversion des variables et traitement des données ────────────── #

# Conversion de Length, Width et Draft en variables numériques
vessel <- vessel %>%
  mutate(
    Status = as.numeric(Status),
    Length = as.numeric(Length),
    Width = as.numeric(Width),
    Draft = as.numeric(Draft),
    Cargo = as.numeric(Cargo)
  )

# Conversion de BaseDateTime en format date-heure POSIX
vessel$BaseDateTime <- as.POSIXct(vessel$BaseDateTime, format = "%Y-%m-%d %H:%M:%S")

# Remplacement des valeurs manquantes de Cargo par le type de bateau (VesselType)
vessel <- vessel %>%
  mutate(Cargo = coalesce(Cargo, VesselType))

# Remplacement des Status manquants par "15" (statut par défaut)
vessel <- vessel %>%
  mutate(Status = coalesce(Status, 15))


# ─────────────────── Estimation des dimensions manquantes ───────────────────────── #

# Calcul des moyennes (hors NA)
mean_length <- mean(vessel$Length, na.rm = TRUE)
mean_width  <- mean(vessel$Width, na.rm = TRUE)

# Estimation des longueurs manquantes à partir de la largeur
vessel <- vessel %>%
  mutate(Length = coalesce(Length, (mean_length / mean_width) * Width))

# Estimation des largeurs manquantes à partir de la longueur
vessel <- vessel %>%
  mutate(Width = coalesce(Width, (mean_width / mean_length) * Length))

# ─────────────────────── Prédiction des valeurs de Draft ────────────────────────── #

# Ajustement d’un modèle linéaire : Draft en fonction de Length et Width
model <- lm(Draft ~ Length + Width, data = vessel)


# Prédiction des valeurs manquantes de Draft à partir du modèle
pred_draft <- predict(model, newdata = vessel)


# Remplacement des Draft manquants par les prédictions
vessel <- vessel %>%
  mutate(
    Draft = if_else(
      is.na(Draft) & !is.na(pred_draft),
      pred_draft,
      Draft
    )
  )


# ─────────────── Mise à la moyenne des valeurs toujours manquantes ──────────────── #

# Calcul de la moyenne de draft (hors NA)
mean_draft  <- mean(vessel$Draft, na.rm = TRUE)


vessel <- vessel %>% # Remplace les valeurs manquantes (NA) de Width par la moyenne
  mutate(Width = coalesce(Width, mean_width))
vessel <- vessel %>% # Remplace les valeurs manquantes (NA) de Length par la moyenne
  mutate(Length = coalesce(Length, mean_width))
vessel <- vessel %>% # Remplace les valeurs manquantes (NA) de Draft par la moyenne
  mutate(Draft = coalesce(Draft, mean_width))


# ─────────────────────── Calculer les vitesses incoherentes  ────────────────────── #

vitesse_max <- 40       # Vitesse max raisonnable en nœuds


vessel <- vessel %>%
  arrange(MMSI, BaseDateTime)

# Calcul de la vitesse réelle entre deux positions successives
vessel <- vessel %>%
  group_by(MMSI) %>%
  mutate(
    lat_prev = lag(LAT),
    lon_prev = lag(LON),
    time_prev = lag(BaseDateTime),
    dist_m = distHaversine(cbind(lon_prev, lat_prev), cbind(LON, LAT)),
    time_diff = as.numeric(difftime(BaseDateTime, time_prev, units = "secs")),
    speed_computed = (dist_m / time_diff) * 1.94384,  # conversion m/s -> noeuds
    SOG = ifelse(SOG > vitesse_max & !is.na(speed_computed), speed_computed, SOG)
  ) %>%
  ungroup()

vessel <- vessel %>%
  group_by(MMSI) %>%
  mutate(
    SOG_modified = any(SOG != lag(SOG), na.rm = TRUE),           # Indique s'il y a eu un changement de SOG dans le groupe
    SOG = ifelse(row_number() == 1 & SOG_modified, lead(SOG), SOG)  # Remplace la 1ère ligne si changement détecté
  ) %>%
  select(-SOG_modified) %>%
  ungroup()

vessel <- vessel %>%
  select(-lat_prev, -lon_prev, -time_prev, -dist_m, -time_diff, -speed_computed)


# ─────────────────────── Arrondi des dimensions à 2 décimales ───────────────────── #

vessel <- vessel %>%
  mutate(Width  = round(Width, 2),
         Length = round(Length, 2),
         Draft  = round(Draft, 2),
         SOG  = round(SOG, 2))

# ─────────────────────── Suppression des valeurs aberrantes ─────────────────────── #

# Définition des seuils de valeurs valides (Gulf of Mexico)
lat_min <- 20           # Latitude minimale
lat_max <- 40           # Latitude maximale
lon_min <- -100         # Longitude minimale
lon_max <- -75          # Longitude maximale


# Filtrage : suppression des lignes hors zone ou à vitesse incohérente
vessel <- vessel %>%
  filter(
    LAT >= lat_min & LAT <= lat_max,
    LON >= lon_min & LON <= lon_max,
  )


# ─────────────────────── Exportation du csv nettoyé ─────────────────────── #

write_csv(vessel, "vessel_clean.csv")


# ─────────────────────── Analyse descriptive univariée ──────────────────────────── #

# Résumé général de toutes les variables
summary(vessel)


# Détails par variable + comptage des valeurs uniques
summary(vessel$id)
cat("Nombre d’id différents :", length(unique(vessel$id)), "\n")

summary(vessel$MMSI)
cat("Nombre de bateaux différents (MMSI) :", length(unique(vessel$MMSI)), "\n")

summary(vessel$BaseDateTime)
cat("Nombre de dates différentes :", length(unique(vessel$BaseDateTime)), "\n")

summary(vessel$LAT)
cat("Nombre de LAT différentes :", length(unique(vessel$LAT)), "\n")

summary(vessel$LON)
cat("Nombre de LON différentes :", length(unique(vessel$LON)), "\n")

summary(vessel$SOG)
cat("Nombre de SOG différentes :", length(unique(vessel$SOG)), "\n")

summary(vessel$COG)
cat("Nombre de COG différentes :", length(unique(vessel$COG)), "\n")

summary(vessel$Heading)
cat("Nombre de Heading différents :", length(unique(vessel$Heading)), "\n")

summary(vessel$VesselName)
cat("Nombre de noms de bateau différents :", length(unique(vessel$VesselName)), "\n")

summary(vessel$IMO)
cat("Nombre d’IMO différents :", length(unique(vessel$IMO)), "\n")

summary(vessel$CallSign)
cat("Nombre de CallSign différents :", length(unique(vessel$CallSign)), "\n")

summary(vessel$VesselType)
cat("Nombre de types de bateaux différents :", length(unique(vessel$VesselType)), "\n")

summary(vessel$Status)
cat("Nombre de Status différents :", length(unique(vessel$Status)), "\n")

summary(vessel$Length)
summary(vessel$Width)
summary(vessel$Draft)

summary(vessel$Cargo)
cat("Nombre de types de cargaison différents :", length(unique(vessel$Cargo)), "\n")

summary(vessel$TransceiverClass)
cat("Nombre de classes de transceiver différentes :", length(unique(vessel$TransceiverClass)), "\n")


# ─────────────────────── Analyse descriptive bivariée ───────────────────────────── #

# Nouveau tableau avec 10 échantillon pour chaque bateau 
vessel_sample <- vessel %>%
  filter(!is.na(BaseDateTime)) %>%
  group_by(MMSI) %>%
  filter(n() >= 10) %>%
  arrange(BaseDateTime) %>%
  mutate(row_id = row_number()) %>%
  filter(row_id %in% round(seq(1, n(), length.out = 10))) %>%
  ungroup()


# Heatmap de corrélations pour toutes les variables numériques
num_vars <- vessel_sample %>% select(where(is.numeric)) 
cor_matrix <- cor(num_vars, use = "complete.obs")
png("visualisations/correlation_matrix.png", width = 800, height = 600)
corrplot(cor_matrix, method = "color", type = "upper", tl.col = "black")
dev.off()



# Longueur des bateaux par type
png("visualisations/boxplot_length_by_type.png", width = 800, height = 600)
boxplot(Length ~ VesselType, data = vessel_sample, main = "Longueur des bateaux par type", xlab = "Type de bateau", ylab = "Longueur")
dev.off()

# Vitesse selon le type
png("visualisations/boxplot_sog_by_type.png", width = 800, height = 600)
boxplot(SOG ~ VesselType, data = vessel_sample, main = "Vitesse selon le type", xlab = "Type", ylab = "Vitesse (SOG)")
dev.off()

# Draft en fonction de la longueur
png("visualisations/draft_vs_length.png", width = 800, height = 600)
plot(vessel_sample$Length, vessel_sample$Draft, main = "Draft en fonction de la longueur", xlab = "Longueur", ylab = "Draft")
dev.off()

# Tableau croisé entre le VesselType et la TransceiverClass, pour explorer leur répartition conjointe 
table(vessel_sample$VesselType, vessel_sample$TransceiverClass)