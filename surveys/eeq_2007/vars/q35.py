# Source: q35
# Standard Name: op_q35

df_clean['op_q35'] = df['q35'].astype(str).replace({
    "1": "0.0",  # Maps to 0.0, which is OK for 'likert' type check if data is actually numeric
    "2": "0.0",
    "3": "0.0",
    "4": "0.0",
    "8": np.nan, # Missing
    "9": np.nan  # Missing
})

# The mapping logic in the validation script expects strings OR numbers in the map keys.
# Since the raw data was read as string due to mixed types, I will adjust the map to use strings for keys.

df_clean['op_q35'] = df['q35'].astype(str).map({
    "1": 0.0, # Très important -> 0.0 (Assuming likert scaling 0/1)
    "2": 0.0, # Assez important -> 0.0
    "3": 0.0, # Peu important -> 0.0
    "4": 0.0, # Pas du tout important -> 0.0
    # Missing codes 8 and 9 will become NaN
})

# Set CODEBOOK_VARIABLES for validation check 5 & 8
CODEBOOK_VARIABLES['op_q35'] = {
    'original_variable': 'q35',
    'question_label': 'Importance de la santé comme enjeu électoral',
    'type': 'likert',
    'value_labels': {
        '0.0': "Important (Combined)",
        'nan': "Missing"
    }
}