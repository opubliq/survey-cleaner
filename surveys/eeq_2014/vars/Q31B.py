# op_q31b — Likert scale question Q31B
# Source: Q31B
# Assumption: Mapping 0 to 0.0 (most negative) and 10 to 1.0 (most positive) for Likert scale.
# Assumption: Codes 98 and 99 are treated as missing as they are unlabelled in the inferred context.
df_clean['op_q31b'] = df['Q31B'].map({
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
CODEBOOK_VARIABLES['op_q31b'] = {
    'original_variable': 'Q31B',
    'question_label': "Likert scale question Q31B",
    'type': 'likert',
    'value_labels': {
        '0.0': "Most Negative End of Scale",
        '1.0': "Most Positive End of Scale",
        'np.nan': "Missing/Refused"
    }
}