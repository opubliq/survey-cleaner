# op_response_b — Response B for Question 44 (Inferred from pattern)
# Source: Q44B
# Assumption: Codes 1-4 mapped to generic labels a-d. Codes 8/9 mapped to DK/Refused.
df_clean['op_response_b'] = df['Q44B'].map({
    1.0: 'a',
    2.0: 'b',
    3.0: 'c',
    4.0: 'd',
    8.0: 'dk',
    9.0: 'refused',
})
CODEBOOK_VARIABLES['op_response_b'] = {
    'original_variable': 'Q44B',
    'question_label': "Response B for Question 44 (Labels Inferred)",
    'type': 'categorical',
    'value_labels': {'a': "Label 1 (Inferred)", 'b': "Label 2 (Inferred)", 'c': "Label 3 (Inferred)", 'd': "Label 4 (Inferred)", 'dk': "Don't Know", 'refused': "Refused"},
}