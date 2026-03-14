# op_q11 — Inferred opinion variable, label unknown
# Source: Q11
# CRITICAL: Missing codebook entry. Labels are placeholders. Codes 8.0 and 9.0 assumed missing.
df_clean['op_q11'] = df['Q11'].map({
    1.0: 'choice_a',
    2.0: 'choice_b',
    3.0: 'choice_c',
    4.0: 'choice_d',
    8.0: np.nan,
    9.0: np.nan,
})
CODEBOOK_VARIABLES['op_q11'] = {
    'original_variable': 'Q11',
    'question_label': "Unknown Question Text (Codebook Missing)",
    'type': 'categorical',
    'value_labels': {'choice_a': "Label A (Placeholder)", 'choice_b': "Label B (Placeholder)", 'choice_c': "Label C (Placeholder)", 'choice_d': "Label D (Placeholder)"},
}
