import json
import re
import pyreadstat
import pandas as pd

def parse_pdf_codebook(pdf_text_path):
    variables = {}
    with open(pdf_text_path, 'r', encoding='utf-8') as f:
        content = f.read()

    variable_blocks = re.split(r'={79,}', content)

    for block in variable_blocks:
        if not block.strip():
            continue

        var_name = None
        question = ''

        # Try to find variable name and question like VAR_NAME ’Question text’
        match_var_question = re.match(r'\n*(\w+)\s+\’([^\’]+(?:\’\n[^\’]+)*)\’', block)
        if match_var_question:
            var_name = match_var_question.group(1).strip()
            question = match_var_question.group(2).replace('\n', ' ').strip()
            # Heuristic to filter out technical descriptions that are not true questions
            if var_name == "QUEST" and "/ COUNT" in question: # Specific for QUEST
                question = ''
            elif var_name == "SDAT": # SDAT also seems to lack a proper question
                question = ''
            elif question == var_name: # If question is just the var_name, it's not a real question
                question = ''
        else:
            # Try to find variable name only (e.g., for QUEST, SDAT, COUNT where question is missing)
            match_var_only = re.match(r'\n*(\w+)\s*', block)
            if match_var_only:
                var_name = match_var_only.group(1).strip()
                question = '' # No direct question found in this pattern
            else:
                continue # Skip blocks that don't match any variable pattern

        if not var_name:
            continue

        current_var = {
            "question": question,
            "type": "unknown",
            "values": {},
            "missing": []
        }

        storage_mode_match = re.search(r'Storage mode:\s*(\w+)', block)
        if storage_mode_match:
            current_var['storage_mode'] = storage_mode_match.group(1).strip()

        min_match = re.search(r'Min:\s*([-+]?\d*\.?\d+(?:[eE][-+]?\d+)?)', block)
        max_match = re.search(r'Max:\s*([-+]?\d*\.?\d+(?:[eE][-+]?\d+)?)', block)
        if min_match and max_match and 'Values and labels' not in block:
            current_var['type'] = 'continuous'

        values_labels_section = re.search(r'Values and labels\s*(.*?)(?=\n={79,}|\n*N Percent|\n*Valid and missing values|$)', block, re.DOTALL)
        if values_labels_section:
            values_text = values_labels_section.group(1)
            for line in values_text.split('\n'):
                line = line.strip()
                if not line:
                    continue
                match_value_label = re.match(r'(\S+)\s+\’([^\’]+)\’', line)
                if match_value_label:
                    code = match_value_label.group(1).strip()
                    label = match_value_label.group(2).strip()
                    try:
                        current_var['values'][str(float(code))] = label
                    except ValueError:
                        current_var['values'][code] = label
                    current_var['type'] = 'categorical'

        missing_match = re.search(r'(NA M|\(unlab\.val\.\))', block)
        if missing_match:
            current_var['missing'].append(missing_match.group(1).strip())

        variables[var_name] = current_var
    return variables

def enrich_with_sav_metadata(variables, sav_path):
    try:
        df, meta = pyreadstat.read_sav(sav_path, apply_value_formats=True)
    except Exception as e:
        print(f"Error reading SAV file: {e}")
        return variables

    for var_name_sav in meta.column_names:
        var_name_key = var_name_sav

        if var_name_key not in variables:
            variables[var_name_key] = {
                "question": "",
                "type": "unknown",
                "values": {},
                "missing": []
            }

        # Get question from SAV (prioritize SAV if it's a real question)
        sav_question = meta.variable_to_label.get(var_name_sav)
        if sav_question and not re.match(r'labels\d+', sav_question): # Exclude internal SPSS labels
            variables[var_name_key]['question'] = sav_question.strip()
        # If SAV question is an internal label or missing, keep what PDF parsed or an empty string

        # Get value labels from SAV (prioritize SAV)
        if var_name_sav in meta.column_labels and meta.column_labels[var_name_sav] in meta.value_labels:
            sav_labels = meta.value_labels[meta.column_labels[var_name_sav]]
            variables[var_name_key]['values'] = {str(k).replace('.0', ''): v for k, v in sav_labels.items()}
            variables[var_name_key]['type'] = 'categorical'

        # If no values from PDF or SAV and it's a numeric type, check for continuous
        if not variables[var_name_key]['values'] and (
            variables[var_name_key].get('storage_mode') == 'double' or 
            (var_name_sav in df.columns and pd.api.types.is_numeric_dtype(df[var_name_sav]))
        ):
            if var_name_sav in df.columns and not df[var_name_sav].isnull().all():
                unique_values = df[var_name_sav].dropna().unique()
                if len(unique_values) > 30: # Heuristic for continuous
                    variables[var_name_key]['type'] = 'continuous'
                elif len(unique_values) > 0: # If there are unique values, but not too many, assume categorical
                    if not variables[var_name_key]['values']:
                        variables[var_name_key]['values'] = {str(int(code)) if isinstance(code, float) and code.is_integer() else str(code): None for code in unique_values if not pd.isna(code)}
                        variables[var_name_key]['type'] = 'categorical'
            elif variables[var_name_key]['type'] == "unknown": # If it's numeric but all null, default to continuous
                variables[var_name_key]['type'] = 'continuous' # Default for unknown numeric with no data

        # Determine type for character variables
        if variables[var_name_key].get('storage_mode') == 'character' or (var_name_sav in df.columns and pd.api.types.is_string_dtype(df[var_name_sav])):
            if not variables[var_name_key]['values']: # If no value labels, it's text
                variables[var_name_key]['type'] = 'text'
            else:
                variables[var_name_key]['type'] = 'categorical'

        # If type is still unknown, default to text
        if variables[var_name_key]['type'] == 'unknown':
            variables[var_name_key]['type'] = 'text'

        if 'storage_mode' in variables[var_name_key]:
            del variables[var_name_key]['storage_mode']

    return variables

def generate_codebook(survey_id, shared_folder, surveys_dir):
    pdf_text_path = f"/tmp/codebook.txt"
    sav_path = f"{shared_folder}/Fichier SPSS - Étude sur la santé - Canada-USA.Sav"
    output_path = f"{shared_folder}/codebook.json"

    parsed_pdf_vars = parse_pdf_codebook(pdf_text_path)

    final_variables = enrich_with_sav_metadata(parsed_pdf_vars, sav_path)

    # Ensure all questions are strings, replace None with empty string
    for var_name, var_data in final_variables.items():
        if var_data['question'] is None:
            var_data['question'] = ''
        # Also handle potential float keys for categorical variables, converting them to int if they are integers
        new_values = {}
        for k, v in var_data['values'].items():
            try:
                # If a float key is actually an integer (e.g., "1.0"), convert to "1"
                if isinstance(k, str) and '.' in k:
                    float_k = float(k)
                    if float_k == int(float_k):
                        new_values[str(int(float_k))] = v
                    else:
                        new_values[k] = v
                else:
                    new_values[k] = v
            except ValueError:
                new_values[k] = v
        var_data['values'] = new_values


    codebook_data = {
        "survey_id": survey_id,
        "variables": final_variables
    }

    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(codebook_data, f, ensure_ascii=False, indent=2)

    return len(final_variables), output_path

if __name__ == "__main__":
    survey_id = "cecd_sante_can_usa"
    shared_folder = "/home/hubcad25/opubliq/gdrive/_SharedFolder_data_produit/cecd_sante_can_usa"
    surveys_dir = "/home/hubcad25/opubliq/repos/survey-cleaner/surveys/cecd_sante_can_usa"
    count, path = generate_codebook(survey_id, shared_folder, surveys_dir)
    print(f"Variables: {count}, Output: {path}")
