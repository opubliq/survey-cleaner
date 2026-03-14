# behav_voted — Electoral participation (voted in provincial election)
# Source: q11
df_clean['behav_voted'] = df['q11'].map({
    '1': 1.0,
    '2': 0.0,
    '8': np.nan,
    '9': np.nan,
})
CODEBOOK_VARIABLES['behav_voted'] = {
    'original_variable': 'q11',
    'question_label': "Avez-vous voté à cette élection provinciale ?",
    'type': 'binary',
    'value_labels': {'0.0': 'No', '1.0': 'Yes'},
}
