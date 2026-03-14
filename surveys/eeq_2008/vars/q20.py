# op_referendum_vote — Intention de vote au référendum
# Source: q20
df_clean['op_referendum_vote'] = df['q20'].map({
    1.0: 'oui',
    2.0: 'non',
    3.0: 'abstention',
    8.0: np.nan,
    9.0: np.nan,
})
CODEBOOK_VARIABLES['op_referendum_vote'] = {
    'original_variable': 'q20',
    'question_label': "S'il y avait un référendum aujourd'hui, voteriez-vous OUI ou NON ?",
    'type': 'categorical',
    'value_labels': {
        'oui': "OUI",
        'non': "NON",
        'abstention': "Ne voterait pas / annulerait",
    },
}
