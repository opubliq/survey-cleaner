# ses_language — Language spoken
# Source: LANGU
# Assumption: Codes 1, 2, 3 mapped to French, English, Other based on common survey language variables (no codebook provided).
df_clean['ses_language'] = df['LANGU'].map({
    1.0: 'french',
    2.0: 'english',
    3.0: 'other',
})
CODEBOOK_VARIABLES['ses_language'] = {
    'original_variable': 'LANGU',
    'question_label': "Language spoken (Assumed mapping)",
    'type': 'categorical',
    'value_labels': {'french': "French", 'english': "English", 'other': "Other"},
}