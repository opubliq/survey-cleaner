# op_q21 — Generic opinion variable Q21
# Source: Q21
# Assumption: codes 8.0 and 9.0 are treated as missing (not in assumed codebook)
df_clean['op_q21'] = df['Q21'].map({
    1.0: 'yes',
    2.0: 'no',
    8.0: np.nan,
    9.0: np.nan,
})
CODEBOOK_VARIABLES['op_q21'] = {
    'original_variable': 'Q21',
    'question_label': "Question 21 - Placeholder Label",
    'type': 'categorical',
    'value_labels': {'yes': "Yes", 'no': "No"},
}
