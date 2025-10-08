#!/usr/bin/env python3
import pandas as pd
import numpy as np
import pyreadstat
from datetime import datetime

# Load data with metadata
df, meta = pyreadstat.read_sav('surveys/ces19/raw/ces_2019.sav', encoding='latin1')

# Check variable metadata
print("Variable format information:")
if hasattr(meta, 'variable_value_labels'):
    print(f"Value labels: {meta.variable_value_labels.get('cps19_StartDate', 'None')}")
if hasattr(meta, 'variable_display_width'):
    print(f"Display width: {meta.variable_display_width.get('cps19_StartDate', 'None')}")
if hasattr(meta, 'original_variable_types'):
    print(f"Original type: {meta.original_variable_types.get('cps19_StartDate', 'None')}")

# Try different interpretations
stata_value = df['cps19_StartDate'].iloc[0]
print(f"\nRaw Stata value: {stata_value}")

# Interpretation 1: Stata datetime (milliseconds since 1960-01-01)
stata_epoch = datetime(1960, 1, 1)
from datetime import timedelta
date1 = stata_epoch + timedelta(milliseconds=stata_value)
print(f"As milliseconds from 1960-01-01: {date1}")

# Interpretation 2: Seconds since 1960-01-01
date2 = stata_epoch + timedelta(seconds=stata_value)
print(f"As seconds from 1960-01-01: {date2}")

# Interpretation 3: Unix timestamp (seconds since 1970-01-01)
try:
    date3 = datetime.fromtimestamp(stata_value)
    print(f"As Unix timestamp: {date3}")
except:
    print("Not a valid Unix timestamp")

# Interpretation 4: Stata tc format (milliseconds)
# CES 2019 was conducted in 2019, so we expect dates around Sep-Oct 2019
# Let's check if it's stored differently
print("\n\nLet's try converting as Stata date-time:")
# In Stata, %tc format is milliseconds since 1960-01-01 00:00:00
# But the value seems very large for that
print(f"Value / 1000 = {stata_value / 1000} (seconds)")
print(f"Value / 1000000 = {stata_value / 1000000} (thousands of seconds)")

# Check if pyreadstat converted it
print("\n\nChecking metadata for format information:")
print(dir(meta))