# op_q62h — Voting status (Inferred)
# Source: Q62H
# Assumption: Codes 6.0, 8.0, 9.0 are non-response/missing, mapped to np.nan
df_clean['op_q62h'] = df['Q62H'].map({
    1.0: 'yes',
    2.0: 'no',
    6.0: np.nan,
    8.0: np.nan,
    9.0: np.nan,
})
CODEBOOK_VARIABLES['op_q62h'] = {
    'original_variable': 'Q62H',
    'question_label': "Status for Q62H (Label unknown, using inferred mapping)",
    'type': 'categorical',
    'value_labels': {'yes': "Yes", 'no': "No"},
}