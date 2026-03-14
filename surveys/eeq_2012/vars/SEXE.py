# ses_gender — Province de résidence
# Source: SEXE
# Assumption: Codes 1.0/2.0 map to Male/Female, respectively. Missing values are automatically handled as NaN.
df_clean['ses_gender'] = df['SEXE'].map({
    1.0: 'male',
    2.0: 'female',
})
CODEBOOK_VARIABLES['ses_gender'] = {
    'original_variable': 'SEXE',
    'question_label': "Province de résidence",
    'type': 'categorical',
    'value_labels': {'male': "Male", 'female': "Female"},
}