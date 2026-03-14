# op_vote_intention_q75 — Placeholder for question 75 (no codebook)
# Source: q75
# Assumption: Codes observed in data are mapped to generic labels as no codebook was provided.
# Assumption: Code 99.0 is treated as missing based on general pipeline context.
df_clean['op_vote_intention_q75'] = df['q75'].map({
    1922.0: 'code_1922',
    1926.0: 'code_1926',
    1928.0: 'code_1928',
    1929.0: 'code_1929',
    1930.0: 'code_1930',
    1931.0: 'code_1931',
    1932.0: 'code_1932',
    1933.0: 'code_1933',
    1934.0: 'code_1934',
    1935.0: 'code_1935',
    1936.0: 'code_1936',
    1937.0: 'code_1937',
    1938.0: 'code_1938',
    1939.0: 'code_1939',
    1940.0: 'code_1940',
    1941.0: 'code_1941',
    1942.0: 'code_1942',
    1943.0: 'code_1943',
    1944.0: 'code_1944',
    1945.0: 'code_1945',
    1946.0: 'code_1946',
    1947.0: 'code_1947',
    1948.0: 'code_1948',
    1949.0: 'code_1949',
    1950.0: 'code_1950',
    99.0: np.nan,
})
CODEBOOK_VARIABLES['op_vote_intention_q75'] = {
    'original_variable': 'q75',
    'question_label': "Question 75 - Content Unknown",
    'type': 'categorical',
    'value_labels': {'code_1922': "Code 1922 Unknown", 'code_1926': "Code 1926 Unknown", 'code_1928': "Code 1928 Unknown", 'code_1929': "Code 1929 Unknown", 'code_1930': "Code 1930 Unknown", 'code_1931': "Code 1931 Unknown", 'code_1932': "Code 1932 Unknown", 'code_1933': "Code 1933 Unknown", 'code_1934': "Code 1934 Unknown", 'code_1935': "Code 1935 Unknown", 'code_1936': "Code 1936 Unknown", 'code_1937': "Code 1937 Unknown", 'code_1938': "Code 1938 Unknown", 'code_1939': "Code 1939 Unknown", 'code_1940': "Code 1940 Unknown", 'code_1941': "Code 1941 Unknown", 'code_1942': "Code 1942 Unknown", 'code_1943': "Code 1943 Unknown", 'code_1944': "Code 1944 Unknown", 'code_1945': "Code 1945 Unknown", 'code_1946': "Code 1946 Unknown", 'code_1947': "Code 1947 Unknown", 'code_1948': "Code 1948 Unknown", 'code_1949': "Code 1949 Unknown", 'code_1950': "Code 1950 Unknown"},
}