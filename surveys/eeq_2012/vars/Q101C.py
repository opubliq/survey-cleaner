# behav_vote_option — Inferred vote option
# Source: Q101C
# Assumption: Codes 8.0 and 9.0 treated as missing (unlabelled in codebook)
df_clean['behav_vote_option'] = df['Q101C'].map({
    1.0: 'option_one',
    2.0: 'option_two',
    8.0: np.nan,
    9.0: np.nan,
})
CODEBOOK_VARIABLES['behav_vote_option'] = {
    'original_variable': 'Q101C',
    'question_label': "Inferred vote option (1 or 2), codes 8/9 as missing",
    'type': 'categorical',
    'value_labels': {'option_one': 'Option 1', 'option_two': 'Option 2'},
}
