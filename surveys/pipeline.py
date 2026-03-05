#!/usr/bin/env python3
"""
pipeline.py — Orchestrateur v3 du pipeline de nettoyage de sondages.

Usage:
    python surveys/pipeline.py <survey_id>
    python surveys/pipeline.py eeq_2007
    python surveys/pipeline.py eeq_2007 --vars q2 q3 nomx   # subset de variables
    python surveys/pipeline.py eeq_2007 --skip-validate      # skip étape validation
"""

import argparse
import json
import shutil
import subprocess
import sys
import textwrap
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime
from pathlib import Path

SURVEYS_DIR = Path(__file__).parent
REPO_ROOT = SURVEYS_DIR.parent
SHARED_FOLDER = REPO_ROOT / "_SharedFolder_data_produit"


# ============================================================================
# Helpers
# ============================================================================

def log(msg: str) -> None:
    ts = datetime.now().strftime("%H:%M:%S")
    print(f"[{ts}] {msg}", flush=True)


def run_agent(agent: str, prompt: str, survey_id: str, tag: str, model: str | None = None) -> str:
    """
    Appelle `opencode run --agent <agent> --format json <prompt>`.
    Capture le sessionID depuis le premier event JSON.
    Exporte la session dans surveys/{survey_id}/logs/{tag}_{session_id}.json.
    Retourne le sessionID.
    """
    logs_dir = SURVEYS_DIR / survey_id / "logs"
    logs_dir.mkdir(parents=True, exist_ok=True)

    cmd = ["opencode", "run", "--agent", agent, "--format", "json"]
    if model:
        cmd += ["--model", model]
    cmd.append(prompt)
    log(f"  → agent={agent} model={model or 'agent-default'} tag={tag}")

    result = subprocess.run(cmd, capture_output=True, text=True)

    # Extraire le sessionID du premier event JSON valide
    session_id = None
    for line in result.stdout.splitlines():
        line = line.strip()
        if not line:
            continue
        try:
            event = json.loads(line)
            session_id = event.get("sessionID")
            if session_id:
                break
        except json.JSONDecodeError:
            continue

    if result.returncode != 0:
        log(f"  [ERREUR] agent={agent} tag={tag} rc={result.returncode}")
        if result.stderr:
            print(result.stderr[:500], file=sys.stderr)

    # Exporter la session pour debug
    if session_id:
        export_session(session_id, logs_dir, tag)
    else:
        log(f"  [WARN] Pas de sessionID pour {tag} — export impossible")

    return session_id or ""


def export_session(session_id: str, logs_dir: Path, tag: str) -> None:
    """Exporte la session opencode en JSON dans logs/."""
    out_path = logs_dir / f"{tag}_{session_id}.json"
    export = subprocess.run(
        ["opencode", "export", session_id],
        capture_output=True, text=True,
    )
    if export.returncode == 0:
        out_path.write_text(export.stdout, encoding="utf-8")
        log(f"  [log] {out_path.relative_to(REPO_ROOT)}")
    else:
        log(f"  [WARN] Export session {session_id} échoué")


# ============================================================================
# Étapes du pipeline
# ============================================================================

def init(survey_id: str) -> None:
    """
    Étape 0 — Initialisation déterministe (pas d'agent LLM).
    - Crée surveys/{survey_id}/ et vars/ et logs/
    - Copie le template clean.py si absent
    - Crée ou met à jour surveys/status.json
    """
    log(f"[0/5] init({survey_id})")
    survey_dir = SURVEYS_DIR / survey_id
    (survey_dir / "vars").mkdir(parents=True, exist_ok=True)
    (survey_dir / "logs").mkdir(parents=True, exist_ok=True)

    # Template clean.py
    clean_path = survey_dir / "clean.py"
    if not clean_path.exists():
        template = SURVEYS_DIR / "_template" / "clean.py"
        content = template.read_text(encoding="utf-8").replace("[SURVEY_ID]", survey_id).replace("[NOM_SONDAGE]", survey_id)
        clean_path.write_text(content, encoding="utf-8")
        log(f"  [ok] clean.py créé depuis template")
    else:
        log(f"  [skip] clean.py déjà présent")

    # Trouver le fichier de données dans _SharedFolder_data_produit
    source_dir = SHARED_FOLDER / survey_id
    data_file = None
    n_obs = n_vars = None
    if source_dir.exists():
        for ext in ("*.sav", "*.dta", "*.csv", "*.xlsx", "*.xls"):
            found = list(source_dir.glob(ext))
            if found:
                data_file = str(found[0])
                break
        if data_file:
            try:
                import importlib.util
                spec = importlib.util.spec_from_file_location("surveys_io", SURVEYS_DIR / "io.py")
                assert spec and spec.loader
                surveys_io = importlib.util.module_from_spec(spec)
                spec.loader.exec_module(surveys_io)  # type: ignore[union-attr]
                df, _ = surveys_io.read_survey_file(data_file, usecols=None)
                n_obs, n_vars = len(df), len(df.columns)
                log(f"  [ok] {Path(data_file).name} — {n_obs} obs x {n_vars} vars")
            except Exception as e:
                log(f"  [WARN] Impossible de lire le fichier de données: {e}")
    else:
        log(f"  [WARN] {source_dir} introuvable — status.json sans métadonnées de données")

    # status.json
    status_path = SURVEYS_DIR / "status.json"
    status = json.loads(status_path.read_text(encoding="utf-8")) if status_path.exists() else {"surveys": {}}
    if survey_id not in status["surveys"]:
        status["surveys"][survey_id] = {
            "status": "not_started",
            "created_date": datetime.now().strftime("%Y-%m-%d"),
            "data_file": data_file,
            "n_observations": n_obs,
            "n_variables": n_vars,
            "variables": {"total": n_vars, "cleaned": 0, "pending": n_vars},
            "last_updated": datetime.now().isoformat(),
        }
        status_path.write_text(json.dumps(status, indent=2, ensure_ascii=False), encoding="utf-8")
        log(f"  [ok] status.json — {survey_id} ajouté")
    else:
        log(f"  [skip] status.json — {survey_id} déjà présent")


def parse_codebook(survey_id: str, model: str | None = None) -> None:
    """Étape 1 — Appelle l'agent transform-codebook → codebook.json."""
    log(f"[1/5] parse_codebook({survey_id})")
    prompt = json.dumps({
        "survey_id": survey_id,
        "shared_folder": str(SHARED_FOLDER / survey_id),
        "surveys_dir": str(SURVEYS_DIR / survey_id),
    })
    run_agent("transform-codebook", prompt, survey_id, "transform-codebook", model=model)


def clean_variable(survey_id: str, variable_name: str, model: str | None = None) -> str:
    """Étape 2 — Appelle l'agent clean-variable pour UNE variable."""
    ctx_path = SURVEYS_DIR / survey_id / "vars" / f"ctx_{variable_name}.json"
    if not ctx_path.exists():
        # Trouver le data_file depuis status.json pour éviter que l'agent cherche
        data_file = None
        status_path = SURVEYS_DIR / "status.json"
        if status_path.exists():
            status = json.loads(status_path.read_text(encoding="utf-8"))
            data_file = status.get("surveys", {}).get(survey_id, {}).get("data_file")
        prompt = json.dumps({
            "survey_id": survey_id,
            "variable_name": variable_name,
            "surveys_dir": str(SURVEYS_DIR / survey_id),
            "data_file": data_file,
        })
    else:
        prompt = ctx_path.read_text(encoding="utf-8")

    tag = f"clean-variable_{variable_name}"
    return run_agent("clean-variable", prompt, survey_id, tag, model=model)


def clean_all_variables(survey_id: str, variables: list[str], max_workers: int = 4, model: str | None = None) -> None:
    """Étape 2 — Nettoie toutes les variables en parallèle."""
    log(f"[2/5] clean_variable x{len(variables)} (max_workers={max_workers})")
    with ThreadPoolExecutor(max_workers=max_workers) as pool:
        futures = {
            pool.submit(clean_variable, survey_id, var, model): var
            for var in variables
        }
        for fut in as_completed(futures):
            var = futures[fut]
            try:
                fut.result()
                log(f"  [ok] {var}")
            except Exception as exc:
                log(f"  [ERREUR] {var}: {exc}")


def assemble(survey_id: str) -> None:
    """
    Étape 3 — Assemble tous les vars/*.py en un clean.py complet.
    Concatène les fichiers vars/*.py dans le corps de clean_data().
    """
    log(f"[3/5] assemble({survey_id})")
    survey_dir = SURVEYS_DIR / survey_id
    vars_dir = survey_dir / "vars"
    var_files = sorted(vars_dir.glob("*.py")) if vars_dir.exists() else []

    if not var_files:
        log("  [WARN] Aucun fichier vars/*.py trouvé — clean.py non généré")
        return

    template_path = SURVEYS_DIR / "_template" / "clean.py"
    template = template_path.read_text(encoding="utf-8")

    # Construire le bloc de nettoyage à partir des vars/*.py
    var_blocks = []
    for vf in var_files:
        var_blocks.append(f"    # --- {vf.stem} ---")
        for line in vf.read_text(encoding="utf-8").splitlines():
            var_blocks.append("    " + line if line.strip() else "")
        var_blocks.append("")

    injected = "\n".join(var_blocks)

    # Remplacer le placeholder TODO dans le template
    placeholder = (
        "    # ========================================================================\n"
        "    # TODO: Ajouter le code de nettoyage pour chaque variable ci-dessous\n"
        "    # Pattern: nettoyage variable → entrée CODEBOOK_VARIABLES → prochaine variable\n"
        "    # ========================================================================\n"
    )
    if placeholder in template:
        clean_py = template.replace(placeholder, injected + "\n")
    else:
        # Fallback: insérer avant le return df_clean
        clean_py = template.replace("    return df_clean", injected + "\n    return df_clean")

    # Remplacer les placeholders du template
    clean_py = clean_py.replace("[SURVEY_ID]", survey_id).replace("[NOM_SONDAGE]", survey_id)

    out_path = survey_dir / "clean.py"
    out_path.write_text(clean_py, encoding="utf-8")
    log(f"  [ok] {out_path.relative_to(REPO_ROOT)} ({len(var_files)} variables)")


def validate_all_variables(survey_id: str, variables: list[str], max_workers: int = 4, model: str | None = None) -> None:
    """Étape 4 (optionnelle) — Valide chaque vars/*.py via l'agent validate-cleaning."""
    log(f"[4/5] validate x{len(variables)} (max_workers={max_workers})")

    def _validate_one(var: str) -> str:
        ctx_path = SURVEYS_DIR / survey_id / "vars" / f"ctx_{var}.json"
        prompt = str(ctx_path) if ctx_path.exists() else json.dumps({
            "survey_id": survey_id, "variable_name": var,
        })
        tag = f"validate_{var}"
        return run_agent("validate-cleaning", prompt, survey_id, tag, model=model)

    with ThreadPoolExecutor(max_workers=max_workers) as pool:
        futures = {pool.submit(_validate_one, var): var for var in variables}
        for fut in as_completed(futures):
            var = futures[fut]
            try:
                fut.result()
                log(f"  [ok] {var}")
            except Exception as exc:
                log(f"  [ERREUR] {var}: {exc}")


def finalize(survey_id: str, model: str | None = None) -> None:
    """Étape 5 — Appelle l'agent finalize-survey → met status.json à 'completed'."""
    log(f"[5/5] finalize({survey_id})")
    prompt = json.dumps({"survey_id": survey_id, "surveys_dir": str(SURVEYS_DIR)})
    run_agent("finalize-survey", prompt, survey_id, "finalize-survey", model=model)


# ============================================================================
# Coût d'un sondage
# ============================================================================

def survey_cost(survey_id: str) -> None:
    """
    Lit tous les logs JSON dans surveys/{survey_id}/logs/ et imprime
    un résumé des tokens et coûts par agent + total.
    """
    logs_dir = SURVEYS_DIR / survey_id / "logs"
    if not logs_dir.exists():
        print(f"Aucun log trouvé pour {survey_id}")
        return

    rows = []
    for log_file in sorted(logs_dir.glob("*.json")):
        try:
            data = json.loads(log_file.read_text(encoding="utf-8"))
        except Exception:
            continue

        t_in = t_out = t_cache_read = t_cache_write = cost = 0
        for msg in data.get("messages", []):
            info = msg.get("info", {})
            tokens = info.get("tokens", {})
            if not tokens:
                continue
            t_in          += tokens.get("input", 0) or 0
            t_out         += tokens.get("output", 0) or 0
            cache          = tokens.get("cache", {}) or {}
            t_cache_read  += cache.get("read", 0) or 0
            t_cache_write += cache.get("write", 0) or 0
            cost          += info.get("cost", 0) or 0

        rows.append({
            "tag": log_file.stem,
            "in": t_in,
            "out": t_out,
            "cache_r": t_cache_read,
            "cache_w": t_cache_write,
            "total": t_in + t_out + t_cache_read + t_cache_write,
            "cost": cost,
        })

    if not rows:
        print(f"Aucune donnée de tokens dans {logs_dir}")
        return

    # Affichage
    print(f"\n=== Coût pipeline : {survey_id} ===\n")
    col_w = max(len(r["tag"]) for r in rows) + 2
    header = f"{'Agent':<{col_w}}  {'Input':>8}  {'Output':>8}  {'Cache R':>8}  {'Cache W':>8}  {'Total':>10}  {'Cost':>10}"
    print(header)
    print("-" * len(header))
    for r in rows:
        print(f"{r['tag']:<{col_w}}  {r['in']:>8,}  {r['out']:>8,}  {r['cache_r']:>8,}  {r['cache_w']:>8,}  {r['total']:>10,}  ${r['cost']:>9.4f}")
    print("-" * len(header))
    totals = {k: sum(r[k] for r in rows) for k in ("in", "out", "cache_r", "cache_w", "total", "cost")}
    print(f"{'TOTAL':<{col_w}}  {totals['in']:>8,}  {totals['out']:>8,}  {totals['cache_r']:>8,}  {totals['cache_w']:>8,}  {totals['total']:>10,}  ${totals['cost']:>9.4f}")
    print()


# ============================================================================
# CLI
# ============================================================================

def get_variables_from_codebook(survey_id: str) -> list[str]:
    """Lit codebook.json et retourne la liste des noms de variables brutes."""
    cb_path = SURVEYS_DIR / survey_id / "codebook.json"
    if not cb_path.exists():
        log(f"  [WARN] codebook.json introuvable dans {survey_id}/")
        return []
    data = json.loads(cb_path.read_text(encoding="utf-8"))
    return list(data.get("variables", {}).keys())


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Pipeline v3 — nettoyage complet d'un sondage",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=textwrap.dedent("""\
            Exemples:
              python surveys/pipeline.py eeq_2007
              python surveys/pipeline.py eeq_2007 --vars q2 q3 nomx
              python surveys/pipeline.py eeq_2007 --skip-codebook --skip-validate
        """),
    )
    parser.add_argument("survey_id", help="ID du sondage (ex: eeq_2007)")
    parser.add_argument("--vars", nargs="+", metavar="VAR",
                        help="Subset de variables à nettoyer (défaut: toutes depuis codebook.json)")
    parser.add_argument("--max-vars", type=int, metavar="N",
                        help="Limiter aux N premières variables du codebook (utile pour tester)")
    parser.add_argument("--model", metavar="MODEL",
                        help="Modèle à utiliser pour tous les agents (ex: google/gemini-2.5-flash)")
    parser.add_argument("--skip-init", action="store_true",
                        help="Sauter l'init (répertoire + status.json déjà créés)")
    parser.add_argument("--skip-codebook", action="store_true",
                        help="Sauter l'étape transform-codebook (codebook.json déjà présent)")
    parser.add_argument("--skip-validate", action="store_true",
                        help="Sauter l'étape validate-cleaning")
    parser.add_argument("--skip-finalize", action="store_true",
                        help="Sauter l'étape finalize-survey")
    parser.add_argument("--workers", type=int, default=4,
                        help="Nombre de threads parallèles (défaut: 4)")
    parser.add_argument("--cost", action="store_true",
                        help="Afficher le rapport de coût des sessions (sans relancer le pipeline)")
    args = parser.parse_args()

    survey_id = args.survey_id

    # Mode coût seulement
    if args.cost:
        survey_cost(survey_id)
        return

    model = args.model or None
    log(f"=== Pipeline v3 : {survey_id} | model={model or 'agent-default'} ===")

    # 0. Init (déterministe, pas d'agent)
    if not args.skip_init:
        init(survey_id)
    else:
        log("[0/5] init — skipped")

    # 1. Codebook
    if not args.skip_codebook:
        parse_codebook(survey_id, model=model)
    else:
        log("[1/5] parse_codebook — skipped")

    # 2. Variables à nettoyer
    variables = args.vars or get_variables_from_codebook(survey_id)
    if args.max_vars:
        variables = variables[:args.max_vars]
    if not variables:
        log("[ERREUR] Aucune variable à nettoyer. Fournir --vars ou générer codebook.json d'abord.")
        sys.exit(1)
    log(f"  Variables: {variables}")
    clean_all_variables(survey_id, variables, max_workers=args.workers, model=model)

    # 3. Assemble
    assemble(survey_id)

    # 4. Validate
    if not args.skip_validate:
        validate_all_variables(survey_id, variables, max_workers=args.workers, model=model)
    else:
        log("[4/5] validate — skipped")

    # 5. Finalize
    if not args.skip_finalize:
        finalize(survey_id, model=model)
    else:
        log("[5/5] finalize — skipped")

    log(f"=== Done : {survey_id} ===")


if __name__ == "__main__":
    main()
