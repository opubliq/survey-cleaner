# op_q73e — Likely choice of party in election
# Source: Q73E
# NOTE: Codebook entry was missing. Inferred type is categorical based on float64 dtype and codes 1-4, 8, 9.
# Assumption: Codes 8.0 and 9.0 are treated as missing (unlabelled in inferred codebook).
df_clean['op_q73e'] = df['Q73E'].map({
    1.0: 'choice_one',
    2.0: 'choice_two',
    3.0: 'choice_three',
    4.0: 'choice_four',
    8.0: np.nan,
    9.0: np.nan,
})
CODEBOOK_VARIABLES['op_q73e'] = {
    'original_variable': 'Q73E',
    'question_label': "Likely choice of party in election (Inferred)",
    'type': 'categorical',
    'value_labels': {'choice_one': "Choice 1 (Inferred)", 'choice_two': "Choice 2 (Inferred)", 'choice_three': "Choice 3 (Inferred)", 'choice_four': "Choice 4 (Inferred)"},
}
