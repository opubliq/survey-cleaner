# op_q101a — Response to question 101A
# Source: Q101A
# Assumption: Codes 8.0 and 9.0 are missing/refused (not specified in codebook).
df_clean['op_q101a'] = df['Q101A'].map({
    1.0: 'yes',
    2.0: 'no',
    8.0: np.nan,
    9.0: np.nan,
})
CODEBOOK_VARIABLES['op_q101a'] = {
    'original_variable': 'Q101A',
    'question_label': "Response to Question 101A (No codebook context)",
    'type': 'categorical',
    'value_labels': {'yes': 'Yes response', 'no': 'No response'},
}