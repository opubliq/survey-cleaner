# ses_voted_2006 — A voté à l'élection fédérale de 2006
# Source: q57
# Assumption: codes 96, 97, 98, 99 treated as missing (not fully labelled in codebook)
df_clean['ses_voted_2006'] = df['q57'].map({
    1.0: 'yes',
    2.0: 'no',
    3.0: 'did_not_vote',
    4.0: 'does_not_know',
    5.0: 'refused',
    96.0: np.nan,
    97.0: np.nan,
    98.0: np.nan,
    99.0: np.nan,
})
CODEBOOK_VARIABLES['ses_voted_2006'] = {
    'original_variable': 'q57',
    'question_label': "Avez-vous voté à l'élection fédérale de 2006?",
    'type': 'categorical',
    'value_labels': {'yes': "Oui", 'no': "Non", 'did_not_vote': "Ne s'est pas présenté", 'does_not_know': "Ne sait pas", 'refused': "Refus"},
}
