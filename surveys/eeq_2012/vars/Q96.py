# ses_region_q96 — Inferred region/category from Q96
# Source: Q96
# Assumption: Codes 8/9 are missing/unlabelled based on float dtype and value distribution.
df_clean['ses_region_q96'] = df['Q96'].map({
    1.0: 'option_a',
    2.0: 'option_b',
    8.0: np.nan,
    9.0: np.nan,
})
CODEBOOK_VARIABLES['ses_region_q96'] = {
    'original_variable': 'Q96',
    'question_label': "Unknown question label for Q96",
    'type': 'categorical',
    'value_labels': {'option_a': "Option A (Inferred)", 'option_b': "Option B (Inferred)"},
}