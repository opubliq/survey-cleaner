# behav_ref1995_vote — Vote in the 1995 sovereignty referendum
# Source: Q48
# Assumption: Code 9.0 ("I prefer not to answer") is mapped to np.nan
df_clean['behav_ref1995_vote'] = df['Q48'].map({
    1.0: 'yes',
    2.0: 'no',
    9.0: np.nan,
})
CODEBOOK_VARIABLES['behav_ref1995_vote'] = {
    'original_variable': 'Q48',
    'question_label': "How did you vote?",
    'type': 'categorical',
    'value_labels': {'yes': "Yes", 'no': "No"},
}