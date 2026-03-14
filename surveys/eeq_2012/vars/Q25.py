# op_response_q25 — Response to question Q25
# Source: Q25
# Assumption: Codes 96.0 and 99.0 are treated as missing. Categories 1.0-6.0 mapped to generic labels due to missing codebook.
df_clean['op_response_q25'] = df['Q25'].map({
    1.0: 'category_a',
    2.0: 'category_b',
    3.0: 'category_c',
    4.0: 'category_d',
    5.0: 'category_e',
    6.0: 'category_f',
    96.0: np.nan,
    99.0: np.nan,
})
CODEBOOK_VARIABLES['op_response_q25'] = {
    'original_variable': 'Q25',
    'question_label': "Response to Q25 (Label unknown)",
    'type': 'categorical',
    'value_labels': {'category_a': "Category A", 'category_b': "Category B", 'category_c': "Category C", 'category_d': "Category D", 'category_e': "Category E", 'category_f': "Category F"},
}