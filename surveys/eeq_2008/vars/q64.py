# op_response_q64 — Generic response for question Q64
# Source: q64
# Assumption: No codebook provided; mapping observed codes to string equivalent of the code.
df_clean['op_response_q64'] = df['q64'].map({
    0.0: '0.0',
    1.0: '1.0',
    2.0: '2.0',
    5.0: '5.0',
    6.0: '6.0',
    7.0: '7.0',
    10.0: '10.0',
    11.0: '11.0',
    12.0: '12.0',
    15.0: '15.0',
    17.0: '17.0',
    18.0: '18.0',
    20.0: '20.0',
    22.0: '22.0',
    25.0: '25.0',
    30.0: '30.0',
    33.0: '33.0',
    35.0: '35.0',
    40.0: '40.0',
    45.0: '45.0',
    49.0: '49.0',
    50.0: '50.0',
    51.0: '51.0',
    55.0: '55.0',
    60.0: '60.0',
})
CODEBOOK_VARIABLES['op_response_q64'] = {
    'original_variable': 'q64',
    'question_label': "Unknown question label (No codebook provided)",
    'type': 'categorical',
    'value_labels': {'0.0': "Code 0.0", '1.0': "Code 1.0", '2.0': "Code 2.0", '5.0': "Code 5.0", '6.0': "Code 6.0", '7.0': "Code 7.0", '10.0': "Code 10.0", '11.0': "Code 11.0", '12.0': "Code 12.0", '15.0': "Code 15.0", '17.0': "Code 17.0", '18.0': "Code 18.0", '20.0': "Code 20.0", '22.0': "Code 22.0", '25.0': "Code 25.0", '30.0': "Code 30.0", '33.0': "Code 33.0", '35.0': "Code 35.0", '40.0': "Code 40.0", '45.0': "Code 45.0", '49.0': "Code 49.0", '50.0': "Code 50.0", '51.0': "Code 51.0", '55.0': "Code 55.0", '60.0': "Code 60.0"},
}