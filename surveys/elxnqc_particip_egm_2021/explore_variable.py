import pandas as pd
import numpy as np
from pathlib import Path

data_file = Path('/home/hubcad25/opubliq/repos/survey-cleaner/_SharedFolder_data_produit/elxnqc_particip_egm_2021/Participation ÉGM 2021_Base de données.xlsx')
if data_file.suffix == '.csv':
    df = pd.read_csv(data_file)
elif data_file.suffix == '.sav':
    import pyreadstat
    df, meta = pyreadstat.read_sav(data_file)
elif data_file.suffix in ['.xlsx', '.xls']:
    df = pd.read_excel(data_file)

var_name = 'caseid'
if var_name not in df.columns:
    print('ERROR: Variable '{}' not found in data'.format(var_name))
    print('Available columns: {}...'.format(', '.join(df.columns[:10])))
    exit(1)

print('Variable: {}'.format(var_name))
print('Type: {}'.format(df[var_name].dtype))
print('Missing: {} / {} ({:.1f}%)'.format(df[var_name].isna().sum(), len(df), df[var_name].isna().mean()*100))
print('\nValue counts:')
print(df[var_name].value_counts().sort_index().head(20))
print('\nUnique values: {}'.format(df[var_name].nunique()))
if df[var_name].dtype in ['int64', 'float64']:
    print('\nStats:')
    print(df[var_name].describe())
