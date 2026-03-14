# op_vote_choice — Hypothetical vote choice question
# Source: q1
# Assumption: Codes 1.0-6.0 are choices, 96.0 is missing/refused.
df_clean['op_vote_choice'] = df['q1'].map({
    1.0: 'parti_a',
    2.0: 'parti_b',
    3.0: 'parti_c',
    4.0: 'parti_d',
    5.0: 'parti_e',
    6.0: 'parti_f',
    96.0: np.nan, # TODO: verify mapping and labels for codes 1.0-96.0
})
CODEBOOK_VARIABLES['op_vote_choice'] = {
    'original_variable': 'q1',
    'question_label': "Hypothetical vote choice question (Codebook missing)",
    'type': 'categorical',
    'value_labels': {'parti_a': "Choice 1 (Unknown Label)", 'parti_b': "Choice 2 (Unknown Label)", 'parti_c': "Choice 3 (Unknown Label)", 'parti_d': "Choice 4 (Unknown Label)", 'parti_e': "Choice 5 (Unknown Label)", 'parti_f': "Choice 6 (Unknown Label)"},
}