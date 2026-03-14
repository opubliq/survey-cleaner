# op_q63_2012 — Response to Question 63
# Source: Q63
# Assumption: Codes 8.0 and 9.0 treated as missing (unlabelled in codebook)
df_clean['op_q63_2012'] = df['Q63'].map({
    1.0: 'option_one',
    2.0: 'option_two',
    8.0: np.nan,
    9.0: np.nan,
})
CODEBOOK_VARIABLES['op_q63_2012'] = {
    'original_variable': 'Q63',
    'question_label': "Response to Q63",
    'type': 'categorical',
    'value_labels': {'option_one': "Option 1", 'option_two': "Option 2"},
}