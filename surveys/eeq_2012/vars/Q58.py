# op_q58 — Unknown opinion/behavior question 58
# Source: Q58
# Assumption: Codes 8 and 9 are treated as missing ('Don't Know'/'Refused') as they are not standard response codes.
df_clean['op_q58'] = df['Q58'].map({
    1.0: 'intent_option_1',
    2.0: 'intent_option_2',
    8.0: np.nan,
    9.0: np.nan,
})
CODEBOOK_VARIABLES['op_q58'] = {
    'original_variable': 'Q58',
    'question_label': "Q58 (Label missing, inferred as opinion)",
    'type': 'categorical',
    'value_labels': {'intent_option_1': "Option 1", 'intent_option_2': "Option 2"},
}
