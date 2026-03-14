# op_question_26b — Opinion variable Q26B - Labels unknown
# Source: Q26B
# Assumption: Codes 8.0 and 9.0 treated as missing based on common survey practice, as no codebook was available.
df_clean['op_question_26b'] = df['Q26B'].map({
    1.0: 'yes',
    2.0: 'no',
    8.0: np.nan,
    9.0: np.nan,
})
CODEBOOK_VARIABLES['op_question_26b'] = {
    'original_variable': 'Q26B',
    'question_label': "Opinion variable Q26B - Labels unknown",
    'type': 'categorical',
    'value_labels': {'yes': "Yes", 'no': "No"},
}
