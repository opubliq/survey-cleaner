# behav_referendum_intent — Hypothetical referendum voting intent
# Source: q20
df_clean['behav_referendum_intent'] = df['q20'].map({
    '1': 'yes',
    '2': 'no',
    '3': 'would_not_vote',
    '8': np.nan,
    '9': np.nan,
})
CODEBOOK_VARIABLES['behav_referendum_intent'] = {
    'original_variable': 'q20',
    'question_label': "Même si vous n'avez peut-être pas encore fait votre choix, s'il y avait un référendum aujourd'hui sur cette question, seriez-vous tenté(e) de voter pour le OUI ou pour le NON ?",
    'type': 'categorical',
    'value_labels': {'yes': 'Oui', 'no': 'Non', 'would_not_vote': 'Ne voterait pas/annulerait'},
}
