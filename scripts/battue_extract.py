#!/usr/bin/env python3
"""
Battue : script d'extraction 100 variables + JSON pour analyse pattern.

Découvre tous les sondages directement dans _SharedFolder_data_produit/,
échantillonne ~100 variables de façon stratifiée, fait tourner le
pattern_classifier sur chacune, et exporte un JSON riche prêt pour analyse.

Output JSON inclut pour chaque variable :
  - Classification complète (tier, pattern_id, confidence, all_confidences)
  - Reason string (diagnostic de la classification)
  - Missing codes détectés (codes + meanings)
  - Value distribution (top 20 valeurs)
  - Metadata (var_label, n_unique)

Usage:
    python scripts/battue_extract.py
    python scripts/battue_extract.py --n 100 --seed 42 --output data/battue_100vars.json
    python scripts/battue_extract.py --surveys eeq_2022 govcan_2022
"""

from __future__ import annotations

import argparse
import json
import logging
import sys
import warnings
from pathlib import Path
from typing import Optional

import pandas as pd

warnings.filterwarnings("ignore", category=RuntimeWarning)
for _noisy in ("LiteLLM", "litellm", "httpx", "pyreadstat"):
    logging.getLogger(_noisy).setLevel(logging.CRITICAL)

ROOT = Path(__file__).parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

DATA_DIR = ROOT / "_SharedFolder_data_produit"
OUTPUT_DEFAULT = ROOT / "data" / "battue_100vars.json"
DATA_EXTS = {".csv", ".sav", ".dta", ".xlsx", ".xls"}


def discover_surveys(allowed: Optional[list[str]] = None) -> list[tuple[str, Path]]:
    """Parcourt _SharedFolder_data_produit/ et retourne (survey_id, data_file)."""
    results = []
    for survey_dir in sorted(DATA_DIR.iterdir()):
        if not survey_dir.is_dir() or survey_dir.name.startswith("_"):
            continue
        if allowed and survey_dir.name not in allowed:
            continue
        data_files = [f for f in survey_dir.iterdir() if f.suffix.lower() in DATA_EXTS]
        if not data_files:
            continue
        main_file = max(data_files, key=lambda f: f.stat().st_size)
        results.append((survey_dir.name, main_file))
    return results


def stratified_sample(
    surveys: list[tuple[str, Path]],
    n_total: int,
    rng_seed: int,
) -> list[tuple[str, Path, str]]:
    """Échantillonnage stratifié proportionnel aux colonnes par sondage."""
    import random
    from surveys.io import read_survey_file

    rng = random.Random(rng_seed)
    survey_cols = []

    for survey_id, data_file in surveys:
        try:
            df, _ = read_survey_file(data_file)
            cols = list(df.columns)
            if cols:
                survey_cols.append((survey_id, data_file, cols))
        except Exception as e:
            print(f"  [SKIP] {survey_id} : {e}", file=sys.stderr)

    total_vars = sum(len(cols) for _, _, cols in survey_cols)
    if total_vars == 0:
        raise ValueError("Aucune variable trouvée.")

    quotas = {sid: max(1, round(len(cols) / total_vars * n_total))
              for sid, _, cols in survey_cols}
    diff = n_total - sum(quotas.values())
    sorted_by_size = sorted(survey_cols, key=lambda x: -len(x[2]))
    for i in range(abs(diff)):
        sid = sorted_by_size[i % len(sorted_by_size)][0]
        quotas[sid] = max(0, quotas[sid] + (1 if diff > 0 else -1))

    samples = []
    for survey_id, data_file, cols in survey_cols:
        quota = quotas.get(survey_id, 0)
        if quota == 0:
            continue
        chosen = rng.sample(cols, min(quota, len(cols)))
        for col in chosen:
            samples.append((survey_id, data_file, col))
    return samples


def value_counts_dict(series: pd.Series, top_n: int = 20) -> dict:
    """Retourne un dict {valeur: count} pour les top_n valeurs."""
    counts = series.value_counts(dropna=True)
    top = counts.head(top_n)
    return {str(k): int(v) for k, v in top.items()}


def extract(
    n_total: int = 100,
    rng_seed: int = 42,
    output_path: Path = OUTPUT_DEFAULT,
    allowed_surveys: Optional[list[str]] = None,
    verbose: bool = True,
) -> None:
    from surveys.io import read_survey_file
    from surveys.pattern_engine import classify

    def log(msg: str) -> None:
        if verbose:
            print(msg)

    log(f"Découverte des sondages dans : {DATA_DIR}")
    surveys = discover_surveys(allowed_surveys)
    log(f"  {len(surveys)} sondages trouvés\n")

    log(f"Échantillonnage stratifié (~{n_total} vars, seed={rng_seed})")
    samples = stratified_sample(surveys, n_total, rng_seed)
    log(f"  {len(samples)} variables sélectionnées sur {len(surveys)} sondages\n")

    by_survey = {}
    for survey_id, data_file, var_name in samples:
        key = (survey_id, str(data_file))
        by_survey.setdefault(key, []).append(var_name)

    output_path.parent.mkdir(parents=True, exist_ok=True)
    output = []

    for (survey_id, data_file_str), var_names in by_survey.items():
        data_file = Path(data_file_str)
        log(f"→ {survey_id}  ({len(var_names)} vars)  [{data_file.name}]")

        try:
            df, meta = read_survey_file(data_file)
        except Exception as e:
            log(f"  [ERREUR chargement] {e}")
            continue

        for var_name in var_names:
            if var_name not in df.columns:
                log(f"    [SKIP] colonne absente : {var_name}")
                continue

            series: pd.Series = df[var_name]  # type: ignore[assignment]

            try:
                result = classify(series)
                var_output = {
                    "survey_id": survey_id,
                    "raw_name": var_name,
                    "var_label": meta.variable_labels.get(var_name, ""),
                    "n_unique": result.effective_n_unique if result.effective_n_unique is not None else series.nunique(),
                    "tier_auto": result.tier,
                    "pattern_id_auto": result.pattern_id,
                    "confidence_auto": result.confidence,
                    "all_confidences": result.all_confidences,
                    "reason": result.reason,
                    "missing_codes": {
                        "codes": sorted(list(result.missing_codes.codes)),
                        "meanings": result.missing_codes.meanings,
                        "high_missing_rate": result.missing_codes.high_missing_rate,
                    },
                    "value_counts": value_counts_dict(series),
                    "tier_manuel": None,
                    "pattern_id_manuel": None,
                    "notes": None,
                }
                output.append(var_output)
                log(f"    ✓ {var_name:30s}  tier={result.tier}  "
                    f"pattern={result.pattern_id or '—':25s}  conf={result.confidence:.2f}")
            except Exception as e:
                log(f"    [ERREUR classify] {var_name} : {e}")
                continue

    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(output, f, indent=2, ensure_ascii=False)

    tier_dist = {}
    for v in output:
        tier_dist[v["tier_auto"]] = tier_dist.get(v["tier_auto"], 0) + 1
    log(f"\n{'─'*60}")
    log(f"JSON exporté : {output_path}")
    log(f"  Variables écrites : {len(output)}")
    log(f"  Distribution Tier  : {tier_dist}")
    tier1_rate = tier_dist.get(1, 0) / len(output) * 100 if output else 0
    log(f"  Taux Tier 1     : {tier1_rate:.1f}%")
    log(f"\nProchaines étapes :")
    log(f"  1. Transférer le JSON à Claude Code pour diagnostic pattern")
    log(f"  2. Remplir tier_manuel/pattern_id_manuel/notes si tu veux valider")


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Battue : extrait ~N variables avec classification auto pour analyse pattern."
    )
    parser.add_argument("--n", type=int, default=100,
                        help="Nombre de variables à échantillonner (défaut : 100)")
    parser.add_argument("--seed", type=int, default=42,
                        help="Graine aléatoire (défaut : 42)")
    parser.add_argument("--output", type=Path, default=OUTPUT_DEFAULT,
                        help=f"JSON de sortie (défaut : {OUTPUT_DEFAULT})")
    parser.add_argument("--surveys", nargs="+", metavar="SURVEY_ID",
                        help="Restreindre à certains sondages")
    parser.add_argument("--quiet", action="store_true",
                        help="Mode silencieux")
    args = parser.parse_args()

    extract(
        n_total=args.n,
        rng_seed=args.seed,
        output_path=args.output,
        allowed_surveys=args.surveys,
        verbose=not args.quiet,
    )


if __name__ == "__main__":
    main()
