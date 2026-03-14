# op_q55 — Likely political opinion or behaviour indicator
# Source: q55
# Assumption: Codes '01' through '05' are labelled options. Codes '96' to '99' are treated as missing (unmapped).
df_clean['op_q55'] = df['q55'].map({
    '01': 'option_one',
    '02': 'option_two',
    '03': 'option_three',
    '04': 'option_four',
    '05': 'option_five',
})
CODEBOOK_VARIABLES['op_q55'] = {
    'original_variable': 'q55',
    'question_label': "Unknown question for q55",
    'type': 'categorical',
    'value_labels': {'option_one': "First option", 'option_two': "Second option", 'option_three': "Third option", 'option_four': "Fourth option", 'option_five': "Fifth option"},
}