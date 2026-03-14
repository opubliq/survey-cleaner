# op_vote_intent — Vote intention/preference
# Source: Q101F
# Assumption: Variable is binary, 1.0 = Yes/Support, 2.0 = No/Oppose. Codes 8.0/9.0 are treated as missing.
df_clean['op_vote_intent'] = df['Q101F'].map({
    1.0: 'yes',
    2.0: 'no',
    8.0: np.nan,
    9.0: np.nan,
})
CODEBOOK_VARIABLES['op_vote_intent'] = {
    'original_variable': 'Q101F',
    'question_label': "Inferred: Vote Intention/Preference (1=Yes, 2=No, 8/9=Missing)",
    'type': 'binary',
    'value_labels': {'yes': "Intends to vote / Supports", 'no': "Does not intend to vote / Opposes"},
}