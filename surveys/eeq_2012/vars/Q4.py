# op_qc_difference — Principale différence entre Québécois et reste du Canada
# Source: Q4
df_clean['op_qc_difference'] = df['Q4'].map({
    1.0: 'language',
    2.0: 'religion',
    3.0: 'culture',
    4.0: 'values',
    5.0: 'history',
    7.0: 'no_difference',
    8.0: np.nan,
    9.0: np.nan,
})
CODEBOOK_VARIABLES['op_qc_difference'] = {
    'original_variable': 'Q4',
    'question_label': "According to you, what is the main difference between Québécois people and people from the rest of Canada?",
    'type': 'categorical',
    'value_labels': {
        'language': "Language",
        'religion': "Religion",
        'culture': "Culture",
        'values': "Values",
        'history': "History",
        'no_difference': "There are no important differences between these two groups",
    },
}
