# op_vote_intention — Vote intention (inferred)
# Source: q79
# Assumption: codes 1-7 mapped to placeholder labels; codes 96/99 treated as missing.
df_clean['op_vote_intention'] = df['q79'].map({
    1.0: 'party a',
    2.0: 'party b',
    3.0: 'party c',
    4.0: 'party d',
    5.0: 'party e',
    6.0: 'party f',
    7.0: 'party g',
    96.0: np.nan,
    99.0: np.nan,
})
CODEBOOK_VARIABLES['op_vote_intention'] = {
    'original_variable': 'q79',
    'question_label': "Vote intention (inferred)",
    'type': 'categorical',
    'value_labels': {'party a': "Party A", 'party b': "Party B", 'party c': "Party C", 'party d': "Party D", 'party e': "Party E", 'party f': "Party F", 'party g': "Party G"},
}