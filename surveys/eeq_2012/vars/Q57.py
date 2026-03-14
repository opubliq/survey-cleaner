# op_vote_intention — Vote intention
# Source: Q57
# Assumption: Variable treated as categorical with common federal party codes for 2012.
# Assumption: Missing code 99 treated as np.nan.
df_clean['op_vote_intention'] = df['Q57'].map({
    1.0: 'conservative',
    2.0: 'liberal',
    3.0: 'bloc_quebecois',
    4.0: 'ndp',
    5.0: 'green',
    99.0: np.nan,
})
CODEBOOK_VARIABLES['op_vote_intention'] = {
    'original_variable': 'Q57',
    'question_label': "Vote intention (Assumed: Conservative, Liberal, BQ, NDP, Green)",
    'type': 'categorical',
    'value_labels': {'conservative': "Conservative", 'liberal': "Liberal", 'bloc_quebecois': "Bloc Québécois", 'ndp': "NDP", 'green': "Green"},
}