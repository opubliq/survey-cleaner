# ses_code3 — Unknown categorical code variable
# Source: CODE3
# Assumption: Code 9 treated as missing, letters mapped to lowercase for consistency
df_clean['ses_code3'] = df['CODE3'].map({
    '9': np.nan,
    'A': 'a',
    'B': 'b',
    'C': 'c',
    'E': 'e',
    'G': 'g',
    'H': 'h',
    'J': 'j',
    'K': 'k',
    'L': 'l',
    'M': 'm',
    'N': 'n',
    'P': 'p',
    'R': 'r',
    'S': 's',
    'T': 't',
    'V': 'v',
    'W': 'w',
    'X': 'x',
    'Y': 'y',
    'Z': 'z',
})
CODEBOOK_VARIABLES['ses_code3'] = {
    'original_variable': 'CODE3',
    'question_label': "Unknown: Categorical codes from data exploration",
    'type': 'categorical',
    'value_labels': {'a': 'Code A label (needs verification)', 'b': 'Code B label (needs verification)', 'c': 'Code C label (needs verification)', 'e': 'Code E label (needs verification)', 'g': 'Code G label (needs verification)', 'h': 'Code H label (needs verification)', 'j': 'Code J label (needs verification)', 'k': 'Code K label (needs verification)', 'l': 'Code L label (needs verification)', 'm': 'Code M label (needs verification)', 'n': 'Code N label (needs verification)', 'p': 'Code P label (needs verification)', 'r': 'Code R label (needs verification)', 's': 'Code S label (needs verification)', 't': 'Code T label (needs verification)', 'v': 'Code V label (needs verification)', 'w': 'Code W label (needs verification)', 'x': 'Code X label (needs verification)', 'y': 'Code Y label (needs verification)', 'z': 'Code Z label (needs verification)'},
}