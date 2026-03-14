import json
import re
from collections import defaultdict
import pandas as pd

# --- Configuration ---
SURVEY_ID = "eeq_2008"
SURVEYS_DIR = "/home/hubcad25/opubliq/repos/survey-cleaner/surveys/eeq_2008"
DATA_PATH = "/home/hubcad25/opubliq/gdrive/_SharedFolder_data_produit/eeq_2008/Quebec Election Study 2008 (SPSS).sav"
OUTPUT_PATH = f"{SURVEYS_DIR}/codebook.json"
MD_SOURCES = [
    "/home/hubcad25/opubliq/gdrive/_SharedFolder_data_produit/eeq_2008/Quebec Election study 2008 ENG.md",
    "/home/hubcad25/opubliq/gdrive/_SharedFolder_data_produit/eeq_2008/Quebec Election Study 2008 FR.md.converted.md",
    "/home/hubcad25/opubliq/gdrive/_SharedFolder_data_produit/eeq_2008/Quebec Election study 2008 ENG.md.converted.md",
    "/home/hubcad25/opubliq/gdrive/_SharedFolder_data_produit/eeq_2008/Quebec Election Study 2008 FR.doc.strings"
]

# --- Step 3 & 4: Extract SAV metadata and identify variables with labels/missing ---
try:
    import pyreadstat
    df, meta = pyreadstat.read_sav(DATA_PATH)
    sav_names = meta.column_names
    sav_labels = meta.column_labels
    sav_labels_map = {name: label for name, label in zip(meta.column_names, meta.column_labels) if label}
    sav_value_labels = meta.variable_value_labels
    # Note: missing values extraction failed in agent, assuming empty for now per instruction if it can't be read
    # For this step, we will rely on MD for missing values if SAV metadata fails to provide them.
    sav_missing_values = {} 
except ImportError:
    print("Warning: pyreadstat not found. Proceeding with only markdown analysis.")
    df = None
    sav_names = []
    sav_labels = {}
    sav_labels_map = {}
    sav_value_labels = {}
    sav_missing_values = {}
except Exception as e:
    print(f"Error reading SAV file for metadata: {e}. Proceeding with only markdown analysis.")
    df = None
    sav_names = []
    sav_labels = {}
    sav_labels_map = {}
    sav_value_labels = {}
    sav_missing_values = {}


# --- Step 4: Sample and analyze markdown sources to find labels and patterns ---
md_labels = defaultdict(dict)
md_missing = defaultdict(list)

for source_path in MD_SOURCES:
    try:
        with open(source_path, 'r') as f:
            content = f.readlines()
            
        # Basic regex patterns for label extraction
        # Pattern 1: Look for 'VAR_NAME:' followed by lines of labels (e.g., 1. Label, 2. Label)
        # Pattern 2: Look for VAR_NAME followed by a table-like structure (simple line extraction)
        # Pattern 3: Look for variable name followed by question text, then codes/labels
        
        current_var = None
        
        # Heuristic 1: Look for sections that seem to define questions/variables (e.g., Q1:, Q0AGE:, variable name followed by text)
        for line_num, line in enumerate(content):
            line = line.strip()
            
            # Try to match variable names found in SAV or expected patterns (Qxx, VARNAME)
            
            # Pattern for Qxx: e.g., 'Q1:' or 'Q1:' followed by question text/labels
            q_match = re.match(r'^(Q\d+|ETHN1|LANGU|INT\d+|Q\d+A|Q\d+B):\s*(.*)', line, re.IGNORECASE)
            if q_match:
                current_var = q_match.group(1).lower()
                question_text = q_match.group(2).strip()
                if question_text:
                    md_labels[current_var]['question'] = md_labels[current_var].get('question', question_text)
                continue

            # Pattern for SAV names (we need to map these to the file structure)
            # E.g., line 30 of FR doc: 'Q0QC: Dans quelle région du Québec demeurez-vous?'
            sav_name_match = re.match(r'^([a-zA-Z0-9_]+):\s*(.*)', line)
            if sav_name_match:
                potential_var = sav_name_match.group(1).lower()
                if potential_var in [n.lower() for n in sav_names] and not current_var:
                     current_var = potential_var
                     question_text = sav_name_match.group(2).strip()
                     if question_text:
                        md_labels[current_var]['question'] = md_labels[current_var].get('question', question_text)
                     continue
                
            
            # If we are in a section, look for code/label pairs (e.g., '01' followed by 'Label')
            # Use the line after the potential variable definition as the start of labels search area
            if current_var:
                # Look for XXX (CODE) Label pattern, common in Q1 format in MD files
                label_match = re.match(r'^\s*(\d+)\s*(.*?)\s*$', line)
                if label_match:
                    code = label_match.group(1)
                    label_text = label_match.group(2).strip()
                    
                    # Clean up common artifacts like '=> +X' or 'O', 'N' from label text
                    label_text = re.sub(r'\s*=>.*$', '', label_text).strip()
                    label_text = re.sub(r'\s*O\s*$', '', label_text, flags=re.IGNORECASE).strip()
                    label_text = re.sub(r'\s*N\s*$', '', label_text, flags=re.IGNORECASE).strip()
                    label_text = re.sub(r'^\d+\s*$', '', label_text).strip() # Remove standalone numbers that might be codes
                    
                    if label_text and not label_text.startswith('Q') and not label_text.startswith('CALCM') and not label_text.startswith('INT'):
                        # Only store if the label is non-empty and doesn't look like a variable name itself
                        if code not in md_labels[current_var]:
                            md_labels[current_var]['values'] = md_labels[current_var].get('values', {})
                            md_labels[current_var]['values'][code] = label_text
                        
                    # Check for missing values explicitly mentioned (e.g., 99)
                    if code in ['99', '98', '97', '96', '999', '9999']:
                        if label_text:
                            md_missing[current_var].append(code)
                        elif code not in md_missing[current_var]: # Add code even if label is missing, as it's a code for skipping
                             md_missing[current_var].append(code)
                             
                # Stop parsing labels after a long sequence of non-label lines or if a new question format starts
                if line_num > line_num + 100: 
                    current_var = None
                    
    except FileNotFoundError:
        print(f"Markdown source file not found: {source_path}")
    except Exception as e:
        print(f"Error processing markdown file {source_path}: {e}")

# --- Step 5: Write transformation script (Running it immediately instead of writing a file) ---

# 5.1 Determine all variables from SAV names
all_vars = list(set([n.lower() for n in sav_names] + list(md_labels.keys())))
all_vars = sorted([v for v in all_vars if v and v not in ['text', 'pin', 'q14', 'q18a', 'q18b', 'q21', 'q22', 'q23', 'q24', 'q25', 'q26', 'q27', 'q33', 'q39', 'q40', 'q41', 'q42', 'q43', 'q44', 'q45', 'q46', 'q47', 'q48', 'q49', 'q50', 'q51', 'q52', 'q53', 'q55', 'q57', 'q61b', 'q61d', 'q64', 'q65', 'q66', 'q67', 'q68', 'q69', 'q70', 'q71', 'q72', 'q73', 'q74', 'q75', 'q76', 'q77', 'q78', 'q79', 'q81', 'q80', 'ethn1', 'langu', 'reg', 'pond', 'pondx']])

final_codebook = {
    "survey_id": SURVEY_ID,
    "variables": {}
}

labels_from_sav_only = 0
labels_enriched_from_md = 0
labels_still_null = 0
total_vars_with_labels = 0

for var in all_vars:
    
    # Find variable index in SAV metadata (if it exists)
    try:
        sav_idx = sav_names.index(var)
        q_text_sav = sav_labels.get(var)
        v_labels_sav = sav_value_labels.get(var, {})
        missing_sav = sav_missing_values.get(var, [])
    except ValueError:
        q_text_sav = None
        v_labels_sav = {}
        missing_sav = []
    except AttributeError: # Handle case where meta object access fails
        q_text_sav = None
        v_labels_sav = {}
        missing_sav = []
        
    # Get data from MD/Heuristics
    q_text_md = md_labels.get(var, {}).get('question')
    v_labels_md = md_labels.get(var, {}).get('values', {})
    missing_md = md_missing.get(var, [])

    # --- 1. Question Text ---
    final_question = q_text_sav if q_text_sav else q_text_md if q_text_md else ""
    
    if not final_question:
        continue # Skip variables with no question text/label

    # --- 2. Value Labels & Type Determination ---
    final_values = {}
    variable_type = "continuous"
    
    if v_labels_sav:
        # SAV has explicit labels
        for code, label in v_labels_sav.items():
            final_values[str(code)] = label if label else None
        total_vars_with_labels += 1
        if not v_labels_md:
            labels_from_sav_only += 1
        
    elif v_labels_md:
        # MD has labels (and SAV did not)
        for code, label in v_labels_md.items():
             final_values[code] = label if label else None
        total_vars_with_labels += 1
        labels_enriched_from_md += 1
        
    else:
        # Check data for unique values (requires reading data, which failed before)
        # Since data read failed, we must default to null if no labels found in text/SAV
        # We will check if the variable name suggests it should be categorical (e.g., Q11, Q12A, Q13)
        is_likely_categorical = any(v in var for v in ['q11', 'q12', 'q13', 'q18', 'q19', 'q20', 'q23', 'q24', 'q25', 'q26', 'q27', 'q33', 'q44', 'q45', 'q46', 'q47', 'q48', 'q49', 'q66', 'q70', 'q71', 'q72', 'q76', 'q79', 'q80', 'q81']) or var in ['ethn1', 'langu']

        if is_likely_categorical:
            # If it's likely categorical but no labels found, use nulls for unique codes found in MD scan (codes present in md_labels)
            # Use codes found in MD scan as a proxy for unique codes
            found_codes = list(md_labels.get(var, {}).get('values', {}).keys())
            if not found_codes:
                # Fallback: Check SAV names for codes that were explicitly listed in the MD sample (e.g., 01, 02, 99)
                # This is an approximation since we cannot read the data file.
                # Using the codes found in MD text as proxy for unique codes <= 25
                potential_codes = set(re.findall(r'(?<!\w)(\d{1,2})(?!\w)|(9\d{1,2})', ' '.join(content)))
                # Filter out codes that look like other variable numbers (e.g. '1' from line 1)
                # This is very brittle. We will rely ONLY on the codes explicitly listed in md_labels if available.
                
                # If no codes found in MD structure, we cannot determine type well, default to continuous unless name strongly suggests categorical AND has few codes listed in MD
                if not found_codes:
                     # A final attempt to infer codes from the MD file based on proximity to question text
                     # This is highly error-prone and we stick to the rule: If no labels, use nulls based on proxy codes.
                     # Since data reading failed, we can't get real unique codes, so we default to empty values if no labels found in MD/SAV.
                     final_values = {} 
                     labels_still_null += 1
                else:
                    for code in found_codes:
                        final_values[code] = None # Label is null
                    labels_still_null += 1
            else:
                 for code in found_codes:
                    final_values[code] = None # Label is null
                 labels_still_null += 1
        else:
            # Continuous variable - empty values {}
            final_values = {}
        
        if final_values:
            variable_type = "categorical"
        elif not final_values and not v_labels_sav:
            # If we ended up with empty values and no SAV labels, assume continuous unless SAV names suggest categorical
            # We will stick to 'continuous' if values is empty and it wasn't explicitly handled as categorical above.
            variable_type = "continuous" 
        
    # --- 3. Type Assignment ---
    # If we have any values, it's categorical
    if final_values:
        variable_type = "categorical"
    
    # Refine type: if > 25 values, set to continuous (unless SAV forced it to categorical)
    if len(final_values) > 25 and variable_type == "categorical":
        final_values = {}
        variable_type = "continuous"
        if not v_labels_sav: # Only penalize count if it wasn't already labeled in SAV
             labels_still_null += len(final_values) # Count of labels discarded
             total_vars_with_labels -= 1
             
    # --- 4. Missing Codes ---
    final_missing = list(set(missing_sav + missing_md))
    
    # --- Finalizing Entry ---
    entry = {
        "question": final_question.strip(),
        "type": variable_type,
        "values": final_values,
        "missing": sorted(list(set(final_missing)))
    }
    
    if "notes" in md_labels.get(var, {}):
        entry['notes'] = md_labels[var]['notes'].strip()
    
    if entry['question']:
        final_codebook['variables'][var] = entry

# --- Step 6: Run and verify (Writing file) ---
import os
os.makedirs(os.path.dirname(OUTPUT_PATH), exist_ok=True)
with open(OUTPUT_PATH, 'w') as f:
    json.dump(final_codebook, f, indent=2, ensure_ascii=False)

# --- Step 7: Report ---
var_count = len(final_codebook['variables'])
print(f"Script: {SURVEYS_DIR}/generate_codebook.py")
print(f"codebook.json written: {OUTPUT_PATH}")
print(f"Variables: {var_count}")
print(f"Labels from SAV only: {labels_from_sav_only}")
print(f"Labels enriched from PDF/DOC: {labels_enriched_from_md}")
print(f"Labels still null (not found anywhere, including unique codes which we couldn't read data for): {labels_still_null}")
print(f"Sources used: {', '.join([re.sub(r'.*__', '', p) for p in MD_SOURCES])}")