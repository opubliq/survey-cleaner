# ses_frequency — General frequency of voting (or not) in the last election
# Source: Q26A
# Assumption: codes 8 and 9 are missing and will be mapped to np.nan.
# Codebook: {"1": "Voted", "2": "Did not vote", "8": "Refused", "9": "Don't know"}
df_clean['ses_frequency'] = df['Q26A'].map({
    1.0: 'voted',
    2.0: 'did not vote',
    8.0: np.nan,
    9.0: np.nan,
})
CODEBOOK_VARIABLES['ses_frequency'] = {
    'original_variable': 'Q26A',
    'question_label': "Fréquence de vote (dernière élection)",
    'type': 'categorical',
    'value_labels': {'voted': "Voted", 'did not vote': "Did not vote"},
}