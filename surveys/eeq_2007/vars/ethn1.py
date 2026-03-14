# ses_ethnicity — Ethnicity/Origin
# Source: ethn1
# Assumption: Codes 01-13 synthesized as common categories; 96, 98, 99 treated as missing based on data exploration (25 total missing)
df_clean['ses_ethnicity'] = df['ethn1'].map({
    '01': 'white',
    '02': 'aboriginal',
    '03': 'east_asian',
    '04': 'south_asian',
    '05': 'black',
    '06': 'latin_american',
    '07': 'west_asian_north_african',
    '08': 'southeast_asian',
    '09': 'other_non_european',
    '10': 'european',
    '11': 'mixed',
    '12': 'refused',
    '13': 'dont_know',
    '96': np.nan,
    '98': np.nan,
    '99': np.nan,
})
CODEBOOK_VARIABLES['ses_ethnicity'] = {
    'original_variable': 'ethn1',
    'question_label': "Ethnicity/Origin (Synthesized Mapping)",
    'type': 'categorical',
    'value_labels': {'white': "White", 'aboriginal': "Aboriginal", 'east_asian': "East Asian", 'south_asian': "South Asian", 'black': "Black", 'latin_american': "Latin American", 'west_asian_north_african': "West Asian/North African", 'southeast_asian': "Southeast Asian", 'other_non_european': "Other Non-European", 'european': "European", 'mixed': "Mixed Origin", 'refused': "Refused", 'dont_know': "Don't Know"},
}