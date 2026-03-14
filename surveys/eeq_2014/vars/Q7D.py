# op_response — Response to question 7D (inferred)
# Source: Q7D
# Assumption: Codes 1-4 map to inferred categorical answers. Codes 8.0, 9.0, and NaN are missing.
df_clean['op_response'] = df['Q7D'].map({
    1.0: 'yes',
    2.0: 'no',
    3.0: "don't know",
    4.0: 'refused',
    8.0: np.nan,
    9.0: np.nan,
})
CODEBOOK_VARIABLES['op_response'] = {
    'original_variable': 'Q7D',
    'question_label': "Response to Q7D (label not provided, inferred)",
    'type': 'categorical',
    'value_labels': {'yes': "Yes", 'no': "No", "don't know": "Don't Know", 'refused': "Refused"},
}