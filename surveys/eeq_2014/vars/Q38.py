# ses_q38_response — Response to Q38 (inferred categorical)
# Source: Q38
# Assumption: Codes 8.0 and 9.0 treated as valid responses ('dont_know', 'refused') as no missing codes were provided.
df_clean['ses_q38_response'] = df['Q38'].map({
    1.0: 'response_1',
    2.0: 'response_2',
    8.0: 'dont_know',
    9.0: 'refused',
})
CODEBOOK_VARIABLES['ses_q38_response'] = {
    'original_variable': 'Q38',
    'question_label': "Response to Q38 (Label unknown, inferred from data exploration)",
    'type': 'categorical',
    'value_labels': {'response_1': "Response 1", 'response_2': "Response 2", 'dont_know': "Don't Know", 'refused': "Refused"},
}