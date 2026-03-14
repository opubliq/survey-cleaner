# geo_postal_code — CODE POSTAL (Postal code)
# Source: codep
# Note: Variable is text/string containing Canadian postal codes (FSA format: 1 letter, 1 digit, 1 letter)
# Assumption: code '999' treated as missing (standard missing indicator)
# 39 records have code 999, treated as missing values
df_clean['geo_postal_code'] = df['codep'].map(
    lambda x: x.lower() if x != '999' else None
)
# Convert None to np.nan for consistency
df_clean['geo_postal_code'] = df_clean['geo_postal_code'].where(df_clean['geo_postal_code'].notna(), np.nan)

CODEBOOK_VARIABLES['geo_postal_code'] = {
    'original_variable': 'codep',
    'question_label': 'CODEP. CODE POSTAL',
    'type': 'categorical',
    'value_labels': {},  # Postal codes are individual identifiers, no standardized labels
}
