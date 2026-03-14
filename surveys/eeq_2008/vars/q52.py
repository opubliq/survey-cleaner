# op_q52 — Question 52 response
# Source: q52
# Assumption: codes 8.0 and 9.0 are treated as missing (unlabelled in provided context)
# TODO: verify mapping for codes 1.0-4.0 and the meaning of codes 8.0/9.0
df_clean['op_q52'] = df['q52'].map({
    1.0: 'option_one',
    2.0: 'option_two',
    3.0: 'option_three',
    4.0: 'option_four',
    8.0: np.nan,
    9.0: np.nan,
})
CODEBOOK_VARIABLES['op_q52'] = {
    'original_variable': 'q52',
    'question_label': "Question 52 from survey eeq_2008 (Labels pending verification)",
    'type': 'categorical',
    'value_labels': {'option_one': 'Value 1 (Unverified)', 'option_two': 'Value 2 (Unverified)', 'option_three': 'Value 3 (Unverified)', 'option_four': 'Value 4 (Unverified)'},
}