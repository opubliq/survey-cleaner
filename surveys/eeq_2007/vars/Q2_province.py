# ses_province — Province de résidence
# Source: Q2_province
# Assumption: The raw data column name is 'q2' based on data preview, not 'Q2_province'.
# Assumption: codes are read as floats due to SPSS origin and missing values.
df_clean['ses_province'] = df['q2'].map({
    1.0: 'québec',
    2.0: 'ontario',
    3.0: 'alberta',
    99.0: np.nan,
})
CODEBOOK_VARIABLES['ses_province'] = {
    'original_variable': 'Q2_province',
    'question_label': "Province de résidence",
    'type': 'categorical',
    'value_labels': {'québec': "Québec", 'ontario': "Ontario", 'alberta': "Alberta"},
}