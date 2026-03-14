# op_q78 — Response to question 78
# Source: q78
# Assumption: codes '98' and '99' treated as missing (unlabelled in context)
df_clean['op_q78'] = df['q78'].map({
    '01': 'option_one',
    '02': 'option_two',
    '03': 'option_three',
    '04': 'option_four',
    '05': 'option_five',
    '06': 'option_six',
    '07': 'option_seven',
    '08': 'option_eight',
    '09': 'option_nine',
    '10': 'option_ten',
    '98': np.nan,
    '99': np.nan,
})
CODEBOOK_VARIABLES['op_q78'] = {
    'original_variable': 'q78',
    'question_label': "Unknown question text for Q78",
    'type': 'categorical',
    'value_labels': {'option_one': 'Value 01', 'option_two': 'Value 02', 'option_three': 'Value 03', 'option_four': 'Value 04', 'option_five': 'Value 05', 'option_six': 'Value 06', 'option_seven': 'Value 07', 'option_eight': 'Value 08', 'option_nine': 'Value 09', 'option_ten': 'Value 10'},
}