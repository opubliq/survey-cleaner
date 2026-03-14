# behav_q33a — Response to Question 33A
# Source: Q33A
# Assumption: Codes 8 and 9 treated as missing (unlabelled in data exploration)
# Assumption: Codes 1-4 mapped to Yes/No/DK/Refused as common practice for response questions
df_clean['behav_q33a'] = df['Q33A'].map({
    1.0: 'yes',
    2.0: 'no',
    3.0: 'dk',
    4.0: 'refused',
    8.0: np.nan,
    9.0: np.nan,
})
CODEBOOK_VARIABLES['behav_q33a'] = {
    'original_variable': 'Q33A',
    'question_label': "Response to Question 33A",
    'type': 'categorical',
    'value_labels': {'yes': "Yes", 'no': "No", 'dk': "Don't know", 'refused': "Refused"},
}