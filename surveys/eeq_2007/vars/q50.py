# behav_vote_intention_last_election — Vote intention (last election)
# Source: q50
# Assumption: Codes 5, 6, 7 not observed, mapped to np.nan. Code 99 treated as missing.
df_clean['behav_vote_intention_last_election'] = df['q50'].map({
    '1': 'bq',
    '2': 'pc',
    '3': 'lpc',
    '4': 'npd',
    '8': 'autre',
    '9': 'refuse_no_vote',
    # Explicitly map any other codes (like 99) to nan if they appear as strings
    '99': np.nan,
})
CODEBOOK_VARIABLES['behav_vote_intention_last_election'] = {
    'original_variable': 'q50',
    'question_label': "Vote intention (last election)",
    'type': 'categorical',
    'value_labels': {'bq': "Bloc Québécois", 'pc': "Conservateur", 'lpc': "Libéral", 'npd': "NPD", 'autre': "Autre parti", 'refuse_no_vote': "Ne votera pas"},
}