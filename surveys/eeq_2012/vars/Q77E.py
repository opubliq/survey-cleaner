# op_vote_intention — Vote intention
# Source: Q77E
# Assumption: Inferred mapping based on common election study variable structure and observed codes 8/9.
df_clean['op_vote_intention'] = df['Q77E'].map({
    1.0: 'vote_1',
    2.0: 'vote_2',
    3.0: 'vote_3',
    4.0: 'vote_4',
    8.0: 'dk',
    9.0: 'refused',
})
CODEBOOK_VARIABLES['op_vote_intention'] = {
    'original_variable': 'Q77E',
    'question_label': "Vote intention (Inferred mapping)",
    'type': 'categorical',
    'value_labels': {'vote_1': "Vote for Party 1", 'vote_2': "Vote for Party 2", 'vote_3': "Vote for Party 3", 'vote_4': "Vote for Party 4", 'dk': "Don't know", 'refused': "Refused"},
}