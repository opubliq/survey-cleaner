# know_voter_intent — Voter intention or related knowledge question (inferred)
# Source: q52
# Assumption: Codes 8 and 9 are treated as missing (unlabelled in codebook).
# The meaning of codes 1-4 is inferred as primary choices.
df_clean['know_voter_intent'] = df['q52'].map({
    '1': 'choice_1',
    '2': 'choice_2',
    '3': 'choice_3',
    '4': 'choice_4',
    '8': np.nan,
    '9': np.nan,
})
CODEBOOK_VARIABLES['know_voter_intent'] = {
    'original_variable': 'q52',
    'question_label': "Voter intention or related knowledge question (inferred)",
    'type': 'categorical',
    'value_labels': {'choice_1': "Choice 1", 'choice_2': "Choice 2", 'choice_3': "Choice 3", 'choice_4': "Choice 4"},
}