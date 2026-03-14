# op_vote_group_g — Grouped voting intention or attitude G
# Source: Q33G
# Assumption: Codes 1-4 are valid categories. Codes 8 and 9 are unlabelled and treated as missing.
df_clean['op_vote_group_g'] = df['Q33G'].map({
    1.0: 'option_a',
    2.0: 'option_b',
    3.0: 'option_c',
    4.0: 'option_d',
    8.0: np.nan,
    9.0: np.nan,
})
CODEBOOK_VARIABLES['op_vote_group_g'] = {
    'original_variable': 'Q33G',
    'question_label': "Unknown question label for Q33G, inferred as grouped opinion/vote.",
    'type': 'categorical',
    'value_labels': {'option_a': "Option A", 'option_b': "Option B", 'option_c': "Option C", 'option_d': "Option D"},
}