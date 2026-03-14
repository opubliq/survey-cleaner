# ses_lang — Language spoken at home
# Source: LANG
# Assumption: All found codes are mapped. No explicit missing codes found in data preview.
df_clean['ses_lang'] = df['LANG'].map({
    'EN': 'english',
    'FR': 'french',
})
CODEBOOK_VARIABLES['ses_lang'] = {
    'original_variable': 'LANG',
    'question_label': "Language spoken at home",
    'type': 'categorical',
    'value_labels': {'english': "English", 'french': "French"},
}
