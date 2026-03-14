#!/usr/bin/env python3
"""
Generate codebook.json for eeq_2007 by merging SAV metadata with markdown codebook.

Strategy:
1. Load SAV metadata: variable names, labels (questions), and value labels
2. Load markdown codebook and extract code→label mappings
3. For each variable:
   - Use SAV question text if available
   - Use SAV value labels if they exist
   - If SAV has no labels but variable is categorical, search markdown
   - If no labels found anywhere, leave values as {}
4. Write codebook.json
"""

import json
import re
from pathlib import Path
import pyreadstat

# Paths
SAV_FILE = Path("/home/hubcad25/opubliq/repos/survey-cleaner/_SharedFolder_data_produit/eeq_2007/Quebec Election Study 2007 (SPSS).sav")
MD_FILE = Path("/tmp/eeq_2007_fr_codebook.md")
OUTPUT_DIR = Path("/home/hubcad25/opubliq/repos/survey-cleaner/surveys/eeq_2007")
OUTPUT_FILE = OUTPUT_DIR / "codebook.json"

def load_sav_metadata():
    """Load variable names, labels, and value labels from SAV file."""
    df, meta = pyreadstat.read_sav(str(SAV_FILE))
    
    return {
        'column_names': list(meta.column_names),
        'column_labels': list(meta.column_labels),
        'variable_value_labels': meta.variable_value_labels,
        'df': df
    }

def load_markdown():
    """Parse markdown file to extract variable definitions and value labels."""
    with open(MD_FILE, 'r', encoding='utf-8', errors='ignore') as f:
        content = f.read()
    return content

def parse_markdown_for_variable(var_name, md_content):
    """
    Extract question text and value labels for a specific variable from markdown.
    
    Pattern:
    VARNAME:
    Question text...
    Code1    Label
    Code2    Label
    ...
    """
    # Create regex to find the variable block
    # Match: VAR_NAME: ... until next variable or EOF
    pattern = rf'^{re.escape(var_name.upper())}:\s*\n(.*?)(?=^[A-Z][A-Z0-9]*:\s*\n|\Z)'
    match = re.search(pattern, md_content, re.MULTILINE | re.IGNORECASE | re.DOTALL)
    
    if not match:
        return None, {}
    
    block = match.group(1)
    lines = block.strip().split('\n')
    
    # First non-empty line is usually the question
    question = None
    value_labels = {}
    
    i = 0
    for line in lines:
        line = line.strip()
        if not line:
            continue
        
        # If we haven't found the question yet, this is it
        if question is None:
            question = line
            i += 1
            break
        i += 1
    
    # Now parse value labels (code + label pairs)
    # Format: "Label    Code" or "Code    Label" or similar
    for line in lines[i:]:
        line = line.strip()
        if not line or line.startswith('=>'):
            continue
        
        # Try to split: look for multiple spaces or tabs
        # The pattern is usually: "Text description    CODE" or "CODE    Text"
        # We need to find where the code is (usually numeric or short like '1', '01', '8', etc.)
        
        parts = re.split(r'\s{2,}|\t+', line)  # Split on 2+ spaces or tabs
        if len(parts) >= 2:
            # Check which end is the code
            potential_code = parts[-1].strip()
            potential_label = ' '.join(parts[:-1]).strip()
            
            # If last part looks like a code (digits, short), it's likely: Label CODE
            if re.match(r'^[0-9]+[A-Z]?$|^[A-Z]+$', potential_code) and potential_label:
                value_labels[potential_code] = potential_label
            else:
                # Try first part as code
                potential_code = parts[0].strip()
                potential_label = ' '.join(parts[1:]).strip()
                if re.match(r'^[0-9]+$|^[0-9]+[A-Z]?$', potential_code) and potential_label:
                    value_labels[potential_code] = potential_label
    
    return question, value_labels

def get_unique_values(df, var_name):
    """Get unique non-null values from a column, sorted."""
    if var_name not in df.columns:
        return []
    col = df[var_name].dropna()
    unique = sorted(col.unique())
    return unique

def infer_type(var_name, unique_values, has_labels):
    """Infer variable type based on unique values and labels."""
    if not unique_values:
        return "text"
    
    # If has labels or few unique values, it's categorical
    if has_labels or len(unique_values) <= 25:
        return "categorical"
    
    # If numeric with many values, continuous
    try:
        for v in unique_values:
            float(v)
        return "continuous"
    except (ValueError, TypeError):
        return "text"

def build_codebook(sav_meta, md_content):
    """Build codebook by merging SAV and Markdown sources."""
    
    codebook = {
        "survey_id": "eeq_2007",
        "variables": {}
    }
    
    var_names = sav_meta['column_names']
    col_labels = sav_meta['column_labels']
    var_value_labels = sav_meta['variable_value_labels']
    df = sav_meta['df']
    
    labels_from_sav = 0
    labels_from_md = 0
    labels_null = 0
    
    for i, var_name in enumerate(var_names):
        # Get question text from SAV column_labels (indexed by position)
        question = col_labels[i] if i < len(col_labels) else ""
        
        # If not in SAV or empty, try markdown
        if not question:
            question, _ = parse_markdown_for_variable(var_name, md_content)
        
        # Skip if no question text found
        if not question:
            continue
        
        # Determine value labels: SAV first, then markdown
        values = {}
        labels_source = None
        
        # Check if SAV has value labels for this variable
        sav_labels = var_value_labels.get(var_name, {})
        
        if sav_labels:
            # Use SAV labels directly
            values = dict(sav_labels)
            labels_source = "sav"
            labels_from_sav += 1
        else:
            # Try to get labels from markdown
            _, md_labels = parse_markdown_for_variable(var_name, md_content)
            
            if md_labels:
                values = md_labels
                labels_source = "markdown"
                labels_from_md += 1
            else:
                # No labels found anywhere; try to infer from unique data values
                unique_vals = get_unique_values(df, var_name)
                if unique_vals and len(unique_vals) <= 25:
                    # Create null-valued entries for categorical
                    values = {str(v): None for v in unique_vals}
                    labels_source = "data_inferred"
                    labels_null += 1
                else:
                    labels_null += 1
        
        # Infer type
        var_type = infer_type(var_name, get_unique_values(df, var_name), bool(values))
        
        # Build variable entry
        var_entry = {
            "question": question,
            "type": var_type,
            "values": values
        }
        
        # Add notes if skip patterns exist (simplified check)
        notes = ""
        if "=>" in question:
            notes = "Contains skip patterns (see raw codebook)"
        
        if notes:
            var_entry["notes"] = notes
        
        codebook["variables"][var_name] = var_entry
    
    return codebook, labels_from_sav, labels_from_md, labels_null

def main():
    print("Loading SAV metadata...")
    sav_meta = load_sav_metadata()
    
    print("Loading Markdown documentation...")
    md_content = load_markdown()
    
    print("Building codebook...")
    codebook, lfs, lfm, lnull = build_codebook(sav_meta, md_content)
    
    print(f"  Variables with labels from SAV: {lfs}")
    print(f"  Variables with labels from Markdown: {lfm}")
    print(f"  Variables with null/inferred labels: {lnull}")
    print(f"  Total variables: {len(codebook['variables'])}")
    
    # Write output
    output_path = Path(OUTPUT_FILE)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(codebook, f, indent=2, ensure_ascii=False)
    
    print(f"\nWrote: {output_path}")
    
    # Verify by reading first few variables
    print("\n=== SAMPLE (first 3 variables) ===")
    for i, (var_name, var_data) in enumerate(list(codebook['variables'].items())[:3]):
        print(f"\n{var_name}:")
        print(f"  Question: {var_data['question'][:80]}")
        print(f"  Type: {var_data['type']}")
        print(f"  Values: {list(var_data['values'].items())[:3]}")

if __name__ == '__main__':
    main()
