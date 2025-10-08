#!/usr/bin/env python3
import pandas as pd
import numpy as np
import pyreadstat

# Load data
df, meta = pyreadstat.read_sav('surveys/ces19/raw/ces_2019.sav', encoding='latin1')

# Explore variable: cps19_StartDate
var_name = 'cps19_StartDate'
print("=" * 60)
print(f"VARIABLE: {var_name}")
print("=" * 60)
print(f"\nData type: {df[var_name].dtype}")
print(f"Unique values: {df[var_name].nunique()}")
print(f"Missing values: {df[var_name].isna().sum()} ({df[var_name].isna().sum() / len(df) * 100:.2f}%)")

# Since it's StartDate, likely datetime
print("\nFirst 20 values:")
print(df[var_name].head(20))

print("\nValue distribution (head):")
print(df[var_name].value_counts().head(20))

print("\nData sample:")
print(df[var_name].describe())