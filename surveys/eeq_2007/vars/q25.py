# op_government_honesty — Perception of government leaders' honesty
# Source: q25
# Question: "Pensen-vous que...? / LIRE LES 3 CHOIX"
# 1 = many are dishonest (low trust), 2 = some are dishonest, 3 = almost none are dishonest (high trust)
# 8/9 treated as missing (don't know / refused)
df_clean['op_government_honesty'] = df['q25'].map({
    '1': 'many_dishonest',
    '2': 'some_dishonest',
    '3': 'almost_none_dishonest',
    '8': np.nan,
    '9': np.nan,
})
CODEBOOK_VARIABLES['op_government_honesty'] = {
    'original_variable': 'q25',
    'question_label': "Pensen-vous que...? / LIRE LES 3 CHOIX",
    'type': 'categorical',
    'value_labels': {'many_dishonest': "Plusieurs dirigeants gouvernementaux sont malhonnêtes", 'some_dishonest': "Certains d'entre eux sont malhonnêtes", 'almost_none_dishonest': "Presqu'aucun d'entre eux n'est malhonnête"},
}
