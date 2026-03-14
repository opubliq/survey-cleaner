# behav_referendum_vote_1995 — Vote intention on 1995-style sovereignty referendum
# Source: q19
# Assumption: codes 8 (don't know) and 9 (refusal) treated as missing
df_clean['behav_referendum_vote_1995'] = df['q19'].map({
    '1': 'oui',
    '2': 'non',
    '3': 'abstain',
    '8': np.nan,
    '9': np.nan,
})
CODEBOOK_VARIABLES['behav_referendum_vote_1995'] = {
    'original_variable': 'q19',
    'question_label': "Si un référendum avait lieu aujourd'hui sur la même question que celle qui a été posée lors du dernier référendum de 1995, c'est-à-dire sur la souveraineté assortie d'une offre de partenariat au reste du Canada, voteriez-vous OUI ou voteriez-vous NON ?",
    'type': 'categorical',
    'value_labels': {'oui': "Oui", 'non': "Non", 'abstain': "Ne voterait pas/annulerait"},
}
