# ses_q9 — Avez-vous l'intention de voter aux prochaines élections?
# Source: Q9
# Assumption: codes 8 and 9 treated as missing (unlabelled in codebook)
df_clean['ses_q9'] = df['Q9'].map({
    1.0: 'yes',
    2.0: 'no',
    3.0: 'undecided',
    4.0: 'will_not_vote',
    8.0: np.nan,
    9.0: np.nan,
})
CODEBOOK_VARIABLES['ses_q9'] = {
    'original_variable': 'Q9',
    'question_label': "Avez-vous l'intention de voter aux prochaines élections?",
    'type': 'categorical',
    'value_labels': {'yes': "Oui", 'no': "Non", 'undecided': "Indécis", 'will_not_vote': "Ne votera pas"},
}
