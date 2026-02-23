#!/usr/bin/env python3
"""
Battue : analyse le JSON d'extraction par batchs.

Lit data/battue_100vars.json et affiche des batchs analysables.
Chaque batch peut être transmis à Claude Code pour diagnostic pattern.

Usage:
    python scripts/battue_analyze.py              # montre tous les batchs (read-only)
    python scripts/battue_analyze.py --batch 0      # montre le batch 0 uniquement
    python scripts/battue_analyze.py --batch 2 --n 15  # batch 2, 15 entrées
"""

import argparse
import json
from pathlib import Path
from typing import Optional

JSON_PATH = Path("data/battue_100vars.json")


def load_json() -> list[dict]:
    """Charge le JSON d'extraction."""
    if not JSON_PATH.exists():
        raise FileNotFoundError(f"JSON introuvable : {JSON_PATH}")
    with open(JSON_PATH, encoding="utf-8") as f:
        return json.load(f)


def summarize_all(data: list[dict]) -> dict:
    """Résumé global de toutes les variables."""
    tier_dist = {}
    for d in data:
        tier_dist[d["tier_auto"]] = tier_dist.get(d["tier_auto"], 0) + 1

    # Pattern coverage
    pattern_dist = {}
    for d in data:
        pid = d["pattern_id_auto"] or "None"
        pattern_dist[pid] = pattern_dist.get(pid, 0) + 1

    # Top 5 patterns les plus fréquents
    top_patterns = sorted(pattern_dist.items(), key=lambda x: -x[1])[:5]

    return {
        "total": len(data),
        "tier_dist": tier_dist,
        "pattern_dist": pattern_dist,
        "top_patterns": top_patterns,
        "tier1_rate": tier_dist.get(1, 0) / len(data) * 100 if data else 0,
    }


def batch_analysis(batch: list[dict], batch_idx: int) -> str:
    """
    Analyse un batch d'entrées et retourne une version compacte
    prête pour être montrée à Claude Code.
    """
    lines = [f"=== Batch {batch_idx} ({len(batch)} variables) ==="]

    # Résumé du batch
    tier_dist = {1: 0, 2: 0, 3: 0}
    tier1_pattern_dist = {}
    tier2_near_misses = []

    for d in batch:
        tier = d["tier_auto"]
        tier_dist[tier] = tier_dist.get(tier, 0) + 1

        if tier == 1:
            pid = d["pattern_id_auto"]
            tier1_pattern_dist[pid] = tier1_pattern_dist.get(pid, 0) + 1
        elif tier == 2:
            # Trouve les top 3 patterns (near misses)
            confs = d.get("all_confidences", {})
            top = sorted(confs.items(), key=lambda x: -x[1])[:3]
            if top and top[0][1] < 0.8:
                tier2_near_misses.append((d["raw_name"], top))

    lines.append(f"Tier distribution: {tier_dist}")
    lines.append(f"Tier 1 patterns: {tier1_pattern_dist}")

    # Détail des entrées (format compact)
    lines.append("\nDétail par variable:")
    for d in batch:
        lines.append(
            f"  [{d['tier_auto']}] {d['survey_id']}.{d['raw_name']:30s} | "
            f"pattern={d['pattern_id_auto'] or 'None':20s} | conf={d['confidence_auto']:.2f} | "
            f"n_unique={d['n_unique']} | "
            f"val_samples={', '.join(list(d['value_counts'].keys())[:4])}"
        )

    # Near-misses pour Tier 2 (potentiels ajustements)
    if tier2_near_misses:
        lines.append("\nTier 2 near-misses (scores proches de 0.8):")
        for var_name, top in tier2_near_misses[:10]:
            lines.append(f"  {var_name}: {top}")

    return "\n".join(lines)


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Analyse le JSON battue par batchs pour validation pattern."
    )
    parser.add_argument(
        "--batch-size", type=int, default=20,
        help="Taille des batchs (défaut : 20)"
    )
    parser.add_argument(
        "--batch", type=int, default=None,
        help="Numéro de batch spécifique à afficher (0-indexed). Si omis, montre tous."
    )
    parser.add_argument(
        "--n", type=int, default=None,
        help="Nombre d'entrées par batch (écrase --batch-size si utilisé)"
    )
    parser.add_argument(
        "--json", action="store_true",
        help="Affiche le batch en JSON brut au lieu du format lisible"
    )
    args = parser.parse_args()

    batch_size = args.n or args.batch_size
    data = load_json()

    # Résumé global
    summary = summarize_all(data)
    print(f"\n=== RÉSUMÉ GLOBAL ===")
    print(f"Total variables : {summary['total']}")
    print(f"Distribution Tier : {summary['tier_dist']}")
    print(f"Taux Tier 1     : {summary['tier1_rate']:.1f}%")
    print(f"Top 5 patterns    : {summary['top_patterns']}")

    # Afficher batch(s)
    total_batches = (len(data) + batch_size - 1) // batch_size

    if args.batch is not None:
        # Un seul batch
        start = args.batch * batch_size
        end = start + batch_size
        batch = data[start:end]
        if args.json:
            print("\n" + json.dumps(batch, indent=2, ensure_ascii=False))
        else:
            print("\n" + batch_analysis(batch, args.batch))
    else:
        # Tous les batchs (summary)
        print(f"\n=== BATCHS (taille={batch_size}, total={total_batches}) ===")
        print("Utilise --batch N pour voir le détail d'un batch spécifique\n")

        for i in range(total_batches):
            start = i * batch_size
            end = start + batch_size
            batch = data[start:end]

            # Mini-résumé de chaque batch
            tier_dist = {1: 0, 2: 0, 3: 0}
            patterns = {}
            for d in batch:
                t = d["tier_auto"]
                tier_dist[t] = tier_dist.get(t, 0) + 1
                if t == 1 and d["pattern_id_auto"]:
                    patterns[d["pattern_id_auto"]] = patterns.get(d["pattern_id_auto"], 0) + 1

            print(f"Batch {i}: Tier {tier_dist} | Patterns T1: {dict(sorted(patterns.items()))}")


if __name__ == "__main__":
    main()
