# know_q57 — Unknown question/score, assuming 5-point scale
# Source: q57
# Assumption: Codes 01-05 mapped to placeholder levels, 96-99 treated as missing (unlabelled in codebook)
df_clean['know_q57'] = df['q57'].map({
    '01': 'level_one',
    '02': 'level_two',
    '03': 'level_three',
    '04': 'level_four',
    '05': 'level_five',
    '96': np.nan,
    '97': np.nan,
    '98': np.nan,
    '99': np.nan,
})
CODEBOOK_VARIABLES['know_q57'] = {
    'original_variable': 'q57',
    'question_label': "Unknown question content for q57",
    'type': 'categorical',
    'value_labels': {'level_one': "Level One", 'level_two': "Level Two", 'level_three': "Level Three", 'level_four': "Level Four", 'level_five': "Level Five"},
}