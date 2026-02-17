import pandas as pd
import numpy as np
from pathlib import Path

# Use data file path provided by orchestrator
data_file = Path("_SharedFolder_data_produit/elxnqc_particip_egm_2021/Participation ÉGM 2021_Base de données.xlsx")

if data_file.suffix == ".csv":
    df = pd.read_csv(data_file)
elif data_file.suffix == ".sav":
    import pyreadstat
    df, meta = pyreadstat.read_sav(data_file)
elif data_file.suffix in [".xlsx", ".xls"]:
    df = pd.read_excel(data_file)

# Variable to analyze
var_name = "q12_m2"

if var_name not in df.columns:
    print(f"ERROR: Variable '{var_name}' not found in data")
    print(f"Available columns: {', '.join(df.columns[:10])}...")
    exit(1)

# Analyze variable
print(f"Variable: {var_name}")
print(f"Type: {df[var_name].dtype}")
print(f"Missing: {df[var_name].isna().sum()} / {len(df)} ({df[var_name].isna().mean()*100:.1f}%)")
print(f"\nValue counts:")
print(df[var_name].value_counts().sort_index().head(20))
print(f"\nUnique values: {df[var_name].nunique()}")

# Basic stats if numeric
if df[var_name].dtype in ['int64', 'float64']:
    print(f"\nStats:")
    print(df[var_name].describe())