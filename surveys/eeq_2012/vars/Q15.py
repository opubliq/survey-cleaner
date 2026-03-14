# op_vote_intent — Inferred vote intention/opinion scale
# Source: Q15
# Assumption: 6-point scale where 1=0.0 and 6=1.0. Codes 96, 98, 99 treated as missing.
df_clean['op_vote_intent'] = df['Q15'].map({
    1.0: 0.0,
    2.0: 0.2,
    3.0: 0.4,
    4.0: 0.6,
    5.0: 0.8,
    6.0: 1.0,
})
CODEBOOK_VARIABLES['op_vote_intent'] = {
    'original_variable': 'Q15',
    'question_label': "Inferred Vote Intention/Opinion Scale",
    'type': 'likert',
    'value_labels': {0.0: "Lowest Score (1)", 0.2: "Score 2", 0.4: "Score 3", 0.6: "Score 4", 0.8: "Score 5", 1.0: "Highest Score (6)"},
}