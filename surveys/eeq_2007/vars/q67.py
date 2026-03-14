# op_party_support_67 — Assumed Likert scale for variable q67
# Source: q67
# Assumption: Variable is a 5-point Likert scale from -2 (Strongly Disagree) to 2 (Strongly Agree).
# Assumption: Missing code 99 maps to np.nan.
# TODO: Verify exact question label, raw codes, and missing codes for q67 from the actual codebook.
df_clean['op_party_support_67'] = df['q67'].map({
    -2.0: 0.0,
    -1.0: 0.25,
    0.0: 0.5,
    1.0: 0.75,
    2.0: 1.0,
    99.0: np.nan,
})
CODEBOOK_VARIABLES['op_party_support_67'] = {
    'original_variable': 'q67',
    'question_label': "Assumed Likert scale for Q67 on [TOPIC].",
    'type': 'likert',
    'value_labels': {0.0: 'strongly disagree', 0.25: 'disagree', 0.5: 'neutral', 0.75: 'agree', 1.0: 'strongly agree'},
}