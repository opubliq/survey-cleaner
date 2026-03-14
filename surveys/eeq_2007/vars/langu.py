# ses_language — Primary language spoken
# Source: langu
# Assumption: Codes 4-9 are treated as unmapped/missing due to low frequency and lack of codebook.
df_clean['ses_language'] = df['langu'].map({
    '1': 'french',
    '2': 'english',
    '3': 'other',
    '4': np.nan,
    '5': np.nan,
    '6': np.nan,
    '7': np.nan,
    '9': np.nan,
})
CODEBOOK_VARIABLES['ses_language'] = {
    'original_variable': 'langu',
    'question_label': "Primary language spoken",
    'type': 'categorical',
    'value_labels': {'french': "French", 'english': "English", 'other': "Other"},
}