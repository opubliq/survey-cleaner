# op_q43b — Unknown categorical response variable
# Source: Q43B
# Assumption: Codes mapped arbitrarily due to missing codebook entry.
# TODO: verify mapping for all codes observed in data.
df_clean['op_q43b'] = df['Q43B'].map({
    0.0: 'none',
    2.0: 'response_a',
    3.0: 'response_b',
    4.0: 'response_c',
    5.0: 'response_d',
    6.0: 'response_e',
    10.0: 'response_f',
    15.0: 'response_g',
    20.0: 'response_h',
    25.0: 'response_i',
    30.0: 'response_j',
    33.0: 'response_k',
    35.0: 'response_l',
    36.0: 'response_m',
    40.0: 'response_n',
    44.0: 'response_o',
    45.0: 'response_p',
    46.0: 'response_q',
    48.0: 'response_r',
    49.0: 'response_s',
    50.0: 'majority_response',
    55.0: 'response_u',
    56.0: 'response_v',
    60.0: 'response_w',
    99.0: np.nan,
})
CODEBOOK_VARIABLES['op_q43b'] = {
    'original_variable': 'Q43B',
    'question_label': "Placeholder for Q43B question text",
    'type': 'categorical',
    'value_labels': {'none': "None/Baseline", 'majority_response': "Most frequent response"}
}