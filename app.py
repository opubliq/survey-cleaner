# app.py
import streamlit as st
import pandas as pd
import os
from io import StringIO

st.title("Bot de Nettoyage de Sondages")

# Sidebar pour instructions d'utilisation
with st.sidebar:
    st.header("Instructions")
    st.info("""
    1. Téléversez votre fichier de sondage (CSV/SAV)
    2. Ajoutez le codebook (optionnel)
    3. Précisez vos instructions spécifiques
    4. Téléchargez le script R généré
    """)

# Formulaire upload fichier sondage
st.header("Fichier de sondage")
survey_file = st.file_uploader("Téléversez votre fichier CSV ou SAV", type=["csv", "sav"])

# Preview des données
if survey_file is not None:
    try:
        if survey_file.name.endswith('.csv'):
            df = pd.read_csv(survey_file)
            st.write("Aperçu des données:")
            st.dataframe(df.head())
        elif survey_file.name.endswith('.sav'):
            st.warning("Support SAV en développement - conversion basique pour prévisualisation")
            # Note: pyreadstat serait utilisé ici dans la version complète
            st.text("Fichier SAV détecté: " + survey_file.name)
    except Exception as e:
        st.error(f"Erreur lors de la lecture du fichier: {e}")

# Upload codebook
st.header("Codebook (optionnel)")
codebook_file = st.file_uploader("Téléversez le codebook", type=["csv", "pdf"])

if codebook_file is not None:
    st.success(f"Codebook téléversé: {codebook_file.name}")

# Instructions spécifiques
st.header("Instructions spécifiques")
instructions = st.text_area("Entrez vos instructions pour le nettoyage du sondage", 
                           placeholder="Ex: Standardiser les variables démographiques, recoder les valeurs manquantes...")

# Bouton pour générer script
if st.button("Générer script R"):
    # Pour le MVP, on retourne un script R statique
    sample_script = """
    # Script de nettoyage généré
    library(tidyverse)
    library(haven) # Pour les fichiers SAV
    
    # Charger les données
    data <- read_csv("chemin/vers/fichier.csv")
    
    # Nettoyer les noms de colonnes
    data <- data %>%
      janitor::clean_names()
    
    # Standardiser valeurs manquantes
    data <- data %>%
      mutate(across(everything(), ~na_if(., "")))
    
    # Préfixes pour variables démographiques
    data <- data %>%
      rename_with(~paste0("demo_", .), c(age, sexe, region))
    
    # Sauvegarder le résultat
    write_rds(data, "donnees_nettoyees.rds")
    """
    
    st.code(sample_script, language="r")
    
    # Bouton téléchargement
    st.download_button(
        label="Télécharger le script R",
        data=sample_script,
        file_name="nettoyage_sondage.R",
        mime="text/plain"
    )