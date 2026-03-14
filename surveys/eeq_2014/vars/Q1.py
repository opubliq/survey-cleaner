# op_vote_intent — Intention de vote
# Source: Q1
# Note: Variable type is numeric (float64) but represents categorical survey data, mapped to 0-1 scale for vote intent.
df_clean['op_vote_intent'] = df['Q1'].map({
    1.0: 0.0,  # Parti libéral du Québec (PLQ)
    2.0: 0.1,  # Coalition Avenir Québec (CAQ)
    3.0: 0.2,  # Parti Québécois (PQ)
    4.0: 0.3,  # Québec solidaire (QS)
    5.0: 0.4,  # Parti Conservateur du Québec (PCQ)
    6.0: 0.5,  # Parti Vert (PV)
    7.0: 0.6,  # Autre parti
    8.0: 0.7,  # Ne votera pas (Refus de voter) - Treating as distinct option
    9.0: 0.8,  # Ne votera pas (Ne sait pas/Ne répond pas) - Treating as distinct option
    10.0: 0.9, # Ne sait pas / Ne répond pas
    98.0: np.nan, # Autre (Refusé/Non-réponse) - Map to missing
    99.0: np.nan, # Non-réponse (Refusé/Non-réponse) - Map to missing
})
CODEBOOK_VARIABLES['op_vote_intent'] = {
    'original_variable': 'Q1',
    'question_label': "À quel parti politique avez-vous l'intention de voter aux prochaines élections provinciales?",
    'type': 'categorical',
    'value_labels': {'0.0': "PLQ", '0.1': "CAQ", '0.2': "PQ", '0.3': "QS", '0.4': "PCQ", '0.5': "PV", '0.6': "Autre parti", '0.7': "Ne votera pas (Refus de voter)", '0.8': "Ne votera pas (Ne sait pas/Ne répond pas)", '0.9': "Ne sait pas / Ne répond pas"},
}