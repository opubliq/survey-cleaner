# op_vote_intention — Intention de voter (Question 101B)
# Source: Q101B
# Assumption: Codes 8.0 and 9.0 are treated as missing/refused based on typical survey practice for codes not explicitly labelled as valid responses.
df_clean['op_vote_intention'] = df['Q101B'].map({
    1.0: 'yes',
    2.0: 'no',
    8.0: np.nan,
    9.0: np.nan,
})
CODEBOOK_VARIABLES['op_vote_intention'] = {
    'original_variable': 'Q101B',
    'question_label': "Intention de voter (Question 101B)",
    'type': 'categorical',
    'value_labels': {'yes': 'Oui', 'no': 'Non'},
}
