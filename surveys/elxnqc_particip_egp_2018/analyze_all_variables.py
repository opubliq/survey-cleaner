#!/usr/bin/env python3
"""
Analyse toutes les variables du sondage pour faciliter le nettoyage manuel

Génère un rapport avec:
- Type de variable (numeric/categorical/text)
- Distribution des valeurs
- Valeurs manquantes
- Suggestions de nettoyage
"""

import pandas as pd
import numpy as np
from pathlib import Path

# Paths
RAW_DIR = Path(__file__).parent / "raw"
data_file = RAW_DIR / "data.csv"

# Load data
print("Chargement des données...")
df = pd.read_csv(data_file, encoding='latin-1', sep=';')
print(f"Dataset: {len(df)} observations × {len(df.columns)} variables\n")

# Variables déjà nettoyées (à skip) - au début, liste vide
cleaned_vars = []

# Variables techniques à skip - à identifier
technical_vars = []

skip_vars = set(cleaned_vars + technical_vars)

# Analyze each variable
report = []
report.append("="*80)
report.append("RAPPORT D'ANALYSE DES VARIABLES - elxnqc_particip_egp_2018")
report.append("="*80)
report.append("")

for col in df.columns:
    if col in skip_vars:
        continue

    report.append("-"*80)
    report.append(f"VARIABLE: {col}")
    report.append("-"*80)

    # Basic info
    dtype = df[col].dtype
    n_unique = df[col].nunique()
    n_missing = df[col].isna().sum()
    pct_missing = (n_missing / len(df)) * 100

    report.append(f"Type: {dtype}")
    report.append(f"Valeurs uniques: {n_unique}")
    report.append(f"Valeurs manquantes: {n_missing} ({pct_missing:.1f}%)")
    report.append("")

    # Determine variable type and suggest cleaning
    is_numeric = pd.api.types.is_numeric_dtype(dtype)

    # Binary (2 unique values)
    if n_unique == 2 and is_numeric:
        report.append("TYPE DÉTECTÉ: Binaire (oui/non)")
        report.append("SUGGESTION: Mapper 1.0→1.0, 2.0→0.0 (ou yes/no en texte)")
        report.append("")
        report.append("Distribution:")
        counts = df[col].value_counts(dropna=False).sort_index()
        for val, count in counts.items():
            pct = (count / len(df)) * 100
            report.append(f"  {val}: {count} ({pct:.1f}%)")

    # Categorical (3-20 unique values)
    elif 3 <= n_unique <= 20 and is_numeric:
        report.append("TYPE DÉTECTÉ: Catégorielle ordinale ou nominale")
        report.append("SUGGESTION: Utiliser .map() avec labels descriptifs")
        report.append("")
        report.append("Distribution:")
        counts = df[col].value_counts(dropna=False).sort_index()
        for val, count in counts.items():
            pct = (count / len(df)) * 100
            report.append(f"  {val}: {count} ({pct:.1f}%)")

    # Many categories (>20) - possibly continuous or many-valued categorical
    elif n_unique > 20 and is_numeric:
        report.append("TYPE DÉTECTÉ: Continue ou multi-catégorielle")
        report.append("SUGGESTION: Vérifier si continue (créer bins) ou catégorielle (mapper)")
        report.append("")
        report.append("Statistiques descriptives:")
        stats = df[col].describe()
        for stat_name, stat_val in stats.items():
            report.append(f"  {stat_name}: {stat_val:.2f}")
        report.append("")
        report.append("Premiers exemples de valeurs:")
        sample_vals = df[col].dropna().unique()[:10]
        report.append(f"  {list(sample_vals)}")

    # Text/object
    elif dtype == 'object' or not is_numeric:
        report.append("TYPE DÉTECTÉ: Texte/Objet")
        if n_unique <= 20:
            report.append("SUGGESTION: Catégorielle textuelle - mapper vers valeurs standardisées")
            report.append("")
            report.append("Distribution:")
            counts = df[col].value_counts(dropna=False)
            for val, count in counts.head(20).items():
                pct = (count / len(df)) * 100
                val_str = str(val)[:50]  # Truncate long strings
                report.append(f"  '{val_str}': {count} ({pct:.1f}%)")
        else:
            report.append("SUGGESTION: Texte libre (open-ended) - conserver tel quel ou SKIP si PII")
            report.append("")
            report.append("Exemples (premiers 5):")
            samples = df[col].dropna().head(5)
            for i, val in enumerate(samples, 1):
                val_str = str(val)[:80]
                report.append(f"  {i}. {val_str}")

    # Single value (constant)
    elif n_unique == 1:
        report.append("TYPE DÉTECTÉ: Constante (une seule valeur)")
        report.append("SUGGESTION: SKIP - pas de variabilité")
        report.append(f"Valeur unique: {df[col].dropna().iloc[0] if not df[col].dropna().empty else 'NaN'}")

    report.append("")

# Save report
report_text = "\n".join(report)
report_file = Path(__file__).parent / "VARIABLES_ANALYSIS_REPORT.txt"
report_file.write_text(report_text, encoding='utf-8')

print(f"\n✓ Rapport généré: {report_file}")
print(f"\nVariables analysées: {len(df.columns) - len(skip_vars)}")
print(f"Variables skippées: {len(skip_vars)}")
print(f"\nConsulte {report_file.name} pour les détails !")
