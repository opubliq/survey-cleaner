# op_favorability_alex_tyrrell — Favorability rating for Alex Tyrrell (Normalized 0-1)
# Source: Q29F
# Strategy: Likert scale 0-100, normalize to 0.0-1.0. Map explicit codes 997-999 to NaN.
mapping = {}
for i in range(101):
    mapping[float(i)] = i / 100.0

# Explicit non-response codes from codebook
mapping[997.0] = np.nan
mapping[998.0] = np.nan
mapping[999.0] = np.nan

df_clean['op_favorability_alex_tyrrell'] = df['Q29F'].map(mapping)

CODEBOOK_VARIABLES['op_favorability_alex_tyrrell'] = {
    'original_variable': 'Q29F',
    'question_label': "Sur une échelle de ZERO à CENT, où zéro veut dire que vous N'AIMEZ VRAIMENT PAS DU TOUT un politicien, et cent veut dire que vous L'AIMEZ VRAIMENT BEAUCOUP, que pensez-vous de: ALEX TYRRELL? (Normalized 0-1)",
    'type': 'likert',
    'value_labels': {
        '0.00': "0/100 - Not at all favorable",
        '1.00': "1/100",
        '0.50': "50/100 - Neutral",
        '1.00': "100/100 - Very favorable",
        'NaN': "Missing/Refused"
    }
}