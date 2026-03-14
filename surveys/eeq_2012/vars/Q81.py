# op_attitude_q81 — Generic attitude/opinion question 81
# Source: Q81
# WARNING: No codebook provided. Mapping 1-5 to generic labels and treating 8/9 as missing.
df_clean['op_attitude_q81'] = df['Q81'].map({
    1.0: 'strong_support',
    2.0: 'weak_support',
    3.0: 'neutral',
    4.0: 'dont_know',
    5.0: 'refused',
    8.0: np.nan,
    9.0: np.nan,
})
CODEBOOK_VARIABLES['op_attitude_q81'] = {
    'original_variable': 'Q81',
    'question_label': "Unknown: Q81 from eeq_2012 data",
    'type': 'categorical',
    'value_labels': {'strong_support': "Strong Support (Inferred)", 'weak_support': "Weak Support (Inferred)", 'neutral': "Neutral (Inferred)", 'dont_know': "Don't Know (Inferred)", 'refused': "Refused (Inferred)"},
}