#!/usr/bin/env python3
"""
Script d'extraction hybride de codebook: Excel + PDF
-----------------------------------------------------
Stratégie:
1. Parser l'Excel (source principale, 75% des variables)
2. Pour les variables manquantes, extraire du PDF de manière ciblée
3. Générer codebook.json structuré et complet
"""

import pandas as pd
import json
import re
from pathlib import Path
from pypdf import PdfReader
from typing import Dict, List, Optional
import sys


class HybridCodebookExtractor:
    def __init__(self, survey_path: str):
        self.survey_path = Path(survey_path)
        self.raw_path = self.survey_path / "raw"
        self.codebook = {}

    def extract_from_excel(self, excel_file: str) -> Dict[str, dict]:
        """Parse le fichier Excel des codes"""
        print(f"📊 Lecture Excel: {excel_file}")

        df = pd.read_excel(self.raw_path / excel_file)
        df.columns = ['variable', 'value', 'label']

        # Grouper par variable
        codebook = {}
        current_var = None

        for _, row in df.iterrows():
            var = row['variable']

            # Nouvelle variable
            if pd.notna(var) and var != 'Valeur':
                current_var = var
                codebook[current_var] = {
                    'name': current_var,
                    'label': '',  # On cherchera dans le PDF
                    'type': 'categorical',
                    'values': {}
                }

            # Valeur de la variable courante
            elif current_var and pd.notna(row['value']):
                value = str(row['value']).strip()
                label = str(row['label']).strip() if pd.notna(row['label']) else ''

                # Détecter type numérique vs catégorique
                if value.replace('.', '').replace('-', '').isdigit():
                    codebook[current_var]['values'][value] = label
                else:
                    codebook[current_var]['values'][value] = label

        print(f"  ✓ {len(codebook)} variables extraites de l'Excel")
        return codebook

    def get_missing_variables(self, dataset_file: str, codebook: dict) -> List[str]:
        """Identifie les variables manquantes dans le codebook"""
        print(f"🔍 Analyse du dataset: {dataset_file}")

        # Charger dataset
        df = pd.read_csv(self.raw_path / dataset_file, sep=';', encoding='latin-1', nrows=5)

        # Variables manquantes
        missing = sorted(set(df.columns) - set(codebook.keys()))
        print(f"  ❌ {len(missing)} variables non documentées")

        return missing

    def extract_from_pdf_targeted(self, pdf_file: str, missing_vars: List[str]) -> Dict[str, dict]:
        """Extrait les variables manquantes du PDF de manière ciblée"""
        print(f"📄 Extraction ciblée depuis PDF: {pdf_file}")

        pdf_path = self.raw_path / pdf_file
        if not pdf_path.exists():
            print(f"  ⚠️  PDF non trouvé: {pdf_path}")
            return {}

        reader = PdfReader(pdf_path)
        print(f"  📖 {len(reader.pages)} pages à analyser")

        # Patterns pour détecter questions
        var_pattern = re.compile(r'\b(' + '|'.join(re.escape(v) for v in missing_vars) + r')\b')
        question_pattern = re.compile(r'^(Q\d+[A-Z]*(?:M\d+)?(?:O)?)[:\.\s]+(.*?)$', re.MULTILINE)

        found_vars = {}

        # Extraire page par page pour ne pas saturer la mémoire
        for page_num, page in enumerate(reader.pages, 1):
            try:
                text = page.extract_text()

                # Chercher variables manquantes sur cette page
                for var in missing_vars:
                    if var in found_vars:
                        continue

                    if var in text:
                        # Extraire contexte autour de la variable
                        context = self._extract_context(text, var)

                        # Détecter type de question
                        var_type, label = self._infer_variable_info(var, context)

                        found_vars[var] = {
                            'name': var,
                            'label': label,
                            'type': var_type,
                            'values': {},
                            'source': f'PDF page {page_num}'
                        }

                        print(f"  ✓ Trouvé: {var} (page {page_num})")

                # Arrêter si toutes les variables sont trouvées
                if len(found_vars) == len(missing_vars):
                    break

            except Exception as e:
                print(f"  ⚠️  Erreur page {page_num}: {e}")
                continue

        print(f"  ✓ {len(found_vars)}/{len(missing_vars)} variables trouvées dans le PDF")

        # Variables encore manquantes
        still_missing = set(missing_vars) - set(found_vars.keys())
        if still_missing:
            print(f"  ❌ Variables introuvables: {', '.join(sorted(still_missing)[:10])}")

            # Créer entrées par défaut pour variables manquantes
            for var in still_missing:
                found_vars[var] = {
                    'name': var,
                    'label': self._infer_label_from_name(var),
                    'type': 'text' if var.endswith('O') else 'categorical',
                    'values': {},
                    'source': 'inferred'
                }

        return found_vars

    def _extract_context(self, text: str, var: str, window: int = 200) -> str:
        """Extrait contexte autour d'une variable"""
        idx = text.find(var)
        if idx == -1:
            return ""

        start = max(0, idx - window)
        end = min(len(text), idx + len(var) + window)
        return text[start:end]

    def _infer_variable_info(self, var: str, context: str) -> tuple:
        """Déduit le type et label de la variable depuis le contexte"""

        # Variables "O" = texte libre (ouvert)
        if var.endswith('O'):
            label = "Réponse ouverte"
            var_type = "text"

            # Chercher "Précisez" ou "Autre"
            if 'précisez' in context.lower() or 'autre' in context.lower():
                label = "Précisez (réponse ouverte)"

        # Variable de pondération
        elif 'pond' in var.lower():
            label = "Pondération"
            var_type = "numeric"

        # Chercher label dans contexte
        else:
            # Pattern: Q## : Description
            match = re.search(rf'{re.escape(var)}[:\.\s]+(.*?)(?:\n|$)', context)
            if match:
                label = match.group(1).strip()[:200]  # Limiter longueur
            else:
                label = f"Variable {var}"

            var_type = "categorical"

        return var_type, label

    def _infer_label_from_name(self, var: str) -> str:
        """Génère un label par défaut depuis le nom de variable"""
        if var.endswith('O'):
            base_var = var[:-1]
            return f"Précisez la réponse à {base_var} (texte libre)"
        elif 'pond' in var.lower():
            return "Pondération"
        else:
            return f"Variable {var}"

    def merge_and_save(self, excel_codebook: dict, pdf_codebook: dict, output_file: str = "codebook.json"):
        """Fusionne les deux sources et sauvegarde"""
        print(f"\n📦 Fusion et sauvegarde")

        # Merge
        final_codebook = {**excel_codebook, **pdf_codebook}

        print(f"  ✓ Total: {len(final_codebook)} variables")
        print(f"    - Excel: {len(excel_codebook)}")
        print(f"    - PDF: {len(pdf_codebook)}")

        # Sauvegarder
        output_path = self.survey_path / output_file
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(final_codebook, f, ensure_ascii=False, indent=2)

        print(f"  ✓ Sauvegardé: {output_path}")

        # Stats
        types_count = {}
        for var_data in final_codebook.values():
            vtype = var_data.get('type', 'unknown')
            types_count[vtype] = types_count.get(vtype, 0) + 1

        print(f"\n📊 Types de variables:")
        for vtype, count in sorted(types_count.items()):
            print(f"    - {vtype}: {count}")

        return final_codebook


def main():
    if len(sys.argv) < 2:
        print("Usage: python extract_codebook_hybrid.py <survey_name>")
        print("Example: python extract_codebook_hybrid.py elxnqc_particip_egp_2018")
        sys.exit(1)

    survey_name = sys.argv[1]
    survey_path = Path(__file__).parent / survey_name

    if not survey_path.exists():
        print(f"❌ Sondage introuvable: {survey_path}")
        sys.exit(1)

    print(f"🚀 Extraction hybride du codebook: {survey_name}\n")

    extractor = HybridCodebookExtractor(str(survey_path))

    # 1. Extraire depuis Excel
    excel_codebook = extractor.extract_from_excel("Participation ÉGP 2018_Liste des codes.xlsx")

    # 2. Trouver variables manquantes
    missing_vars = extractor.get_missing_variables("Participation ÉGP 2018_Base de données.csv", excel_codebook)

    # 3. Extraire depuis PDF (ciblé)
    pdf_codebook = extractor.extract_from_pdf_targeted("enquete-participation-electorale-EGP2018.pdf", missing_vars)

    # 4. Fusionner et sauvegarder
    final_codebook = extractor.merge_and_save(excel_codebook, pdf_codebook)

    print(f"\n✅ Extraction terminée!")
    print(f"   Fichier généré: {survey_path}/codebook.json")


if __name__ == "__main__":
    main()
