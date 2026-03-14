# op_vote_detail — Detailed vote choice/preference
# Source: Q77D
# Assumption: Codes 8/9 are missing (unlabelled in data exploration, inferred from context)
df_clean['op_vote_detail'] = df['Q77D'].map({
    1.0: 'option_one',
    2.0: 'option_two',
    3.0: 'option_three',
    4.0: 'option_four',
    8.0: np.nan,
    9.0: np.nan,
})
CODEBOOK_VARIABLES['op_vote_detail'] = {
    'original_variable': 'Q77D',
    'question_label': "Detailed vote choice/preference (Inferred from data structure)",
    'type': 'categorical',
    'value_labels': {'option_one': "Option 1", 'option_two': "Option 2", 'option_three': "Option 3", 'option_four': "Option 4"},
}
