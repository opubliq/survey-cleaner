# op_opinion_d — Inferred opinion/attitude question D
# Source: Q73D
# Note: Codebook entry was missing. Inferred type is categorical.
# Assumption: Codes 8.0 and 9.0 are missing values (Refused/NA).
df_clean['op_opinion_d'] = df['Q73D'].map({
    1.0: 'option_1',
    2.0: 'option_2',
    3.0: 'option_3',
    4.0: 'option_4',
    8.0: np.nan,
    9.0: np.nan,
})
CODEBOOK_VARIABLES['op_opinion_d'] = {
    'original_variable': 'Q73D',
    'question_label': "Inferred Opinion Variable Q73D (Codebook Missing)",
    'type': 'categorical',
    'value_labels': {'option_1': "Option 1", 'option_2': "Option 2", 'option_3': "Option 3", 'option_4': "Option 4"},
}