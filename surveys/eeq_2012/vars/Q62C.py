# op_q62c — Unknown opinion/attitude variable based on Q62C
# Source: Q62C
# Assumption: Only codes 1.0 and 2.0 have meaningful labels; all others are treated as missing.
# Note: Question label and value labels are placeholders due to missing codebook entry.
df_clean['op_q62c'] = df['Q62C'].map({
    1.0: 'cat_a',
    2.0: 'cat_b',
    6.0: np.nan,
    8.0: np.nan,
    9.0: np.nan,
})
CODEBOOK_VARIABLES['op_q62c'] = {
    'original_variable': 'Q62C',
    'question_label': "Unknown question text for Q62C",
    'type': 'categorical',
    'value_labels': {'cat_a': "Category A (Inferred)", 'cat_b': "Category B (Inferred)"},
}