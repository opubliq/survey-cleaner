# op_q12b — Inferred opinion/behavior variable
# Source: q12b
# Note: Actual codebook missing for eeq_2008/q12b. Proceeding with data-driven mapping and generic labels.
# Assumption: Codes 97, 98, 99 treated as missing.
df_clean['op_q12b'] = df['q12b'].map({
    1.0: 'option_one',
    2.0: 'option_two',
    3.0: 'option_three',
    4.0: 'option_four',
    5.0: 'option_five',
    97.0: np.nan,
    98.0: np.nan,
    99.0: np.nan,
})
CODEBOOK_VARIABLES['op_q12b'] = {
    'original_variable': 'q12b',
    'question_label': "Inferred question label for Q12b (Verification Required)",
    'type': 'categorical',
    'value_labels': {'option_one': "Category 1", 'option_two': "Category 2", 'option_three': "Category 3", 'option_four': "Category 4", 'option_five': "Category 5"},
}