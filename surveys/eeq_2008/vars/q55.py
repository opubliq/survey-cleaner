# op_q55 — Attitude regarding statement Q55
# Source: q55
# Assumption: Codes >= 96.0 treated as missing (96, 97, 98, 99) based on distribution.
df_clean['op_q55'] = df['q55'].map({
    1.0: 'strongly_disagree',
    2.0: 'disagree',
    3.0: 'neutral',
    4.0: 'agree',
    5.0: 'strongly_agree',
    96.0: np.nan,
    97.0: np.nan,
    98.0: np.nan,
    99.0: np.nan,
})
CODEBOOK_VARIABLES['op_q55'] = {
    'original_variable': 'q55',
    'question_label': "Attitude regarding statement Q55 (Assumed)",
    'type': 'categorical',
    'value_labels': {'strongly_disagree': "Strongly Disagree", 'disagree': "Disagree", 'neutral': "Neutral", 'agree': "Agree", 'strongly_agree': "Strongly Agree"},
}