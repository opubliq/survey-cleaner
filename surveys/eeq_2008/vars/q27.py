# op_issue_priority — Priority given to economic, health, education, or environmental issues
# Source: q27
# Assumption: codes 8, 9 are treated as missing (not explicitly labelled in codebook values)
# Note: code 5 (Autre) is expected from codebook but has no counts in the sample observed.
df_clean['op_issue_priority'] = df['q27'].map({
    1.0: 'economie',
    2.0: 'sante',
    3.0: 'education',
    4.0: 'environnement',
    5.0: 'autre',
    8.0: np.nan,
    9.0: np.nan,
    99.0: np.nan,
})
CODEBOOK_VARIABLES['op_issue_priority'] = {
    'original_variable': 'q27',
    'question_label': "Quelle est votre question à propos des enjeux?",
    'type': 'categorical',
    'value_labels': {'economie': "Économie", 'sante': "Santé", 'education': "Éducation", 'environnement': "Environnement", 'autre': "Autre"},
}