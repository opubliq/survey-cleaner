# ses_gender — Sex/Gender of the respondent
# Source: qsexe
# Note: Codebook values were missing, assuming 1.0=Male (0.0) and 2.0=Female (1.0) based on binary nature and common practice.
df_clean['ses_gender'] = df['qsexe'].map({
    1.0: 0.0,
    2.0: 1.0,
})
CODEBOOK_VARIABLES['ses_gender'] = {
    'original_variable': 'qsexe',
    'question_label': "Sex/Gender of the respondent (Inferred)",
    'type': 'binary',
    'value_labels': {'0.0': "Male", '1.0': "Female"},
}