# behav_party_vote_actual — Vote réel pour le chef de parti
# Source: Q7A
# Assumption: Codes 8/9 treated as missing (unlabelled in codebook)
# Note: Variable type is float due to missing values in SPSS file, mapping to float keys.
df_clean['behav_party_vote_actual'] = df['Q7A'].map({
    1.0: 'caq',
    2.0: 'plq',
    3.0: 'pqc',
    4.0: 'pdl',
    8.0: np.nan,
    9.0: np.nan,
})
CODEBOOK_VARIABLES['behav_party_vote_actual'] = {
    'original_variable': 'Q7A',
    'question_label': "Vote réel pour le chef de parti",
    'type': 'categorical',
    'value_labels': {'caq': "Coalition Avenir Québec", 'plq': "Parti libéral du Québec", 'pqc': "Parti québécois", 'pdl': "Parti démocratique du Québec"},
}