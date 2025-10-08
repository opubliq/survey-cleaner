#!/usr/bin/env python3
import pyreadstat

# Load SAV file to get column names - try different encodings
try:
    df, meta = pyreadstat.read_sav('surveys/ces19/raw/ces_2019.sav', encoding='latin1')
except:
    try:
        df, meta = pyreadstat.read_sav('surveys/ces19/raw/ces_2019.sav', encoding='utf-8', encoding_errors='ignore')
    except:
        df, meta = pyreadstat.read_sav('surveys/ces19/raw/ces_2019.sav', encoding='cp1252')

print(f"Total variables: {len(df.columns)}")
print("\nAll column names:")
for col in df.columns:
    print(f"- {col}")