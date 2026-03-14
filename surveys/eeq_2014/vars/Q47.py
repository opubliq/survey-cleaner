# op_opinion_q47 — Hypothetical opinion variable based on codes observed
# Source: Q47
# Assumption: Codes 8 and 9 treated as missing (not explicitly labelled in codebook)
df_clean['op_opinion_q47'] = df['Q47'].map({
    1.0: 'value_1',
    2.0: 'value_2',
    3.0: 'value_3',
    8.0: np.nan,
    9.0: np.nan,
})
CODEBOOK_VARIABLES['op_opinion_q47'] = {
    'original_variable': 'Q47',
    'question_label': "Hypothetical question for Q47",
    'type': 'categorical',
    'value_labels': {'value_1': "Option 1", 'value_2': "Option 2", 'value_3': "Option 3"},
}