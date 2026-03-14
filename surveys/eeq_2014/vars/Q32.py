# op_attitude_q32 — Opinion/Attitude (Likert scale 0-10, scaled 0.0-1.0)
# Source: Q32
# Assumption: Variable is a 0-10 scale (0.0 to 1.0 after scaling). Codes 98.0 and 99.0 treated as missing.
df_clean['op_attitude_q32'] = df['Q32'].map({
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
CODEBOOK_VARIABLES['op_attitude_q32'] = {
    'original_variable': 'Q32',
    'question_label': "Opinion/Attitude based on Q32 (No codebook provided, assumed 0-10 Likert)",
    'type': 'likert',
    'value_labels': {'0.0': "Strongest negative end (0)", '1.0': "Strongest positive end (10)"},
}