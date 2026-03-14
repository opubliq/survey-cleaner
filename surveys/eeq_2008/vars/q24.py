# op_q24 — Opinion on unknown topic for Q24
# Source: q24
# Assumption: Codes 8 and 9 are treated as missing based on exploration.
df_clean['op_q24'] = df['q24'].map({
    1.0: 'yes',
    2.0: 'no',
    3.0: 'dont_know',
    8.0: np.nan,
    9.0: np.nan,
})
CODEBOOK_VARIABLES['op_q24'] = {
    'original_variable': 'q24',
    'question_label': "Question 24 Label (Placeholder)",
    'type': 'categorical',
    'value_labels': {'yes': "Yes", 'no': "No", 'dont_know': "Don't know"},
}