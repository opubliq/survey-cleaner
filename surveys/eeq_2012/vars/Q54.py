# know_media_presse_freq — Frequency of reading the newspaper (La Presse)
# Source: Q54
# Assumption: data type in file uses float keys for codes, missing code 99 is mapped to np.nan
df_clean['know_media_presse_freq'] = df['Q54'].map({
    1.0: 'every_day',
    2.0: 'once_a_week',
    3.0: 'less_than_weekly',
    4.0: 'never',
    99.0: np.nan,
})
CODEBOOK_VARIABLES['know_media_presse_freq'] = {
    'original_variable': 'Q54',
    'question_label': "Frequency of reading the newspaper (La Presse)",
    'type': 'categorical',
    'value_labels': {'every_day': "Every day or almost every day", 'once_a_week': "Once a week or more", 'less_than_weekly': "Less than once a week", 'never': "Never"},
}