# op_q68f — Unknown categorical response code
# Source: Q68F
# WARNING: Codebook entry for Q68F in eeq_2012 was not provided. Mapping raw codes to string labels based on observation only.
df_clean['op_q68f'] = df['Q68F'].map({
    0.0: 'zero',
    1.0: 'one',
    2.0: 'two',
    3.0: 'three',
    4.0: 'four',
    5.0: 'five',
    6.0: 'six',
    9.0: 'nine',
    10.0: 'ten',
    15.0: 'fifteen',
    17.0: 'seventeen',
    20.0: 'twenty',
    25.0: 'twenty-five',
    30.0: 'thirty',
    32.0: 'thirty-two',
    33.0: 'thirty-three',
    35.0: 'thirty-five',
    40.0: 'forty',
    45.0: 'forty-five',
    46.0: 'forty-six',
    50.0: 'fifty',
    55.0: 'fifty-five',
    60.0: 'sixty',
    65.0: 'sixty-five',
    68.0: 'sixty-eight',
})
CODEBOOK_VARIABLES['op_q68f'] = {
    'original_variable': 'Q68F',
    'question_label': "Unknown: Response code for Q68F",
    'type': 'categorical',
    'value_labels': {'zero': "0", 'one': "1", 'two': "2", 'three': "3", 'four': "4", 'five': "5", 'six': "6", 'nine': "9", 'ten': "10", 'fifteen': "15", 'seventeen': "17", 'twenty': "20", 'twenty-five': "25", 'thirty': "30", 'thirty-two': "32", 'thirty-three': "33", 'thirty-five': "35", 'forty': "40", 'forty-five': "45", 'forty-six': "46", 'fifty': "50", 'fifty-five': "55", 'sixty': "60", 'sixty-five': "65", 'sixty-eight': "68"},
}