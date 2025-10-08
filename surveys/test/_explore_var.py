import pandas as pd
import numpy as np
from pathlib import Path

# Load data
survey_dir = Path("surveys/test")
raw_dir = survey_dir / "raw"
data_file = raw_dir / "data.csv"

df = pd.read_csv(data_file)

var_name = "nom"

print("=" * 60)
print(f"VARIABLE: {var_name}")
print("=" * 60)
print(f"\nData type: {df[var_name].dtype}")
print(f"Unique values: {df[var_name].nunique()}")
print(f"Missing values: {df[var_name].isna().sum()}")
print(f"Missing %: {df[var_name].isna().sum() / len(df) * 100:.1f}%")

# Type-specific exploration
if df[var_name].dtype in ['object', 'category']:
    print("\nValue counts (top 20):")
    print(df[var_name].value_counts(dropna=False).head(20))
    print("\nFirst 10 values:")
    print(df[var_name].head(10))
elif df[var_name].dtype in ['int64', 'float64']:
    print("\nDescriptive stats:")
    print(df[var_name].describe())
    if df[var_name].nunique() <= 30:
        print("\nValue counts:")
        print(df[var_name].value_counts(dropna=False).sort_index())
else:
    print("\nFirst 10 values:")
    print(df[var_name].head(10))
