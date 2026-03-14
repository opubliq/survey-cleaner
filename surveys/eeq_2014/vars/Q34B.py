# op_vote_intention_b — Assumed secondary vote intention question
# Source: Q34B
# NOTE: Codebook missing. Codes 8.0 and 9.0 assumed to be missing/refused based on frequency.
# Labels are placeholders.
df_clean['op_vote_intention_b'] = df['Q34B'].map({
    1.0: 'prefer_a',
    2.0: 'prefer_b',
    3.0: 'prefer_c',
    4.0: 'undecided',
    8.0: np.nan,
    9.0: np.nan,
})
CODEBOOK_VARIABLES['op_vote_intention_b'] = {
    'original_variable': 'Q34B',
    'question_label': "Assumed secondary vote intention (labels unknown)",
    'type': 'categorical',
    'value_labels': {'prefer_a': "Prefer Party A (Placeholder)", 'prefer_b': "Prefer Party B (Placeholder)", 'prefer_c': "Prefer Party C (Placeholder)", 'undecided': "Undecided (Placeholder)"},
}