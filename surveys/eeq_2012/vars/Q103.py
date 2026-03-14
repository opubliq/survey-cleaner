# op_q103 — Opinion/Attitude question 103
# Source: Q103
# Assumption: Variable is categorical, mapping codes 1-6 and 9 based on general scale conventions as labels were not provided.
# TODO: verify mapping for codes 1.0-9.0 and replace assumed labels with actual labels from codebook.
df_clean['op_q103'] = df['Q103'].map({
    1.0: 'very_negative',
    2.0: 'negative',
    3.0: 'somewhat_negative',
    4.0: 'somewhat_positive',
    5.0: 'positive',
    6.0: 'very_positive',
    9.0: 'dont_know',
    # All other values (including NaN from data) will map to np.nan automatically
})
CODEBOOK_VARIABLES['op_q103'] = {
    'original_variable': 'Q103',
    'question_label': "Q103 (Label missing, using generic placeholder)",
    'type': 'categorical',
    'value_labels': {'very_negative': "Very Negative", 'negative': "Negative", 'somewhat_negative': "Somewhat Negative", 'somewhat_positive': "Somewhat Positive", 'positive': "Positive", 'very_positive': "Very Positive", 'dont_know': "Don't Know"},
}