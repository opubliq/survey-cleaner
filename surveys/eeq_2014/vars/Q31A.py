# behav_political_donation_last12m — Avez-vous fait un don à un parti politique ou à un candidat lors des 12 derniers mois?
# Source: Q31A
# Assumption: Codes 0.0, 3.0-10.0, 98.0, 99.0 are treated as missing (np.nan) as they are not documented in codebook values.
import numpy as np

# Assuming df_clean and df are pandas DataFrames available in the scope
# Mapping based on the provided strategy: only 1.0 and 2.0 are kept, others become np.nan.
df_clean['behav_political_donation_last12m'] = df['Q31A'].map({
    1.0: 'oui',
    2.0: 'non',
    0.0: np.nan,
    3.0: np.nan,
    4.0: np.nan,
    5.0: np.nan,
    6.0: np.nan,
    7.0: np.nan,
    8.0: np.nan,
    9.0: np.nan,
    10.0: np.nan,
    98.0: np.nan,
    99.0: np.nan,
})
# The variable 'value_labels' in the final codebook should map the new cleaned string values back to human-readable text.
CODEBOOK_VARIABLES['behav_political_donation_last12m'] = {
    'original_variable': 'Q31A',
    'question_label': "Avez-vous fait un don à un parti politique ou à un candidat lors des 12 derniers mois?",
    'type': 'categorical',
    # Mapping from cleaned string values to original labels
    'value_labels': {'oui': "Oui", 'non': "Non"},
}