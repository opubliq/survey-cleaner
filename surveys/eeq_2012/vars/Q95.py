# behav_vote_party — Parti voté pour qui vous avez voté
# Source: Q95
# Assumption: codes 8 and 9 are explicitly mapped as they appear in data counts. Code 99 from codebook is mapped to NaN.
df_clean['behav_vote_party'] = df['Q95'].map({
    1.0: 'parti libéral',
    2.0: 'parti conservateur',
    3.0: 'parti québécois',
    4.0: 'option nationale',
    5.0: 'caq',
    6.0: 'autres partis',
    7.0: 'ne s\'applique pas',
    8.0: 'n\'ai pas voté',
    9.0: 'ne me souviens pas',
    99.0: np.nan,
})
CODEBOOK_VARIABLES['behav_vote_party'] = {
    'original_variable': 'Q95',
    'question_label': "Parti voté pour qui vous avez voté",
    'type': 'categorical',
    'value_labels': {'parti libéral': "Parti libéral", 'parti conservateur': "Parti conservateur", 'parti québécois': "Parti québécois", 'option nationale': "Option nationale", 'caq': "CAQ", 'autres partis': "Autres partis", 'ne s\'applique pas': "Ne s'applique pas", 'n\'ai pas voté': "Je n'ai pas voté", 'ne me souviens pas': "Je ne me souviens pas"},
}