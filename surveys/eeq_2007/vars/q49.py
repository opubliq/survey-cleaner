# op_q49 — Response to question 49 (assumed categorical)
# Source: q49
# Assumption: Codes 8 and 9 are unlabelled missing values based on data exploration.
# Assumption: Codes 1, 2, 3 map to standard agreement scale for this placeholder.
df_clean['op_q49'] = df['q49'].map({
    1.0: 'yes',
    2.0: 'no',
    3.0: "don't know",
    8.0: np.nan,
    9.0: np.nan,
})
CODEBOOK_VARIABLES['op_q49'] = {
    'original_variable': 'q49',
    'question_label': "Response to Question 49 (Placeholder as codebook was missing)",
    'type': 'categorical',
    'value_labels': {'yes': "Yes", 'no': "No", "don't know": "Don't Know"},
}
