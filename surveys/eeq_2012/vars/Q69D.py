# op_attitude_q69d — Attitude/Opinion Q69D (Codebook missing)
# Source: Q69D
# Assumption: Codes 95, 97, 98, 99 are treated as missing based on value distribution (>=95)
df_clean['op_attitude_q69d'] = df['Q69D'].map({
    1.0: 'strongly_disagree',
    2.0: 'disagree',
    3.0: 'neutral',
    4.0: 'agree',
    5.0: 'strongly_agree',
    95.0: np.nan,
    97.0: np.nan,
    98.0: np.nan,
    99.0: np.nan,
})
CODEBOOK_VARIABLES['op_attitude_q69d'] = {
    'original_variable': 'Q69D',
    'question_label': "Attitude/Opinion Q69D (Codebook missing)",
    'type': 'categorical',
    'value_labels': {'strongly_disagree': 'Strongly Disagree', 'disagree': 'Disagree', 'neutral': 'Neutral', 'agree': 'Agree', 'strongly_agree': 'Strongly Agree'},
}