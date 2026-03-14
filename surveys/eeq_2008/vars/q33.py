# op_rating_q33 — General rating on question Q33
# Source: q33
# Assumption: Codes 8/9 treated as missing as they are outside the 1-4 scale.
# Assumption: Question label is generic as codebook was not provided.
df_clean['op_rating_q33'] = df['q33'].map({
    1.0: 'low',
    2.0: 'medium_low',
    3.0: 'medium_high',
    4.0: 'high',
    8.0: np.nan,
    9.0: np.nan,
})
CODEBOOK_VARIABLES['op_rating_q33'] = {
    'original_variable': 'q33',
    'question_label': "Generic rating for Q33 (Mapping derived from data exploration)",
    'type': 'categorical',
    'value_labels': {'low': "Low/Strongly Disagree", 'medium_low': "Medium Low", 'medium_high': "Medium High", 'high': "High/Strongly Agree"},
}