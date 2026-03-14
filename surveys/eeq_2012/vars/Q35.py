# op_voting_intention — Voting intention in the upcoming election
# Source: Q35
# Assumption: Codes 1-4 are main parties. Codes 8 and 9 are treated as missing.
# TODO: verify mapping against actual eeq_2012 codebook
df_clean['op_voting_intention'] = df['Q35'].map({
    1.0: 'liberal',
    2.0: 'caq',
    3.0: 'péquiste',
    4.0: 'conservateur',
    8.0: np.nan,
    9.0: np.nan,
})
CODEBOOK_VARIABLES['op_voting_intention'] = {
    'original_variable': 'Q35',
    'question_label': "Voting intention (Inferred)",
    'type': 'categorical',
    'value_labels': {'liberal': "Liberal", 'caq': "CAQ", 'péquiste': "Péquiste", 'conservateur': "Conservateur"},
}