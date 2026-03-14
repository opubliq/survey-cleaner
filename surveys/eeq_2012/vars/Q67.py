# op_q67 — Unknown categorical question
# Source: Q67
# Assumption: Codes 8.0 and 9.0 are unlabelled and treated as missing (np.nan). Labels for 1.0-4.0 are placeholders due to missing codebook entry.
df_clean['op_q67'] = df['Q67'].map({
    1.0: 'option_one',
    2.0: 'option_two',
    3.0: 'option_three',
    4.0: 'option_four',
    8.0: np.nan,
    9.0: np.nan,
})
CODEBOOK_VARIABLES['op_q67'] = {
    'original_variable': 'Q67',
    'question_label': "Unknown question (Q67 from eeq_2012)",
    'type': 'categorical',
    'value_labels': {'option_one': "Option One (Placeholder)", 'option_two': "Option Two (Placeholder)", 'option_three': "Option Three (Placeholder)", 'option_four': "Option Four (Placeholder)"},
}