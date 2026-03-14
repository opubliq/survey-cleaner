# op_q91 — Unknown attitude/opinion response mapping
# Source: Q91
# Assumption: Codes 1, 2, 3 mapped to positive/neutral/negative. Codes 8, 9 treated as missing (np.nan).
df_clean['op_q91'] = df['Q91'].map({
    1.0: 'positive',
    2.0: 'neutral',
    3.0: 'negative',
    8.0: np.nan,
    9.0: np.nan,
})
CODEBOOK_VARIABLES['op_q91'] = {
    'original_variable': 'Q91',
    'question_label': "Q91 (Label missing, assuming general opinion response)",
    'type': 'categorical',
    'value_labels': {'positive': "Observed value 1 (assumed positive)", 'neutral': "Observed value 2 (assumed neutral)", 'negative': "Observed value 3 (assumed negative)"},
}