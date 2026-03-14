# op_vote_conservative — Intention de voter pour le Parti Conservateur
# Source: Q34C
# Assumption: Codes 3, 4, 8, 9 treated as missing as the variable is labeled binary.
df_clean['op_vote_conservative'] = df['Q34C'].map({
    1.0: 1.0,
    2.0: 0.0,
    3.0: np.nan,
    4.0: np.nan,
    8.0: np.nan,
    9.0: np.nan,
})
CODEBOOK_VARIABLES['op_vote_conservative'] = {
    'original_variable': 'Q34C',
    'question_label': "Avez-vous l'intention de voter pour le Parti Conservateur?",
    'type': 'binary',
    'value_labels': {'1.0': "Oui", '0.0': "Non"},
}