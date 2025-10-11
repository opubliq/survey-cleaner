#!/usr/bin/env python3
"""
Extract data and codebook from multi-sheet Excel files

Usage:
    python extract_excel_sheets.py <excel_file> <survey_name>

Example:
    python extract_excel_sheets.py "data.xlsx" elxnqc_particip_egm_2021
"""

import sys
import pandas as pd
from pathlib import Path

def extract_excel_sheets(excel_path: str, survey_name: str):
    """Extract sheets from Excel file to survey raw/ directory

    Assumes:
    - First sheet = data
    - Second sheet = codebook
    """
    excel_file = Path(excel_path)

    if not excel_file.exists():
        print(f"Error: File not found: {excel_file}")
        sys.exit(1)

    print(f"Reading Excel file: {excel_file.name}")

    # Read Excel file
    xl = pd.ExcelFile(excel_file)

    print(f"Found {len(xl.sheet_names)} sheets: {xl.sheet_names}")

    # Setup survey directory
    survey_dir = Path(f"surveys/{survey_name}")
    raw_dir = survey_dir / "raw"
    raw_dir.mkdir(parents=True, exist_ok=True)

    # Extract first sheet as data (CSV)
    if len(xl.sheet_names) >= 1:
        data_sheet = xl.sheet_names[0]
        print(f"\nExtracting data sheet: '{data_sheet}'")
        df_data = pd.read_excel(excel_file, sheet_name=data_sheet)

        # Save as CSV
        data_csv = raw_dir / "data.csv"
        df_data.to_csv(data_csv, index=False, encoding='utf-8')
        print(f"  → Saved to: {data_csv}")
        print(f"  → Rows: {len(df_data)}, Columns: {len(df_data.columns)}")

    # Extract second sheet as codebook (text)
    if len(xl.sheet_names) >= 2:
        codebook_sheet = xl.sheet_names[1]
        print(f"\nExtracting codebook sheet: '{codebook_sheet}'")
        df_codebook = pd.read_excel(excel_file, sheet_name=codebook_sheet)

        # Save as markdown
        codebook_md = raw_dir / "codebook.md"

        # Convert to markdown table
        with open(codebook_md, 'w', encoding='utf-8') as f:
            f.write(f"# Codebook: {survey_name}\n\n")
            f.write(f"Source: {excel_file.name} (sheet: {codebook_sheet})\n\n")

            # Write as markdown table
            f.write(df_codebook.to_markdown(index=False))
            f.write("\n")

        print(f"  → Saved to: {codebook_md}")
        print(f"  → Rows: {len(df_codebook)}")

    print(f"\n✓ Extraction complete!")
    print(f"\nNext steps:")
    print(f"  1. Review files in surveys/{survey_name}/raw/")
    print(f"  2. Run: ./surveys/run_cleaner.sh {survey_name}")


if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python extract_excel_sheets.py <excel_file> <survey_name>")
        print("\nExample:")
        print('  python extract_excel_sheets.py "_SharedFolder_data_produit/elxnqc_particip_egm_2021/data.xlsx" elxnqc_particip_egm_2021')
        sys.exit(1)

    excel_path = sys.argv[1]
    survey_name = sys.argv[2]

    extract_excel_sheets(excel_path, survey_name)
