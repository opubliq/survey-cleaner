# op_q34 — Opinion question q34
# Source: q34
# Assumption: Codes 8 and 9 are treated as missing (not explicitly labelled in codebook)
df_clean['op_q34'] = df['q34'].map({
    1.0: 'positive',
    2.0: 'negative',
    8.0: np.nan,
    9.0: np.nan,
})
CODEBOOK_VARIABLES['op_q34'] = {
    'original_variable': 'q34',
    'question_label': "Opinion question q34 (Codebook label missing, inferred categorical)",
    'type': 'categorical',
    'value_labels': {'positive': "Positive response or agreement", 'negative': "Negative response or disagreement"},
}