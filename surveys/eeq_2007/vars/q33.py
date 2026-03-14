RAW_NAME = "q33"
standard_name = "ses_q33"
df_clean[standard_name] = df[RAW_NAME].astype(float)

# Mapping from raw values (1-5) to 0.0-1.0 for Likert scale
mapping = {
    1.0: 0.2,  # très satisfait
    2.0: 0.4,  # assez satisfait
    3.0: 0.6,  # ni satisfait ni insatisfait
    4.0: 0.8,  # assez insatisfait
    5.0: 1.0,  # très insatisfait
}
df_clean[standard_name] = df_clean[standard_name].map(mapping)

# Set CODEBOOK_VARIABLES entry
CODEBOOK_VARIABLES[standard_name] = {
    'original_variable': RAW_NAME,
    'question_label': "Opinion sur la performance du gouvernement libéral",
    'type': 'likert',
    'value_labels': {
        "0.2": "très satisfait",
        "0.4": "assez satisfait",
        "0.6": "ni satisfait ni insatisfait",
        "0.8": "assez insatisfait",
        "1.0": "très insatisfait"
    }
}
# Missing codes (8, 9) will map to NaN by default when using .map() on floats