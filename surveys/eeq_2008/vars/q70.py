# op_attitude_70 — General attitude question 70
# Source: q70
# Assumption: Codes 96, 97, 98, 99 are treated as missing/refused/not applicable based on value counts.
# Assumption: Values 1.0 to 5.0 represent distinct response categories.
df_clean['op_attitude_70'] = df['q70'].map({
    1.0: 'option_1',
    2.0: 'option_2',
    3.0: 'option_3',
    4.0: 'option_4',
    5.0: 'option_5',
    96.0: np.nan,
    97.0: np.nan,
    98.0: np.nan,
    99.0: np.nan,
})
CODEBOOK_VARIABLES['op_attitude_70'] = {
    'original_variable': 'q70',
    'question_label': "Inferred: Response to question 70",
    'type': 'categorical',
    'value_labels': {'option_1': "Option 1", 'option_2': "Option 2", 'option_3': "Option 3", 'option_4': "Option 4", 'option_5': "Option 5"},
}