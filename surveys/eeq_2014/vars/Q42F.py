# op_q42f — Best guess at opinion/frequency scale based on data range 1-6
# Source: Q42F
# Assumption: Codes 1.0-6.0 mapped to a frequency/opinion scale. Codes 96.0, 98.0, 99.0 treated as missing.
df_clean['op_q42f'] = df['Q42F'].map({
    1.0: 'very low',
    2.0: 'low',
    3.0: 'somewhat low',
    4.0: 'somewhat high',
    5.0: 'high',
    6.0: 'very high',
    96.0: np.nan,
    98.0: np.nan,
    99.0: np.nan,
})
CODEBOOK_VARIABLES['op_q42f'] = {
    'original_variable': 'Q42F',
    'question_label': "Frequency/Opinion for Q42F (Label unknown, inferred mapping)",
    'type': 'categorical',
    'value_labels': {'very low': "Very Low", 'low': "Low", 'somewhat low': "Somewhat Low", 'somewhat high': "Somewhat High", 'high': "High", 'very high': "Very High"},
}