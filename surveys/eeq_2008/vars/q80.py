# op_vote_intention_q80 — Inferred vote intention question
# Source: q80
# WARNING: Codebook details (question text, value labels) are missing. Mappings are generic placeholders.
# Assumption: Codes 96 and 99 are missing values and will be mapped to np.nan automatically.
df_clean['op_vote_intention_q80'] = df['q80'].map({
    1.0: 'intention_1',
    2.0: 'intention_2',
    3.0: 'intention_3',
    4.0: 'intention_4',
    5.0: 'intention_5',
    6.0: 'intention_6',
    8.0: 'intention_8',
    9.0: 'intention_9',
    10.0: 'intention_10',
    12.0: 'intention_12',
})
CODEBOOK_VARIABLES['op_vote_intention_q80'] = {
    'original_variable': 'q80',
    'question_label': "Inferred Q80 (Vote Intention?) - **MANUAL VERIFICATION REQUIRED**",
    'type': 'categorical',
    'value_labels': {
        'intention_1': 'Value 1 (Verify)',
        'intention_2': 'Value 2 (Verify)',
        'intention_3': 'Value 3 (Verify)',
        'intention_4': 'Value 4 (Verify)',
        'intention_5': 'Value 5 (Verify)',
        'intention_6': 'Value 6 (Verify)',
        'intention_8': 'Value 8 (Verify)',
        'intention_9': 'Value 9 (Verify)',
        'intention_10': 'Value 10 (Verify)',
        'intention_12': 'Value 12 (Verify)',
    }
}