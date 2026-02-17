import pandas as pd

df = pd.read_excel('/home/hubcad25/opubliq/repos/survey-cleaner/_SharedFolder_data_produit/elxnqc_particip_egm_2021/Participation ÉGM 2021_Base de données.xlsx', sheet_name=1)

with open('/home/hubcad25/opubliq/repos/survey-cleaner/_SharedFolder_data_produit/elxnqc_particip_egm_2021/codebook.md', 'w') as f:
    for index, row in df.iterrows():
        variable_name = row['caseid']
        question_text = row['Numéro de questionnaire']
        f.write(f'### {variable_name}\n\n')
        f.write(f'**Question**: {question_text}\n\n')
        f.write('**Type**: categorical\n\n')
        f.write('**Choix de réponse**: \n')
        # Add answer choices here if available in the data
        f.write('\n**Notes**: \n\n')
        f.write('---\n\n')
