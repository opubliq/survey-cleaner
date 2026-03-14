# op_q14 — Inferred opinion/attitude measure scaled 0-1
# Source: q14
# Assumption: Variable is numeric scaled 0-10. Max value is 10.0. Codes 0.0-10.0 mapped to 0.0-1.0.
df_clean['op_q14'] = df['q14'].map({
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
})
CODEBOOK_VARIABLES['op_q14'] = {
    'original_variable': 'q14',
    'question_label': "Inferred: Question regarding attitude/opinion (scale 0-10)",
    'type': 'numeric',
    'value_labels': {'0.0': "Min", '1.0': "1/10", '5.0': "Midpoint", '10.0': "Max"},
}