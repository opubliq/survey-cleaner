# op_q37 — Response to Q37 (Inferred mapping due to missing codebook)
# Source: Q37
# Assumption: Codes 8.0 and 9.0 treated as missing/refusal (not explicitly labelled)
df_clean['op_q37'] = df['Q37'].map({
    1.0: 'option_a',
    2.0: 'option_b',
    8.0: np.nan,
    9.0: np.nan,
})
CODEBOOK_VARIABLES['op_q37'] = {
    'original_variable': 'Q37',
    'question_label': "Response to Q37 (Value labels inferred)",
    'type': 'categorical',
    'value_labels': {'option_a': "Option A", 'option_b': "Option B"},
}