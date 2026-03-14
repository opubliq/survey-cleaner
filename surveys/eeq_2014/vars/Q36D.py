# op_attitude_q36d — Attitude question (unknown content)
# Source: Q36D
# Note: Codebook entry was missing. Assuming 1-4 is a likert scale normalized 0-1.
# Codes 8.0 and 9.0 treated as missing (unlabelled in data exploration).
df_clean['op_attitude_q36d'] = df['Q36D'].map({
    1.0: 0.0,    # Maps 1.0 to the lowest point (0.0)
    2.0: 0.33,   # Maps 2.0 to the middle-low point (approx 1/3)
    3.0: 0.66,   # Maps 3.0 to the middle-high point (approx 2/3)
    4.0: 1.0,    # Maps 4.0 to the highest point (1.0)
    8.0: np.nan, # Treat code 8.0 as missing
    9.0: np.nan, # Treat code 9.0 as missing
})
CODEBOOK_VARIABLES['op_attitude_q36d'] = {
    'original_variable': 'Q36D',
    'question_label': "Attitude question Q36D (label unknown, using placeholder)",
    'type': 'likert',
    'value_labels': {
        '0.0': "Lowest point (Code 1)",
        '0.33': "Low point (Code 2)",
        '0.66': "High point (Code 3)",
        '1.0': "Highest point (Code 4)",
    }
}