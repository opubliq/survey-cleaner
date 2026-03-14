# op_q79 — Voting intention (Inferred from context, no label available)
# Source: Q79
# Assumption: Codes 8.0 and 9.0 are unlabelled missing values (DK/Refused) and will be mapped to NaN.
df_clean['op_q79'] = df['Q79'].map({
    1.0: 'voted_party_a',
    2.0: 'voted_party_b',
    8.0: np.nan,
    9.0: np.nan,
})
CODEBOOK_VARIABLES['op_q79'] = {
    'original_variable': 'Q79',
    'question_label': "Voting intention (Inferred - Label Missing)",
    'type': 'categorical',
    'value_labels': {'voted_party_a': "Voted for Party A (Inferred)", 'voted_party_b': "Voted for Party B (Inferred)"},
}