# op_opinion — General opinion on the election
# Source: q47
# Assumption: Codes 8 and 9 are treated as missing (not explicitly defined in codebook context)
df_clean['op_opinion'] = df['q47'].map({
    1.0: 'positive',
    2.0: 'neutral',
    3.0: 'negative',
    8.0: np.nan,
    9.0: np.nan,
})
CODEBOOK_VARIABLES['op_opinion'] = {
    'original_variable': 'q47',
    'question_label': "General opinion on the election (Inferred)",
    'type': 'categorical',
    'value_labels': {'positive': "Positive", 'neutral': "Neutral", 'negative': "Negative"},
}