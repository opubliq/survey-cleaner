# op_q21 — Question 21 (Unknown meaning)
# Source: Q21
# Assumption: Based on exploration, codes 1.0, 2.0, and 9.0 are present.
# Assumption: This is a categorical variable. Mapped values are invented due to missing codebook.
df_clean['op_q21'] = df['Q21'].map({
    1.0: 'yes',
    2.0: 'no',
    9.0: np.nan, # Treating 9.0 as explicit missing/refused
})
CODEBOOK_VARIABLES['op_q21'] = {
    'original_variable': 'Q21',
    'question_label': "Unknown question for Q21",
    'type': 'categorical',
    'value_labels': {'yes': "Yes", 'no': "No"},
}