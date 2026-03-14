import json
import re
import pyreadstat

def generate_codebook(survey_id, surveys_dir, shared_folder):
    sav_metadata_path = f"{surveys_dir}/sav_metadata.json"
    markdown_path = f"{surveys_dir}/Quebec_Election_Study_2012_FR.md"
    sav_file_path = f"{shared_folder}/Quebec Election Study 2012 (SPSS).sav"
    output_codebook_path = f"{surveys_dir}/codebook.json"

    # Load SAV metadata
    with open(sav_metadata_path, 'r') as f:
        sav_metadata = json.load(f)

    # Read SAV file for actual data to get unique values for type inference and null labels
    df, _ = pyreadstat.read_sav(sav_file_path, apply_value_formats=False, formats_as_category=False)

    variables = {}

    # Initialize variables from SAV metadata
    for i, col_name in enumerate(sav_metadata['column_names']):
        question_text = sav_metadata['column_labels'][i] if i < len(sav_metadata['column_labels']) else None
        value_labels = sav_metadata['variable_value_labels'].get(col_name, {})

        variables[col_name] = {
            "question": question_text,
            "type": None, # Will infer later
            "values": value_labels,
            "missing": [] # Not explicitly available in SAV metadata, will try to infer from markdown
        }

    # Parse Markdown for question text and value labels
    with open(markdown_path, 'r') as f:
        markdown_content = f.read()

    # Regex to find Q<number>: Question text and then indented list of labels
    # This regex is an improvement over previous versions, trying to be more robust
    variable_blocks = re.findall(r'(Q\d+):\s*(.*?)\n(\s*(?:-\s*.*|\d+\.\s*.*|\(INVERSER[^)]*\)\s*\n)?(?:(?:\s*-\s*.*|\s*\d+\.\s*.*|\s*.)(?:(?!\n\n)\n|$))*)\n\n', markdown_content, re.DOTALL)

    for match in re.finditer(r'(Q\d+):\s*(.*?)(?=\n\n(?:Q\d+:|\Z)|\n(?!\s*(?:-|Très|Plutôt|Pas|Également|Uniquement|Langue|Religion|Culture|Valeurs|Histoire|Il n’y a pas de différence importante entre les deux groupes|Très importante|Plutôt importante|Pas très importante|Pas du tout importante|Ne sais pas|Pas de réponse)))((?:\n\s*(?:-\s*.*|\d+\.\s*.*|\(INVERSER[^)]*\)|(?:[A-Z][a-zà-ú]*)(?:\s*-[a-zà-ú]*)?|\s*\S.*))+)', markdown_content, re.DOTALL):
        q_name_match = match.group(1)
        question_text_md = match.group(2).strip()
        labels_block = match.group(3)

        # Heuristic to map Q<number> to SAV variable names.
        # This is a weak link, ideally we'd have a direct mapping or a consistent naming convention.
        # For now, we'll try to match based on question text similarity or simple enumeration.
        # This is a very rough approach and needs manual verification.
        # A better approach would be to find the variable name in the markdown near the question.

        # Let's try to find a variable by matching the question text (partial match)
        # This will need to be improved if there isn't a clear mapping.
        matching_sav_var = None
        for sav_var, sav_data in variables.items():
            if sav_data['question'] and question_text_md.lower() in sav_data['question'].lower():
                matching_sav_var = sav_var
                break

        if not matching_sav_var:
            # Fallback: try to find a variable that hasn't had its question text set from SAV
            # or is currently null
            for sav_var, sav_data in variables.items():
                if not sav_data['question']:
                    matching_sav_var = sav_var
                    break

        if matching_sav_var and variables[matching_sav_var]['question'] is None:
            variables[matching_sav_var]['question'] = question_text_md
        
        # Extract labels from markdown
        md_labels = {}
        
        # Regex for common list formats: - Label, 1. Label, or just indented text
        label_lines = [line.strip() for line in labels_block.split('\\n') if line.strip() and not line.strip().startswith('(INVERSER')]
        
        # If the block contains "Ne sais pas" or "Pas de réponse", these are likely missing values
        notes = []
        inverser_match = re.search(r'\\(INVERSER[^)]*\\)', labels_block)
        if inverser_match:
            notes.append(inverser_match.group(0))

        label_code = 1
        for line in label_lines:
            line = line.replace('-', '').strip() # Remove bullet points
            # Try to match patterns like "1. Label" or just "Label"
            match_num_label = re.match(r'(\d+)\.\s*(.*)', line)
            if match_num_label:
                code = match_num_label.group(1)
                label = match_num_label.group(2).strip()
                if label.lower() == 'ne sais pas' or label.lower() == 'pas de réponse':
                    if code not in variables[matching_sav_var]['missing']:
                        variables[matching_sav_var]['missing'].append(code)
                else:
                    md_labels[code] = label
            elif line: # If it's just a label without a number
                # This is a heuristic, assuming a sequential numbering if not explicit
                # And only if the SAV didn't provide labels for this variable
                if matching_sav_var and not variables[matching_sav_var]['values']:
                    if line.lower() == 'ne sais pas' or line.lower() == 'pas de réponse':
                        # We don't have a code, so we can't add to missing for now
                        pass
                    else:
                        md_labels[str(label_code)] = line
                        label_code += 1

        if matching_sav_var:
            # If SAV had no labels, use markdown labels
            if not variables[matching_sav_var]['values'] and md_labels:
                variables[matching_sav_var]['values'] = md_labels
            # If markdown has "Ne sais pas" or "Pas de réponse" and SAV does not, consider them missing
            if notes and 'notes' not in variables[matching_sav_var]:
                variables[matching_sav_var]['notes'] = "\\n".join(notes)
            elif notes and 'notes' in variables[matching_sav_var]:
                variables[matching_sav_var]['notes'] += "\\n" + "\\n".join(notes)


    # Final pass to infer types and fill in null labels
    for col_name, var_data in variables.items():
        # Get unique values from the dataframe for this column
        if col_name in df.columns:
            unique_values = df[col_name].dropna().unique()

            # Infer type
            if len(var_data['values']) > 0 or len(unique_values) <= 25:
                var_data['type'] = "categorical"
            elif df[col_name].dtype in ['int64', 'float64']:
                var_data['type'] = "continuous"
            else:
                var_data['type'] = "text" # Fallback for strings or other types

            # Fill in null labels for categorical variables if not found
            if var_data['type'] == 'categorical' and not var_data['values']:
                for val in unique_values:
                    if str(val) not in var_data['values']:
                        var_data['values'][str(val)] = None
            
            # If a variable has value labels from SAV and it's missing in markdown,
            # but is present in markdown as a question, we should try to add "notes" from markdown
            # This is a very rough heuristic
            if var_data['type'] == 'categorical' and var_data['values'] and 'notes' not in var_data:
                 for match in re.finditer(r'(Q\d+):\s*(.*?)(?=\n\n(?:Q\d+:|\Z)|\n(?!\s*(?:-|Très|Plutôt|Pas|Également|Uniquement|Langue|Religion|Culture|Valeurs|Histoire|Il n’y a pas de différence importante entre les deux groupes|Très importante|Plutôt importante|Pas très importante|Pas du tout importante|Ne sais pas|Pas de réponse)))((?:\n\s*(?:-\s*.*|\d+\.\s*.*|\(INVERSER[^)]*\)|(?:[A-Z][a-zà-ú]*)(?:\s*-[a-zà-ú]*)?|\s*\S.*))+)', markdown_content, re.DOTALL):
                    question_text_md = match.group(2).strip()
                    labels_block = match.group(3)
                    if var_data['question'] and question_text_md.lower() in var_data['question'].lower():
                        notes = []
                        inverser_match = re.search(r'\\(INVERSER[^)]*\\)', labels_block)
                        if inverser_match:
                            notes.append(inverser_match.group(0))
                        if notes:
                            var_data['notes'] = "\\n".join(notes)
                        break


        # Remove notes if empty
        if 'notes' in var_data and not var_data['notes']:
            del var_data['notes']

        # Ensure question is never None, set to "" if null
        if var_data['question'] is None:
            var_data['question'] = ""
        
        # Remove variables with no question and no values
        if not var_data['question'] and not var_data['values'] and not var_data['missing']:
            del variables[col_name]

    # Filter out variables that have no question text and no values (empty)
    final_variables = {k: v for k, v in variables.items() if v['question'] or v['values'] or v['missing']}


    codebook = {
        "survey_id": survey_id,
        "variables": final_variables
    }

    with open(output_codebook_path, 'w') as f:
        json.dump(codebook, f, indent=4, ensure_ascii=False)

    print(f"Codebook written to {output_codebook_path}")

if __name__ == '__main__':
    survey_id = "eeq_2012"
    shared_folder = "/home/hubcad25/opubliq/gdrive/_SharedFolder_data_produit/eeq_2012"
    surveys_dir = "/home/hubcad25/opubliq/repos/survey-cleaner/surveys/eeq_2012"
    generate_codebook(survey_id, surveys_dir, shared_folder)
