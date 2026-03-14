# op_q5_response — Voting intention (Best Effort mapping due to missing codebook)
# Source: Q5
# Note: No codebook provided. Mapped values are inferred based on observed frequency and standard conventions for election surveys.
# Assumption: Codes 96 and 99 are treated as missing.
df_clean['op_q5_response'] = df['Q5'].map({
    1.0: 'vote_party_a',
    2.0: 'vote_party_b',
    3.0: 'vote_party_c',
    4.0: 'vote_party_d',
    5.0: 'vote_other',
    6.0: 'vote_none',
    96.0: np.nan,
    99.0: np.nan,
})
CODEBOOK_VARIABLES['op_q5_response'] = {
    'original_variable': 'Q5',
    'question_label': "Q5 (Unknown Label - Best Effort)",
    'type': 'categorical',
    'value_labels': {'vote_party_a': "Party A (Inferred)", 'vote_party_b': "Party B (Inferred)", 'vote_party_c': "Party C (Inferred)", 'vote_party_d': "Party D (Inferred)", 'vote_other': "Other (Inferred)", 'vote_none': "None (Inferred)"},
}