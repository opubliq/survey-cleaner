# op_q44a — Generic survey question Q44A
# Source: Q44A
# Note: No codebook provided. Mapping generic codes 1-4 to labels 'a' through 'd'.
# Assumption: codes 8.0 and 9.0 are treated as missing based on common survey practices.
df_clean['op_q44a'] = df['Q44A'].map({
    1.0: 'a',
    2.0: 'b',
    3.0: 'c',
    4.0: 'd',
    8.0: np.nan,
    9.0: np.nan,
})
CODEBOOK_VARIABLES['op_q44a'] = {
    'original_variable': 'Q44A',
    'question_label': "Question Q44A from eeq_2014 (Label Unknown)",
    'type': 'categorical',
    'value_labels': {'a': "Value A (Unknown)", 'b': "Value B (Unknown)", 'c': "Value C (Unknown)", 'd': "Value D (Unknown)"},
}