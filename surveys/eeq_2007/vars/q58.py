# ses_province — Province de résidence (Inferred due to missing codebook_entry)
# Source: q58
# Assumption: Codes 01-03 map to Quebec/Ontario/Alberta based on context example. Codes 04/05 are unlabelled and treated as missing. Codes 96-99 are treated as missing.
df_clean['ses_province'] = df['q58'].map({
    '01': 'quebec',
    '02': 'ontario',
    '03': 'alberta',
    '04': np.nan,
    '05': np.nan,
    '96': np.nan,
    '97': np.nan,
    '98': np.nan,
    '99': np.nan,
})
CODEBOOK_VARIABLES['ses_province'] = {
    'original_variable': 'q58',
    'question_label': "Province de résidence (Inferred)",
    'type': 'categorical',
    'value_labels': {'quebec': "Québec", 'ontario': "Ontario", 'alberta': "Alberta"},
}