# op_voting_intention — Voting intention (inferred)
# Source: q43
# NOTE: Codebook entry was missing. Mapping derived from data exploration (float codes assumed to be categorical keys).
# Assumption: All unique float codes observed are valid categories.
df_clean['op_voting_intention'] = df['q43'].map({
    0.0: 'other_or_none',
    1.0: 'party_a',
    2.0: 'party_b',
    3.0: 'party_c',
    4.0: 'party_d',
    5.0: 'party_e',
    7.0: 'party_f',
    8.0: 'party_g',
    10.0: 'party_h',
    12.0: 'party_i',
    13.0: 'party_j',
    15.0: 'party_k',
    20.0: 'party_l',
    22.0: 'party_m',
    25.0: 'party_n',
    30.0: 'party_o',
    35.0: 'party_p',
    40.0: 'party_q',
    45.0: 'party_r',
    50.0: 'party_s',
    54.0: 'party_t',
    55.0: 'party_u',
    60.0: 'party_v',
    61.0: 'party_w',
    65.0: 'party_x',
})
CODEBOOK_VARIABLES['op_voting_intention'] = {
    'original_variable': 'q43',
    'question_label': "Voting intention (label inferred due to missing codebook)",
    'type': 'categorical',
    'value_labels': {'other_or_none': "Other/None (Code 0)", 'party_a': "Party A (Code 1)", 'party_b': "Party B (Code 2)", 'party_c': "Party C (Code 3)", 'party_d': "Party D (Code 4)", 'party_e': "Party E (Code 5)", 'party_f': "Party F (Code 7)", 'party_g': "Party G (Code 8)", 'party_h': "Party H (Code 10)", 'party_i': "Party I (Code 12)", 'party_j': "Party J (Code 13)", 'party_k': "Party K (Code 15)", 'party_l': "Party L (Code 20)", 'party_m': "Party M (Code 22)", 'party_n': "Party N (Code 25)", 'party_o': "Party O (Code 30)", 'party_p': "Party P (Code 35)", 'party_q': "Party Q (Code 40)", 'party_r': "Party R (Code 45)", 'party_s': "Party S (Code 50)", 'party_t': "Party T (Code 54)", 'party_u': "Party U (Code 55)", 'party_v': "Party V (Code 60)", 'party_w': "Party W (Code 61)", 'party_x': "Party X (Code 65)"},
}