# app.py
import streamlit as st
import pandas as pd
import os
from io import StringIO
from utils.parsers import parse_csv, extract_structure, format_data_for_llm
from utils.llm_interface import prompt_llm

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
# Remplacer la section de preview des données par:
if survey_file is not None:
    try:
        if survey_file.name.endswith('.csv'):
            # Parsage du CSV
            df, error = parse_csv(survey_file)
            if error:
                st.error(f"Erreur: {error}")
            else:
                # Extraction de la structure
                structure = extract_structure(df)
                
                # Affichage aperçu
                st.write("Aperçu des données:")
                st.dataframe(df.head())
                
                # Préparation des données pour le LLM
                st.session_state['data_prompt'] = format_data_for_llm(df, structure)
                
        elif survey_file.name.endswith('.sav'):
            st.warning("Support SAV en développement")
    except Exception as e:
        st.error(f"Erreur: {e}")

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
    if 'data_prompt' not in st.session_state:
        st.error("Aucune donnée chargée.")
    else:
        prompt = f"""
    Génère uniquement un script R.
    
    But : nettoyer un fichier de sondage brut en appliquant les instructions ci-dessous.
    
    Données brutes :
    {st.session_state['data_prompt']}
    
    Instructions de nettoyage à appliquer, strictement dans l’ordre :
    {instructions}
    
    Contraintes :
    - Utilise tidyverse
    - Ne commente pas le code
    - Ne montre aucune sortie ou aperçu
    - Ne fais aucune explication
    - Résultat : un `data.frame` nommé `data`
    
    Retourne **uniquement** le script R, rien d’autre.
"""
        
    with st.spinner("Génération du script..."):
        try:
            r_script = prompt_llm(prompt)
            st.code(r_script, language="r")
            st.download_button(
                label="Télécharger le script R",
                data=r_script,
                file_name="nettoyage_sondage.R",
                mime="text/plain"
            )
        except Exception as e:
            st.error(f"Erreur lors de la génération : {e}")