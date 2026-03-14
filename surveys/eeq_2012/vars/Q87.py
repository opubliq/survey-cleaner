# ses_voting_intent — Intention de vote (Parti principal)
# Source: Q87
# Assumption: codes 8/9 treated as missing (unlabelled in codebook, often used for 'Don't know'/'Refused' in this context)
df_clean['ses_voting_intent'] = df['Q87'].map({
    1.0: 'liberal',
    2.0: 'caq',
    8.0: np.nan,
    9.0: np.nan,
})
CODEBOOK_VARIABLES['ses_voting_intent'] = {
    'original_variable': 'Q87',
    'question_label': "Votre intention de vote pour le parti principal",
    'type': 'categorical',
    'value_labels': {'liberal': "Parti libéral", 'caq': "CAQ", 'nan': "Missing/Refused"},
}