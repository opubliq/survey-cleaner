# utils/parsers.py
import pandas as pd
import re

def parse_csv(file_path, encoding='utf-8', **kwargs):
    """Parse un fichier CSV de sondage et retourne un DataFrame."""
    try:
        df = pd.read_csv(file_path, encoding=encoding, **kwargs)
        return df, None
    except Exception as e:
        return None, str(e)

def extract_structure(df):
    """Extrait la structure d'un DataFrame (types, colonnes)."""
    structure = {
        'colonnes': df.columns.tolist(),
        'types': {col: str(df[col].dtype) for col in df.columns},
        'missing_values': {col: df[col].isna().sum() for col in df.columns},
        'unique_values': {col: df[col].nunique() for col in df.columns},
        'échantillon': df.head(5).to_dict('records')
    }
    return structure

def format_data_for_llm(df, structure):
    """Prépare un texte descriptif du dataset pour le modèle LLM."""
    prompt = f"Structure du fichier CSV:\n"
    prompt += f"- {len(df)} lignes, {len(df.columns)} colonnes\n"
    prompt += f"- Colonnes: {', '.join(structure['colonnes'])}\n\n"
    prompt += f"Aperçu des 5 premières lignes:\n{df.head().to_string()}\n\n"
    prompt += f"Statistiques des valeurs manquantes:\n"
    
    for col, missing in structure['missing_values'].items():
        if missing > 0:
            prompt += f"- {col}: {missing} valeurs manquantes\n"
            
    return prompt