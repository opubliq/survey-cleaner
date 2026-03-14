# behav_vote_choice_party_4 — Vote choice for the four main parties
# Source: Q34D
# Assumption: Codes 8 and 9 are treated as missing (Refused/Don't Know)
df_clean['behav_vote_choice_party_4'] = df['Q34D'].map({
    1.0: 'liberal',
    2.0: 'conservative',
    3.0: 'ndp',
    4.0: 'bloc_quebecois',
    8.0: np.nan,
    9.0: np.nan,
})
CODEBOOK_VARIABLES['behav_vote_choice_party_4'] = {
    'original_variable': 'Q34D',
    'question_label': "Vote choice (4 main parties)",
    'type': 'categorical',
    'value_labels': {'liberal': "Liberal Party", 'conservative': "Conservative Party", 'ndp': "NDP", 'bloc_quebecois': "Bloc Québécois"},
}