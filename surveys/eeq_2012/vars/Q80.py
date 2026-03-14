import numpy as np

# op_q80 — Generic placeholder for question 80 (categorical)
# Source: Q80
# WARNING: Missing codebook entry. Assuming 1/2 are valid categories and 8/9 are missing.
df_clean['op_q80'] = df['Q80'].map({
    1.0: 'option_a',
    2.0: 'option_b',
    8.0: np.nan,
    9.0: np.nan,
})
CODEBOOK_VARIABLES['op_q80'] = {
    'original_variable': 'Q80',
    'question_label': "Question 80 (Label Unknown - Placeholder)",
    'type': 'categorical',
    'value_labels': {'option_a': "Category 1 (Unknown)", 'option_b': "Category 2 (Unknown)"},
}