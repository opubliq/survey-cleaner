# op_interest_politics — Interest in politics in general (0-10 scale normalized to 0-1)
# Source: q15
# Assumption: codes 98.0 and 99.0 treated as missing (documented as don't know / refusal)
df_clean['op_interest_politics'] = df['q15'].map({
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
CODEBOOK_VARIABLES['op_interest_politics'] = {
    'original_variable': 'q15',
    'question_label': "Et toujours avec la même échelle, quel est votre intérêt pour la politique en général? (Sur une échelle de 0 à 10 où 0 veut dire aucun intérêt et 10 veut dire beaucoup d'intérêt)",
    'type': 'likert',
    'value_labels': {
        0.0: 'no interest',
        0.1: 'minimal interest',
        0.2: 'very low interest',
        0.3: 'low interest',
        0.4: 'below average interest',
        0.5: 'moderate interest',
        0.6: 'above average interest',
        0.7: 'high interest',
        0.8: 'very high interest',
        0.9: 'very strong interest',
        1.0: 'maximum interest',
    },
}
