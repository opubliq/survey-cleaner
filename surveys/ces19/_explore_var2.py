#!/usr/bin/env python3
import pandas as pd
import numpy as np
import pyreadstat
from datetime import datetime, timedelta

# Load data
df, meta = pyreadstat.read_sav('surveys/ces19/raw/ces_2019.sav', encoding='latin1')

# Convert Stata time to Python datetime
# Stata time is milliseconds since 1960-01-01
stata_epoch = datetime(1960, 1, 1)

print("Converting Stata timestamps to readable dates...")
print("\nSample conversions:")
for i in range(5):
    stata_time = df['cps19_StartDate'].iloc[i]
    python_date = stata_epoch + timedelta(milliseconds=stata_time)
    print(f"  {stata_time:.0f} -> {python_date}")

print("\nDate range:")
min_time = df['cps19_StartDate'].min()
max_time = df['cps19_StartDate'].max()
min_date = stata_epoch + timedelta(milliseconds=min_time)
max_date = stata_epoch + timedelta(milliseconds=max_time)
print(f"  Min: {min_date}")
print(f"  Max: {max_date}")