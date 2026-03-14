# ses_language — Language of response/interview
# Source: langu
# Assumption: Inferred mapping based on variable name 'langu' and common conventions.
df_clean['ses_language'] = df['langu'].map({
    1.0: 'french',
    2.0: 'english',
    3.0: 'other',
})
CODEBOOK_VARIABLES['ses_language'] = {
    'original_variable': 'langu',
    'question_label': "Language of response/interview",
    'type': 'categorical',
    'value_labels': {'french': "French", 'english': "English", 'other': "Other"},
}