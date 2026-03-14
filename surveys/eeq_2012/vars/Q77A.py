# ses_voting_intention_conservative — Intention de vote conservateur
# Source: Q77A
# Assumption: codes 8/9 treated as missing (unlabelled in codebook)
df_clean['ses_voting_intention_conservative'] = df['Q77A'].map({
    1.0: 'yes',
    2.0: 'no',
    3.0: 'undecided',
    4.0: 'none',
    8.0: np.nan,
    9.0: np.nan,
})
CODEBOOK_VARIABLES['ses_voting_intention_conservative'] = {
    'original_variable': 'Q77A',
    'question_label': "Votez-vous pour le Parti conservateur lors des prochaines élections fédérales?",
    'type': 'categorical',
    'value_labels': {'yes': "Oui", 'no': "Non", 'undecided': "Indécis", 'none': "Aucun"},
}