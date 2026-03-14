# op_attitude_q66 — Unknown attitude/opinion variable
# Source: Q66
# Note: No codebook entry found, mapping derived from observed data values. All values are treated as distinct categories.
df_clean['op_attitude_q66'] = df['Q66'].map({
    1.0: 'code_1',
    2.0: 'code_2',
    7.0: 'code_7',
    10.0: 'code_10',
    12.0: 'code_12',
    14.0: 'code_14',
    18.0: 'code_18',
    22.0: 'code_22',
    23.0: 'code_23',
    24.0: 'code_24',
    25.0: 'code_25',
    26.0: 'code_26',
    30.0: 'code_30',
    34.0: 'code_34',
    43.0: 'code_43',
    46.0: 'code_46',
    48.0: 'code_48',
    50.0: 'code_50',
    51.0: 'code_51',
    52.0: 'code_52',
    53.0: 'code_53',
    54.0: 'code_54',
    60.0: 'code_60',
    61.0: 'code_61',
    63.0: 'code_63',
})
CODEBOOK_VARIABLES['op_attitude_q66'] = {
    'original_variable': 'Q66',
    'question_label': "Q66 (Missing label)",
    'type': 'categorical',
    'value_labels': {
        'code_1': 'Code 1 (Observed)', 'code_2': 'Code 2 (Observed)', 'code_7': 'Code 7 (Observed)', 
        'code_10': 'Code 10 (Observed)', 'code_12': 'Code 12 (Observed)', 'code_14': 'Code 14 (Observed)', 
        'code_18': 'Code 18 (Observed)', 'code_22': 'Code 22 (Observed)', 'code_23': 'Code 23 (Observed)', 
        'code_24': 'Code 24 (Observed)', 'code_25': 'Code 25 (Observed)', 'code_26': 'Code 26 (Observed)', 
        'code_30': 'Code 30 (Observed)', 'code_34': 'Code 34 (Observed)', 'code_43': 'Code 43 (Observed)', 
        'code_46': 'Code 46 (Observed)', 'code_48': 'Code 48 (Observed)', 'code_50': 'Code 50 (Observed)', 
        'code_51': 'Code 51 (Observed)', 'code_52': 'Code 52 (Observed)', 'code_53': 'Code 53 (Observed)', 
        'code_54': 'Code 54 (Observed)', 'code_60': 'Code 60 (Observed)', 'code_61': 'Code 61 (Observed)', 
        'code_63': 'Code 63 (Observed)'
    }
}