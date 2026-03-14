# op_vote_choice — Vote choice
# Source: Q75
# Assumption: Codes 8.0 and 9.0 are treated as missing values (Refused/Not applicable). Mapping for 1.0-4.0 is inferred as no codebook was provided.
df_clean['op_vote_choice'] = df['Q75'].map({
    1.0: 'candidate_a',
    2.0: 'candidate_b',
    3.0: 'candidate_c',
    4.0: 'other',
    8.0: np.nan,
    9.0: np.nan,
})
CODEBOOK_VARIABLES['op_vote_choice'] = {
    'original_variable': 'Q75',
    'question_label': "Vote choice (Inferred)",
    'type': 'categorical',
    'value_labels': {'candidate_a': "Candidate A", 'candidate_b': "Candidate B", 'candidate_c': "Candidate C", 'other': "Other/Other party"},
}
