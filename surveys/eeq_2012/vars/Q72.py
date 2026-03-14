# behav_q72 — Likely outcome of vote for Q72 (Requires codebook verification)
# Source: Q72
# Note: Missing the codebook entry. Codes 8/9 assumed missing based on common practice.
df_clean['behav_q72'] = df['Q72'].map({
    1.0: 'category_a',
    2.0: 'category_b',
    8.0: np.nan,
    9.0: np.nan,
})
CODEBOOK_VARIABLES['behav_q72'] = {
    'original_variable': 'Q72',
    'question_label': "Likely outcome of vote for Q72 (Requires codebook verification)",
    'type': 'categorical',
    'value_labels': {'category_a': 'Category A (Verify)', 'category_b': 'Category B (Verify)'},
}