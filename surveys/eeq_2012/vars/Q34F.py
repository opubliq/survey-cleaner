# op_q34f — Attitude towards issue Q34F
# Source: Q34F
# Assumption: Codes 1.0-4.0 are valid categories. Codes 8.0 and 9.0 are treated as missing (DK/Refused).
df_clean['op_q34f'] = df['Q34F'].map({
    1.0: 'strongly_disagree',
    2.0: 'disagree',
    3.0: 'agree',
    4.0: 'strongly_agree',
    8.0: np.nan, # Assumption: DK
    9.0: np.nan, # Assumption: Refused
})
CODEBOOK_VARIABLES['op_q34f'] = {
    'original_variable': 'Q34F',
    'question_label': "Attitude towards issue Q34F (Inferred categories as codebook values were missing)",
    'type': 'categorical',
    'value_labels': {'strongly_disagree': "Strongly Disagree", 'disagree': "Disagree", 'agree': "Agree", 'strongly_agree': "Strongly Agree"},
}