# op_q70e — Attitude scale 0-10
# Source: Q70E (No codebook provided for this variable/survey, derived from data exploration)
# Assumption: 0 is most negative, 10 is most positive. Normalizing by dividing by 10.0.
# Assumption: Codes 98.0 and 99.0 are unmapped and treated as missing.
df_clean['op_q70e'] = df['Q70E'].map({
    0.0: 0.0,
    1.0: 0.1,
    2.0: 0.2,
    3.0: 0.3,
    4.0: 0.4,
    5.0: 0.5,
    6.0: 0.6,
    7.0: 0.7,
    8.0: 0.8,
    9.0: 0.9,
    10.0: 1.0,
    98.0: np.nan,
    99.0: np.nan,
})
CODEBOOK_VARIABLES['op_q70e'] = {
    'original_variable': 'Q70E',
    'question_label': "Attitude scale (0-10) based on data exploration",
    'type': 'likert',
    'value_labels': {'0.0': "Most Negative (0)", '1.0': "0.1", '2.0': "0.2", '3.0': "0.3", '4.0': "0.4", '5.0': "Midpoint (0.5)", '6.0': "0.6", '7.0': "0.7", '8.0': "0.8", '9.0': "0.9", '1.0': "Most Positive (1.0)"},
}
