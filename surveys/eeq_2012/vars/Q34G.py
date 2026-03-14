# op_q34g — General response to Q34G
# Source: Q34G
# Assumption: Only codes 1.0 ('Oui') and 2.0 ('Non') are mapped. Other codes (3, 4, 8, 9) are treated as missing as they lack labels.
df_clean['op_q34g'] = df['Q34G'].map({
    1.0: 'oui',
    2.0: 'non',
    3.0: np.nan,
    4.0: np.nan,
    8.0: np.nan,
    9.0: np.nan,
})
CODEBOOK_VARIABLES['op_q34g'] = {
    'original_variable': 'Q34G',
    'question_label': "Q34G",
    'type': 'categorical',
    'value_labels': {'oui': "Oui", 'non': "Non"},
}