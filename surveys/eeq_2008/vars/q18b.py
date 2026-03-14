# op_voting_interest — Interest in voting (inferred from q18b structure)
# Source: q18b
# Assumption: Codes 1-5 map to a 0.0-1.0 scale (Likert). Codes 96, 98, 99 treated as missing.
df_clean['op_voting_interest'] = df['q18b'].map({
    1.0: 0.0,
    2.0: 0.25,
    3.0: 0.5,
    4.0: 0.75,
    5.0: 1.0,
    96.0: np.nan,
    98.0: np.nan,
    99.0: np.nan,
})
CODEBOOK_VARIABLES['op_voting_interest'] = {
    'original_variable': 'q18b',
    'question_label': "Interest in voting (inferred from q18b structure)",
    'type': 'likert',
    'value_labels': {'0.0': "Low Interest", '1.0': "High Interest"},
}