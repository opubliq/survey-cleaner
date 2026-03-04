#!/usr/bin/env python3
"""
Transform codebook from Excel file to codebook.json
Source: Participation ÉGM 2021_Base de données.xlsx
- Index sheet: Variable names and question text
- DGE04QT sheet: Survey data with variable values
"""

import pandas as pd
import json
import numpy as np
from pathlib import Path

# Paths
SHARED_FOLDER = Path("/home/hubcad25/Dropbox/_SharedFolder_data_produit/elxnqc_particip_egm_2021/")
SURVEY_DIR = Path("/home/hubcad25/opubliq/repos/survey-cleaner/surveys/elxnqc_particip_egm_2021/")
xlsx_path = SHARED_FOLDER / "Participation ÉGM 2021_Base de données.xlsx"

# Read the Index sheet for question text
df_index = pd.read_excel(xlsx_path, sheet_name="Index")
df_index.columns = ["variable", "question"]
question_dict = dict(zip(df_index["variable"], df_index["question"]))

# Read the data sheet
df_data = pd.read_excel(xlsx_path, sheet_name="DGE04QT")

print(f"Variables in Index: {len(question_dict)}")
print(f"Variables in Data: {len(df_data.columns)}")

# Determine variable type based on data
def get_var_type(series):
    """Determine variable type from pandas series"""
    # Drop NaN for analysis
    clean_series = series.dropna()
    if len(clean_series) == 0:
        return "text"  # Default for empty
    
    # Check if numeric
    if pd.api.types.is_numeric_dtype(series):
        unique_count = clean_series.nunique()
        # If few unique values, treat as categorical
        if unique_count <= 20:
            return "categorical"
        # If continuous (many unique values, could be age, etc.)
        return "continuous"
    else:
        return "text"

# Build codebook
variables = {}

for var_name in df_data.columns:
    # Get question text
    question = question_dict.get(var_name, None)
    
    # Get variable type
    var_type = get_var_type(df_data[var_name])
    
    # Get unique values (excluding NaN)
    unique_values = df_data[var_name].dropna().unique()
    
    # Convert to sorted list of strings for JSON keys
    unique_str_values = sorted([str(int(v)) if isinstance(v, float) and v == int(v) else str(v) for v in unique_values], 
                               key=lambda x: (not x.isdigit(), int(x) if x.isdigit() else x))
    
    # Cap at 25 values - if more, don't include values (will be inferred from data later)
    if len(unique_str_values) > 25:
        values = {}
    else:
        # Create values dict with null labels (no explicit labels in source)
        values = {v: None for v in unique_str_values}
    
    # Build variable entry
    var_entry = {
        "question": question,
        "type": var_type,
        "values": values
    }
    
    variables[var_name] = var_entry

# Create final codebook
codebook = {
    "survey_id": "elxnqc_particip_egm_2021",
    "variables": variables
}

# Write to JSON
output_path = SHARED_FOLDER / "codebook.json"
with open(output_path, "w", encoding="utf-8") as f:
    json.dump(codebook, f, ensure_ascii=False, indent=2)

print(f"\nCodebook written to: {output_path}")
print(f"Total variables: {len(variables)}")

# Show sample
print("\n--- Sample entries (first 3) ---")
for i, (var_name, var_info) in enumerate(list(variables.items())[:3]):
    print(f"\n{var_name}:")
    print(f"  Question: {var_info['question'][:80] if var_info['question'] else None}...")
    print(f"  Type: {var_info['type']}")
    print(f"  Values: {list(var_info['values'].keys())[:10]}...")
