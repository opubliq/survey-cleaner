# know_election_interest — Interest in provincial election on 0-10 scale
# Source: q14
# Assumption: codes 0-10 are valid scale values; 98/99 treated as missing (not interest codes)
df_clean['know_election_interest'] = df['q14'].map({
    0.0: 0.0,
    1.0: 0.1,
    2.0: 0.2,
    3.0: 0.3,
    4.0: 0.4,
    5.0: 0.5,
    6.0: 0.6,
    7.0: 0.7,
    8.0: 0.8,
    9.0: 0.9,
    10.0: 1.0,
    98.0: np.nan,
    99.0: np.nan,
})
CODEBOOK_VARIABLES['know_election_interest'] = {
    'original_variable': 'q14',
    'question_label': "Sur une échelle de 0 à 10 où 0 veut dire aucun intérêt et 10 veut dire beaucoup d'intérêt, quel a été votre intérêt pour l'élection PROVINCIALE qui vient d'avoir lieu ?",
    'type': 'likert',
    'value_labels': {'0.0': 'aucun intérêt', '0.5': 'intérêt moyen', '1.0': 'beaucoup d\'intérêt'},
}
