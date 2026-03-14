# op_vote_choice — Vote choice (inferred from codes)
# Source: q22
# Assumption: Since no codebook was provided, mapping is inferred from observed codes 1-4, 8, 9.
# Assumption: Codes 8 (Don't Know) and 9 (Refused) are treated as missing.
df_clean['op_vote_choice'] = df['q22'].map({
    '1': 'opt_1',
    '2': 'opt_2',
    '3': 'opt_3',
    '4': 'opt_4',
    '8': np.nan,
    '9': np.nan,
})
CODEBOOK_VARIABLES['op_vote_choice'] = {
    'original_variable': 'q22',
    'question_label': "Vote choice (inferred from codes 1-4, 8, 9)",
    'type': 'categorical',
    'value_labels': {'opt_1': "Option 1", 'opt_2': "Option 2", 'opt_3': "Option 3", 'opt_4': "Option 4"},
}
