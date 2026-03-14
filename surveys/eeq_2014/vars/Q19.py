# op_q19 — Likely a choice question response for Q19
# Source: Q19
# Assumption: Codes 8.0 (Don't Know) and 9.0 (Refused) are mapped to np.nan as they are unlabelled here.
df_clean['op_q19'] = df['Q19'].map({
    1.0: 'choice_a',
    2.0: 'choice_b',
    8.0: np.nan,
    9.0: np.nan,
})
CODEBOOK_VARIABLES['op_q19'] = {
    'original_variable': 'Q19',
    'question_label': "Response to question 19 (inferred)",
    'type': 'categorical',
    'value_labels': {'choice_a': "First Option", 'choice_b': "Second Option"},
}