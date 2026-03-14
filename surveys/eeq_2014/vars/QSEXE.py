# ses_sex — Sexe de l'électeur
# Source: QSEXE
# Assumption: code 99 treated as missing (unlabelled in provided data sample)
df_clean['ses_sex'] = df['QSEXE'].map({
    1.0: 'homme',
    2.0: 'femme',
    99.0: np.nan,
})
CODEBOOK_VARIABLES['ses_sex'] = {
    'original_variable': 'QSEXE',
    'question_label': "Sexe de l'électeur",
    'type': 'categorical',
    'value_labels': {'homme': "Homme", 'femme': "Femme"},
}