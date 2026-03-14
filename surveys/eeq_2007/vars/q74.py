# op_response_q74 — Response to question 74
# Source: q74
# Assumption: Codes 96, 98, 99 treated as missing (not labelled in data exploration)
df_clean['op_response_q74'] = df['q74'].map({
    '01': 'response one',
    '02': 'response two',
    '03': 'response three',
    '04': 'response four',
    '05': 'response five',
    '06': 'response six',
    '07': 'response seven',
    '96': np.nan,
    '98': np.nan,
    '99': np.nan,
})
CODEBOOK_VARIABLES['op_response_q74'] = {
    'original_variable': 'q74',
    'question_label': "Response to question 74",
    'type': 'categorical',
    'value_labels': {'response one': "Response 1", 'response two': "Response 2", 'response three': "Response 3", 'response four': "Response 4", 'response five': "Response 5", 'response six': "Response 6", 'response seven': "Response 7"},
}
