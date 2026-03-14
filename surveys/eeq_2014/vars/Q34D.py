# op_opinion_d — Opinion regarding statement D
# Source: Q34D
# Assumption: Likert scale mapped to 0.0 (Strongly Disagree) to 1.0 (Strongly Agree).
# Assumption: Codes 8 (DK) and 9 (Refusal) treated as missing (np.nan).
df_clean['op_opinion_d'] = df['Q34D'].map({
    1.0: 0.0,
    2.0: 0.25,
    3.0: 0.75,
    4.0: 1.0,
    8.0: np.nan,
    9.0: np.nan,
})
CODEBOOK_VARIABLES['op_opinion_d'] = {
    'original_variable': 'Q34D',
    'question_label': "Opinion regarding statement D (Assumed from codes)",
    'type': 'likert',
    'value_labels': {0.0: "Strongly Disagree", 0.25: "Disagree", 0.75: "Agree", 1.0: "Strongly Agree"},
}
