# op_q61c — Opinion variable q61c (Mapping inferred due to missing codebook)
# Source: q61c
# Assumption: Codes 01-05 map to generic levels 1-5.
# Assumption: Codes 96-99 are missing values and will be mapped to np.nan.
df_clean['op_q61c'] = df['q61c'].map({
    '01': 'level_1',
    '02': 'level_2',
    '03': 'level_3',
    '04': 'level_4',
    '05': 'level_5',
    '96': np.nan,
    '97': np.nan,
    '98': np.nan,
    '99': np.nan,
})
CODEBOOK_VARIABLES['op_q61c'] = {
    'original_variable': 'q61c',
    'question_label': "Q61c - Question label missing (inferred as categorical)",
    'type': 'categorical',
    'value_labels': {'level_1': "Value 01 (Label Missing)", 'level_2': "Value 02 (Label Missing)", 'level_3': "Value 03 (Label Missing)", 'level_4': "Value 04 (Label Missing)", 'level_5': "Value 05 (Label Missing)"},
}