# op_vote_intention — Vote intention (Inferred mapping)
# Source: Q33C
# Assumption: Codes 1-4 are parties; 8/9 are missing.
# TODO: Verify mapping against official codebook for eeq_2012.
df_clean['op_vote_intention'] = df['Q33C'].map({
    1.0: 'parti_a',
    2.0: 'parti_b',
    3.0: 'parti_c',
    4.0: 'parti_d',
    8.0: np.nan,
    9.0: np.nan
})
CODEBOOK_VARIABLES['op_vote_intention'] = {
    'original_variable': 'Q33C',
    'question_label': "Vote intention (Inferred)",
    'type': 'categorical',
    'value_labels': {
        'parti_a': 'Parti A', 'parti_b': 'Parti B', 'parti_c': 'Parti C', 'parti_d': 'Parti D'
    }
}