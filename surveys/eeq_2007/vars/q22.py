import numpy as np

# q22 — Opinion sur le gouvernement libéral de M. Charest (1-5)
# Source: q22
df_clean['q22'] = df['q22'].map({
    '1': 'opt_1',
    '2': 'opt_2',
    '3': 'opt_3',
    '4': 'opt_4',
    '5': 'opt_5',
    '8': np.nan,
    '9': np.nan,
})
CODEBOOK_VARIABLES['q22'] = {
    'original_variable': 'q22',
    'question_label': "Opinion sur le gouvernement libéral de M. Charest (1-5)",
    'type': 'likert',
    'value_labels': {'opt_1': "Très bonne performance", 'opt_2': "Bonne performance", 'opt_3': "Performance moyenne", 'opt_4': "Mauvaise performance", 'opt_5': "Très mauvaise performance"},
    'missing_codes': [8, 9]
}