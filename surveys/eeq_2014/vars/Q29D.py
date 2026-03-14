# op_fdavid_rating — Opinion rating for Françoise David (0-100 scale)
# Source: Q29D
# Note: Variable is a 0-100 feeling thermometer disguised as categorical. Codes 997-999 are explicit missing values.
# Assumption: All other values found in the data are valid ratings (0-100) and are scaled by dividing by 100.0.
df_clean['op_fdavid_rating'] = df['Q29D'].map({
    997.0: np.nan,
    998.0: np.nan,
    999.0: np.nan,
}).fillna(df['Q29D'] / 100.0)

CODEBOOK_VARIABLES['op_fdavid_rating'] = {
    'original_variable': 'Q29D',
    'question_label': "Sur une échelle de ZERO à CENT, où zéro veut dire que vous N'AIMEZ VRAIMENT PAS DU TOUT un politicien, et cent veut dire que vous L'AIMEZ VRAIMENT BEAUCOUP, que pensez-vous de FRANÇOISE DAVID? / Entrez une réponse (entre 0 et 100)",
    'type': 'numeric',
    'value_labels': {'0.0': "N'aime vraiment pas du tout", '1.0': "Rating 1/100", '100.0': "Aime vraiment beaucoup"},
}