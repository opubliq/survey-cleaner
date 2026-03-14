# op_q13 — Response to Question 13
# Source: Q13
# Note: Codebook entry missing, proceeding with inferred mapping based on observed data values (1-6 assumed to be categories, 96/98/99 assumed missing).
df_clean['op_q13'] = df['Q13'].map({
    1.0: 'quebec',
    2.0: 'ontario',
    3.0: 'alberta',
    4.0: 'manitoba',
    5.0: 'saskatchewan',
    6.0: 'other_province',
    96.0: np.nan,
    98.0: np.nan,
    99.0: np.nan,
})
CODEBOOK_VARIABLES['op_q13'] = {
    'original_variable': 'Q13',
    'question_label': "Response to Question 13 (Codebook Missing - Inferred Categories)",
    'type': 'categorical',
    'value_labels': {'quebec': "Québec", 'ontario': "Ontario", 'alberta': "Alberta", 'manitoba': "Manitoba", 'saskatchewan': "Saskatchewan", 'other_province': "Other Province"},
}