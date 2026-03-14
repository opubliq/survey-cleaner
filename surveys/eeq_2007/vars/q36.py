# op_q36 — Inferred attitude question (Q36)
# Source: q36
# Assumption: Codes '8' and '9' treated as missing as they are unlabelled in the data.
# Note: Value labels are placeholders as no codebook entry was provided.
df_clean['op_q36'] = df['q36'].map({
    '1': 'très important',
    '2': 'assez important',
    '3': 'peu important',
    '4': 'pas du tout important',
    '8': np.nan,
    '9': np.nan,
})
CODEBOOK_VARIABLES['op_q36'] = {
    'original_variable': 'q36',
    'question_label': "Inferred attitude question Q36 (Missing labels)",
    'type': 'categorical',
    'value_labels': {'option_1': "Option 1", 'option_2': "Option 2", 'option_3': "Option 3", 'option_4': "Option 4"},
}