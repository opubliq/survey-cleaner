# op_voted_for — Vote intention
# Source: Q59
# Assumption: Codes 8.0 and 9.0 are treated as missing (unlabelled in data exploration)
# TODO: Verify actual meaning of codes 1-5 and map to concise labels. Using placeholders now.
df_clean['op_voted_for'] = df['Q59'].map({
    1.0: 'party_a',
    2.0: 'party_b',
    3.0: 'party_c',
    4.0: 'party_d',
    5.0: 'none',
    8.0: np.nan,
    9.0: np.nan,
})
CODEBOOK_VARIABLES['op_voted_for'] = {
    'original_variable': 'Q59',
    'question_label': "Vote intention (Placeholder mapping)",
    'type': 'categorical',
    'value_labels': {'party_a': "Party A", 'party_b': "Party B", 'party_c': "Party C", 'party_d': "Party D", 'none': "None"},
}