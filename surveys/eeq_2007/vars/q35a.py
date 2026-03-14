# op_q35a — Response to question 35a (Deducted from data exploration)
# Source: q35a
# Assumption: Codes '8' and '9' are unlabelled and treated as missing.
df_clean['op_q35a'] = df['q35a'].map({
    '1': 'option_one',
    '2': 'option_two',
    '3': 'option_three',
    '4': 'option_four',
    '8': np.nan,
    '9': np.nan,
})
CODEBOOK_VARIABLES['op_q35a'] = {
    'original_variable': 'q35a',
    'question_label': "Response to question 35a (Deducted from data exploration, values 1-4 present)",
    'type': 'categorical',
    'value_labels': {'option_one': 'Option 1', 'option_two': 'Option 2', 'option_three': 'Option 3', 'option_four': 'Option 4'},
}