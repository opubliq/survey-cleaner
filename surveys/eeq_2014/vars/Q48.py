# ses_q48 — Question 48 response
# Source: Q48
# Assumption: Codes 8.0 and 9.0 are unlabelled and treated as missing (np.nan).
df_clean['ses_q48'] = df['Q48'].map({
    1.0: 'valid_response_1',
    2.0: 'valid_response_2',
    8.0: np.nan,
    9.0: np.nan,
})
CODEBOOK_VARIABLES['ses_q48'] = {
    'original_variable': 'Q48',
    'question_label': "Question 48 response",
    'type': 'categorical',
    'value_labels': {'valid_response_1': "Category 1", 'valid_response_2': "Category 2"},
}