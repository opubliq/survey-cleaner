# op_q24 — Response to question 24 (Inferred from data exploration)
# Source: Q24
# NOTE: Codebook entry was missing. Mapping, type ('categorical'), and value labels are inferred from data exploration (codes 1, 2, 3 present). Codes 8, 9 treated as missing.
df_clean['op_q24'] = df['Q24'].map({
    1.0: 'choice_one',
    2.0: 'choice_two',
    3.0: 'choice_three',
    8.0: np.nan,
    9.0: np.nan,
})
CODEBOOK_VARIABLES['op_q24'] = {
    'original_variable': 'Q24',
    'question_label': "Response to question 24 (Placeholder due to missing codebook)",
    'type': 'categorical',
    'value_labels': {'choice_one': "Choice One (inferred)", 'choice_two': "Choice Two (inferred)", 'choice_three': "Choice Three (inferred)"},
}