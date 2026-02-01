#############################################################################
# Prédiction de la variable VesselType en fonction des variables pertinentes#
# Guillaume LE NESTOUR                                                      #
# 03/06/25                                                                  #
#############################################################################

# ─────────────────────── Chargement des bibliothèques ───────────────────────────── #

packages <- c("nnet", "dyplir", "readr", "ggplot2")

# Installer uniquement les packages manquants
install_if_missing <- function(pkg) {
  if (!requireNamespace(pkg, quietly = TRUE)) {
    install.packages(pkg)
  }
}

invisible(lapply(packages, install_if_missing))

library(nnet)     # Pour les réseaux de neurones simples (modèles de type multinom, nnet)
library(ggplot2)  # Pour l’analyse exploratoire de données (EDA)
library(dplyr)        # Pour la manipulation de données (pipeline %>%, filter, mutate, etc.)
library(readr)        # Pour l'importation/exportation rapide et efficace de fichiers (CSV, TSV, etc.)


# ─────────────────────  Création des dossiers ───────────────────────── #

if (!dir.exists("visualisations")) {
  dir.create("visualisations")
}


# ────────────── Importation des données ─────────────────────────────

vessel_clean <- read.csv("vessel_clean.csv")

# ─────────────────────── Prédiction de la variable VesselType ───────────────────── #

# Nouveau tableau avec 10 échantillon pour chaque bateau 
vessel_sampled <- vessel_clean %>%
  filter(!is.na(BaseDateTime)) %>%
  group_by(MMSI) %>%
  filter(n() >= 10) %>%
  arrange(BaseDateTime) %>%
  mutate(row_id = row_number()) %>%
  filter(row_id %in% round(seq(1, n(), length.out = 10))) %>%
  ungroup()


# Régression logistique sur VesselType en fonction de Length/Width/Draft/Cargo/Heading/Status
model_vessel <- multinom(VesselType ~ Length + Width + Draft + Cargo + Heading + Status , data = vessel_sampled)
#summary(model_vessel)
pred_vesseltype <- predict(model_vessel, newdata = vessel_sampled)

table(Predicted = pred_vesseltype, Actual = vessel_sampled$VesselType)

# Calcul du taux d'erreur
mean(pred_vesseltype != vessel_sampled$VesselType)



# Matrice de confusion de la Prédiction de VesselType
conf_mat <- table(Predicted = pred_vesseltype, Actual = vessel_sampled$VesselType)
conf_df <- as.data.frame(conf_mat)
colnames(conf_df) <- c("Predicted", "Actual", "Freq")
conf_mat_plot = ggplot(conf_df, aes(x = Actual, y = Predicted, fill = Freq)) +
  geom_tile(color = "white") +
  scale_fill_gradient(low = "white", high = "red") +
  geom_text(aes(label = Freq), color = "black", size = 3) +
  labs(title = "Matrice de confusion - Prédiction de VesselType", x = "Réel", y = "Prédit") +
  theme_minimal()

ggsave("visualisations/Prediction_VesselType.png", plot = conf_mat_plot, width = 8, height = 8, dpi = 300)


# ─────────────────────── Prédiction de la vitesse (SOG) ───────────────────────── #

# nouveau tableau avec la vitesse moyenne (excluant les valeurs <1) de chacun des bateaux
vessel_SOG_unique <- vessel_clean %>%
  filter(!is.na(SOG)) %>%
  group_by(MMSI) %>%
  reframe(
    SOG = mean(SOG[SOG > 1], na.rm = TRUE),
    VesselType = mean(VesselType, na.rm = TRUE),
    Length  = mean(Length, na.rm = TRUE),
    Width  = mean(Width, na.rm = TRUE),
    Draft  = mean(Draft, na.rm = TRUE),
    Cargo  = mean(Cargo, na.rm = TRUE)
  )

# On supprime la ligne si le bateau était à l'arret
vessel_SOG_unique <- vessel_SOG_unique %>%
  filter(!is.na(SOG))


# Modèle de régression linéaire 
model_sog <- lm(SOG ~ Length + Width + Draft + VesselType + Cargo, data = vessel_SOG_unique)

# Prédiction
pred_sog <- predict(model_sog, newdata = vessel_SOG_unique)

# Calcul des erreurs
mae <- mean(abs(pred_sog - vessel_SOG_unique$SOG))
rmse <- sqrt(mean((pred_sog - vessel_SOG_unique$SOG)^2))

cat("Erreur moyenne absolue (MAE) :", round(mae, 2), "\n")
cat("Erreur quadratique moyenne (RMSE) :", round(rmse, 2), "\n")

# Graphique : valeurs réelles vs. prédites
g <- ggplot(data = vessel_SOG_unique, aes(x = SOG, y = pred_sog)) +
  geom_point(alpha = 0.4) +
  geom_abline(slope = 1, intercept = 0, color = "blue", linetype = "dashed") +
  labs(
    title = "Prédiction de la vitesse (SOG)",
    x = "SOG réelle",
    y = "SOG prédite"
  ) +
  theme_minimal()

ggsave("visualisations/Prediction_SOG.png", plot = g, width = 8, height = 8, dpi = 300)

# ────────────────── Fin du script fct5 ─────────────────────────────────────────