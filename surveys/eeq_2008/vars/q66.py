# behav_vote_intent_q66 — Assumed voting intention or related behavior question
# Source: q66
# Assumption: Codes 8.0 and 9.0 are treated as missing/unlabelled.
df_clean['behav_vote_intent_q66'] = df['q66'].map({
    1.0: 'option_one',
    2.0: 'option_two',
    8.0: np.nan,
    9.0: np.nan,
})
CODEBOOK_VARIABLES['behav_vote_intent_q66'] = {
    'original_variable': 'q66',
    'question_label': "Question 66 (No label provided)",
    'type': 'categorical',
    'value_labels': {'option_one': "Code 1 Response", 'option_two': "Code 2 Response"},
}