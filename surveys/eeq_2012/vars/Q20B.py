# op_attitude_q20b — Inferred attitude/opinion related to question 20B
# Source: Q20B
# Assumption: Scale 1 (most negative) to 6 (most positive). Codes 96, 98, 99 treated as missing.
df_clean['op_attitude_q20b'] = df['Q20B'].map({
    1.0: 0.0,
    2.0: 0.2,
    3.0: 0.4,
    4.0: 0.6,
    5.0: 0.8,
    6.0: 1.0,
    96.0: np.nan,
    98.0: np.nan,
    99.0: np.nan,
})
CODEBOOK_VARIABLES['op_attitude_q20b'] = {
    'original_variable': 'Q20B',
    'question_label': "Inferred attitude/opinion related to question 20B",
    'type': 'likert',
    'value_labels': {0.0: "Most Negative", 0.2: "Negative", 0.4: "Neutral/Slightly Negative", 0.6: "Neutral/Slightly Positive", 0.8: "Positive", 1.0: "Most Positive"},
}