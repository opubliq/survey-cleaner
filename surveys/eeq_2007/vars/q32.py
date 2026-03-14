# behav_q32 — Unknown category, mapped from numeric codes
# Source: q32
# Assumption: Variable is categorical based on float type and discrete values. Mapping float codes directly to strings due to missing codebook entry.
df_clean['behav_q32'] = df['q32'].map({
    0.0: '0.0',
    1.0: '1.0',
    2.0: '2.0',
    3.0: '3.0',
    4.0: '4.0',
    5.0: '5.0',
    6.0: '6.0',
    7.0: '7.0',
    8.0: '8.0',
    9.0: '9.0',
    10.0: '10.0',
    12.0: '12.0',
    15.0: '15.0',
    20.0: '20.0',
    22.0: '22.0',
    25.0: '25.0',
    30.0: '30.0',
    35.0: '35.0',
    40.0: '40.0',
    45.0: '45.0',
    50.0: '50.0',
    52.0: '52.0',
    55.0: '55.0',
    60.0: '60.0',
    65.0: '65.0',
})
CODEBOOK_VARIABLES['behav_q32'] = {
    'original_variable': 'q32',
    'question_label': "Unknown question text for q32",
    'type': 'categorical',
    'value_labels': {'0.0': "Code 0.0", '1.0': "Code 1.0", '2.0': "Code 2.0", '3.0': "Code 3.0", '4.0': "Code 4.0", '5.0': "Code 5.0", '6.0': "Code 6.0", '7.0': "Code 7.0", '8.0': "Code 8.0", '9.0': "Code 9.0", '10.0': "Code 10.0", '12.0': "Code 12.0", '15.0': "Code 15.0", '20.0': "Code 20.0", '22.0': "Code 22.0", '25.0': "Code 25.0", '30.0': "Code 30.0", '35.0': "Code 35.0", '40.0': "Code 40.0", '45.0': "Code 45.0", '50.0': "Code 50.0", '52.0': "Code 52.0", '55.0': "Code 55.0", '60.0': "Code 60.0", '65.0': "Code 65.0"},
}