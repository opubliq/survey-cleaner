# op_unknown — Unknown code in Q62AH
# Source: Q62AH
# Assumption: Variable type is categorical based on float dtype with discrete codes.
# Assumption: Code 96.0 corresponds to a single 'other' category, as no label is available.
# Note: All other values are treated as missing due to the high percentage of NaNs.
df_clean['op_unknown'] = df['Q62AH'].map({
    96.0: 'other_code',
})
CODEBOOK_VARIABLES['op_unknown'] = {
    'original_variable': 'Q62AH',
    'question_label': "Unknown question for Q62AH",
    'type': 'categorical',
    'value_labels': {'other_code': 'Other/Unspecified'},
}
