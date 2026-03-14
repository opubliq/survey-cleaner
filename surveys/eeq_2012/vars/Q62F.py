# op_vote_frequency — Frequency of voting in the last provincial election
# Source: Q62F
# Assumption: Codes 6.0, 8.0, and 9.0 are treated as missing as they are not documented and likely represent 'Refused', 'Don't know', or 'Not applicable'.
df_clean['op_vote_frequency'] = df['Q62F'].map({
    1.0: 'voted',
    2.0: 'did_not_vote',
    6.0: np.nan,
    8.0: np.nan,
    9.0: np.nan,
})
CODEBOOK_VARIABLES['op_vote_frequency'] = {
    'original_variable': 'Q62F',
    'question_label': "Q62F - (Inferred: Frequency of voting in the last provincial election)",
    'type': 'categorical',
    'value_labels': {'voted': "Voted", 'did_not_vote': "Did not vote"},
}