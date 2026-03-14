# op_political_choice — Political choice (inferred from values 1-4)
# Source: Q82C
# Assumption: Codes 1-4 are distinct choices. Codes 8/9 are treated as missing as per standard practice when details are unavailable.
df_clean['op_political_choice'] = df['Q82C'].map({
    1.0: 'choice_1',
    2.0: 'choice_2',
    3.0: 'choice_3',
    4.0: 'choice_4',
    8.0: np.nan, # Assumption: Don't Know
    9.0: np.nan, # Assumption: Refused
})
CODEBOOK_VARIABLES['op_political_choice'] = {
    'original_variable': 'Q82C',
    'question_label': "Choice for Q82C (Labels inferred due to missing codebook)",
    'type': 'categorical',
    'value_labels': {'choice_1': "Choice 1", 'choice_2': "Choice 2", 'choice_3': "Choice 3", 'choice_4': "Choice 4"},
}
