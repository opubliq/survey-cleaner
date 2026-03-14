# op_opinion_q46 — Opinion question 46 (labels unknown)
# Source: q46
# Assumption: Codes 98 and 99 treated as missing as per convention.
# Note: Labels for codes 1-7 are derived from common question types (e.g., Likert scale responses) due to missing codebook.
df_clean['op_opinion_q46'] = df['q46'].map({
    1.0: 'response_1',
    2.0: 'response_2',
    3.0: 'response_3',
    4.0: 'response_4',
    5.0: 'response_5',
    6.0: 'response_6',
    7.0: 'response_7',
    98.0: np.nan,
    99.0: np.nan,
})
CODEBOOK_VARIABLES['op_opinion_q46'] = {
    'original_variable': 'q46',
    'question_label': "Opinion question 46 (labels unknown)",
    'type': 'categorical',
    'value_labels': {'response_1': "Response 1", 'response_2': "Response 2", 'response_3': "Response 3", 'response_4': "Response 4", 'response_5': "Response 5", 'response_6': "Response 6", 'response_7': "Response 7"},
}