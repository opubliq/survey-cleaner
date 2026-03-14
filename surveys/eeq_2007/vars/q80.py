# op_vote_choice — Inferred vote choice from Q80
# Source: q80
# Assumption: Codebook missing. Mapping inferred from value counts. Codes other than 01/02 are treated as missing.
df_clean['op_vote_choice'] = df['q80'].map({
    '01': 'response_a',
    '02': 'response_b',
    '04': np.nan,
    '05': np.nan,
    '06': np.nan,
    '08': np.nan,
    '09': np.nan,
    '10': np.nan,
    '12': np.nan,
    '15': np.nan,
    '96': np.nan,
    '99': np.nan,
})
CODEBOOK_VARIABLES['op_vote_choice'] = {
    'original_variable': 'q80',
    'question_label': "Inferred: Vote choice (Codebook missing)",
    'type': 'categorical',
    'value_labels': {'response_a': "Response A (Code 01)", 'response_b': "Response B (Code 02)"},
}
