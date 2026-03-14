# op_q12a — Standard 5-point Likert-style question (Inferred)
# Source: q12a
# Assumption: Codes 1-5 map to agreement scale. Codes 96-99 are treated as missing/unlabeled.
df_clean['op_q12a'] = df['q12a'].map({
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
CODEBOOK_VARIABLES['op_q12a'] = {
    'original_variable': 'q12a',
    'question_label': "Question 12a - Placeholder label (Codebook missing)",
    'type': 'categorical',
    'value_labels': {'strongly_disagree': "Strongly Disagree (Inferred)", 'disagree': "Disagree (Inferred)", 'neutral': "Neutral (Inferred)", 'agree': "Agree (Inferred)", 'strongly_agree': "Strongly Agree (Inferred)"},
}