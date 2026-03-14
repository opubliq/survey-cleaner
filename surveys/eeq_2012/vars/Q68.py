# behav_vote_intent_q68 — Vote intention/preference for Q68
# Source: Q68
# WARNING: Codebook not provided for Q68. Mapping inferred from data exploration.
# Assumption: 0.0 is 'no_response' or other non-choice, other codes are discrete choices.
df_clean['behav_vote_intent_q68'] = df['Q68'].map({
    0.0: 'no_response',
    1.0: 'choice_1',
    2.0: 'choice_2',
    3.0: 'choice_3',
    4.0: 'choice_4',
    5.0: 'choice_5',
    6.0: 'choice_6',
    8.0: 'choice_8',
    10.0: 'choice_10',
    12.0: 'choice_12',
    15.0: 'choice_15',
    16.0: 'choice_16',
    17.0: 'choice_17',
    18.0: 'choice_18',
    19.0: 'choice_19',
    20.0: 'choice_20',
    22.0: 'choice_22',
    25.0: 'choice_25',
    30.0: 'choice_30',
    33.0: 'choice_33',
    35.0: 'choice_35',
    37.0: 'choice_37',
    40.0: 'choice_40',
    45.0: 'choice_45',
    46.0: 'choice_46',
})
CODEBOOK_VARIABLES['behav_vote_intent_q68'] = {
    'original_variable': 'Q68',
    'question_label': "Inferred: Vote intention/preference for Q68",
    'type': 'categorical',
    'value_labels': {'no_response': "No Response/Other (Inferred)", 'choice_1': "Choice 1 (Inferred)", 'choice_2': "Choice 2 (Inferred)", 'choice_3': "Choice 3 (Inferred)", 'choice_4': "Choice 4 (Inferred)", 'choice_5': "Choice 5 (Inferred)", 'choice_6': "Choice 6 (Inferred)", 'choice_8': "Choice 8 (Inferred)", 'choice_10': "Choice 10 (Inferred)", 'choice_12': "Choice 12 (Inferred)", 'choice_15': "Choice 15 (Inferred)", 'choice_16': "Choice 16 (Inferred)", 'choice_17': "Choice 17 (Inferred)", 'choice_18': "Choice 18 (Inferred)", 'choice_19': "Choice 19 (Inferred)", 'choice_20': "Choice 20 (Inferred)", 'choice_22': "Choice 22 (Inferred)", 'choice_25': "Choice 25 (Inferred)", 'choice_30': "Choice 30 (Inferred)", 'choice_33': "Choice 33 (Inferred)", 'choice_35': "Choice 35 (Inferred)", 'choice_37': "Choice 37 (Inferred)", 'choice_40': "Choice 40 (Inferred)", 'choice_45': "Choice 45 (Inferred)", 'choice_46': "Choice 46 (Inferred)"},
}