# ses_party_preference — Political party preference
# Source: Q39
# Assumption: codes 8/9 treated as missing (unlabelled in codebook)
df_clean['ses_party_preference'] = df['Q39'].map({
    1.0: 'liberal',
    2.0: 'caq',
    8.0: np.nan,
    9.0: np.nan,
})
CODEBOOK_VARIABLES['ses_party_preference'] = {
    'original_variable': 'Q39',
    'question_label': "Si vous faisiez l'élection aujourd'hui, pour quel parti voteriez-vous?",
    'type': 'categorical',
    'value_labels': {'liberal': "Parti libéral", 'caq': "CAQ"},
}
