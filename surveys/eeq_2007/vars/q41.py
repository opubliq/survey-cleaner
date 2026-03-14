# know_q41 — Q41 (Inferred: Unknown question label)
# Source: q41
# Assumption: Codes observed in data are mapped to their string literal. All unmapped codes (including 11, 16, 18, 19, 21, 23, 27-29, 31-32, etc.) will result in np.nan.
# Assumption: Code 99.0 is treated as missing.
df_clean['know_q41'] = df['q41'].map({
    0.0: 'zero',
    1.0: 'one',
    2.0: 'two',
    3.0: 'three',
    4.0: 'four',
    5.0: 'five',
    6.0: 'six',
    7.0: 'seven',
    8.0: 'eight',
    9.0: 'nine',
    10.0: 'ten',
    12.0: 'twelve',
    13.0: 'thirteen',
    14.0: 'fourteen',
    15.0: 'fifteen',
    17.0: 'seventeen',
    20.0: 'twenty',
    22.0: 'twenty-two',
    24.0: 'twenty-four',
    25.0: 'twenty-five',
    26.0: 'twenty-six',
    30.0: 'thirty',
    33.0: 'thirty-three',
    34.0: 'thirty-four',
    35.0: 'thirty-five',
    99.0: np.nan,
})
CODEBOOK_VARIABLES['know_q41'] = {
    'original_variable': 'q41',
    'question_label': "Q41 (Inferred: Unknown question label)",
    'type': 'categorical',
    'value_labels': {'zero': "0.0", 'one': "1.0", 'two': "2.0", 'three': "3.0", 'four': "4.0", 'five': "5.0", 'six': "6.0", 'seven': "7.0", 'eight': "8.0", 'nine': "9.0", 'ten': "10.0", 'twelve': "12.0", 'thirteen': "13.0", 'fourteen': "14.0", 'fifteen': "15.0", 'seventeen': "17.0", 'twenty': "20.0", 'twenty-two': "22.0", 'twenty-four': "24.0", 'twenty-five': "25.0", 'twenty-six': "26.0", 'thirty': "30.0", 'thirty-three': "33.0", 'thirty-four': "34.0", 'thirty-five': "35.0"},
}