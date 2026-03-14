# op_mps_out_of_touch — Les élus perdent vite contact avec les gens (Likert 0-1)
# Source: q22
df_clean['op_mps_out_of_touch'] = df['q22'].map({
    1.0: 1.0,    # Fortement d'accord
    2.0: 0.667,  # Plutôt d'accord
    3.0: 0.333,  # Plutôt en désaccord
    4.0: 0.0,    # Fortement en désaccord
    8.0: np.nan,
    9.0: np.nan,
})
CODEBOOK_VARIABLES['op_mps_out_of_touch'] = {
    'original_variable': 'q22',
    'question_label': "Ceux qui sont élus au Parlement perdent vite contact avec les gens.",
    'type': 'likert',
    'value_labels': {
        1.0: "Fortement d'accord",
        0.667: "Plutôt d'accord",
        0.333: "Plutôt en désaccord",
        0.0: "Fortement en désaccord",
    },
}
