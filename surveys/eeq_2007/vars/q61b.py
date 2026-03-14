# op_q61b — Frequency of action (inferred)
# Source: q61b
# Assumption: Codes 96, 97, 98, 99 treated as missing (unlabelled in codebook)
df_clean['op_q61b'] = df['q61b'].map({
    '01': 'frequent',
    '02': 'moderate',
    '03': 'infrequent',
    '04': 'very infrequent',
    '05': 'never',
    '96': np.nan,
    '97': np.nan,
    '98': np.nan,
    '99': np.nan,
})
CODEBOOK_VARIABLES['op_q61b'] = {
    'original_variable': 'q61b',
    'question_label': "Frequency of action q61b (INFERRED)",
    'type': 'categorical',
    'value_labels': {'frequent': "01 - Frequent", 'moderate': "02 - Moderate", 'infrequent': "03 - Infrequent", 'very infrequent': "04 - Very Infrequent", 'never': "05 - Never"},
}