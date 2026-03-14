# op_accommodations_importance — Importance of reasonable accommodations as political issue
# Source: q10b
df_clean['op_accommodations_importance'] = df['q10b'].map({
    '1': 1.0,
    '2': 0.667,
    '3': 0.333,
    '4': 0.0,
    '8': np.nan,
    '9': np.nan,
})
CODEBOOK_VARIABLES['op_accommodations_importance'] = {
    'original_variable': 'q10b',
    'question_label': "Est-ce que les accomodements raisonnables ÉTAIENT un enjeu important pour vous dans cette élection ?",
    'type': 'likert',
    'value_labels': {1.0: "très important", 0.667: "assez important", 0.333: "peu important", 0.0: "pas du tout important"},
}
