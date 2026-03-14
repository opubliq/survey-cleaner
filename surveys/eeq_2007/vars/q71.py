# op_voter_intention — Assumed to be voter intention: Party 1, 2, 3, or 4
# Source: q71
# Assumption: Codes 8 and 9 are treated as missing (not present in codebook)
df_clean['op_voter_intention'] = df['q71'].map({
    '1': 'vote_party_1',
    '2': 'vote_party_2',
    '3': 'vote_party_3',
    '4': 'vote_party_4',
    '8': np.nan,
    '9': np.nan,
})
CODEBOOK_VARIABLES['op_voter_intention'] = {
    'original_variable': 'q71',
    'question_label': "Assumed Voter Intention (Based on codes 1-4)",
    'type': 'categorical',
    'value_labels': {'vote_party_1': "Vote Party 1", 'vote_party_2': "Vote Party 2", 'vote_party_3': "Vote Party 3", 'vote_party_4': "Vote Party 4"},
}