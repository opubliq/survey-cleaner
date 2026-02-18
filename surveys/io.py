"""
surveys/io.py — Lecture robuste de n'importe quel fichier de données de sondage.

Point d'entrée unique : ``read_survey_file(path)``.

Gère :
  - CSV : auto-détection encodage (UTF-8, latin-1, cp1252, utf-8-sig) et
          séparateur (',', ';', '\\t') via sniffing + fallback exhaustif.
  - SAV  (SPSS)  : pyreadstat, retourne (df, variable_labels)
  - DTA  (Stata) : pandas read_stata, extrait les labels depuis df.attrs
  - XLSX / XLS   : openpyxl via pandas

Usage::

    from surveys.io import read_survey_file

    df, meta = read_survey_file(Path("data.csv"))
    # meta.variable_labels  → dict[str, str]
    # meta.encoding          → str détecté
    # meta.sep               → str séparateur CSV

    df, meta = read_survey_file(Path("data.sav"))
"""

from __future__ import annotations

import logging
import warnings
from dataclasses import dataclass, field
from pathlib import Path
from typing import Optional

import pandas as pd

logger = logging.getLogger(__name__)

# ---------------------------------------------------------------------------
# Résultat de la lecture
# ---------------------------------------------------------------------------

@dataclass
class SurveyReadMeta:
    """Métadonnées retournées avec le DataFrame."""

    file_path: Path
    format: str                              # "csv" | "sav" | "dta" | "xlsx"
    encoding: Optional[str] = None          # encodage utilisé (CSV seulement)
    sep: Optional[str] = None               # séparateur utilisé (CSV seulement)
    variable_labels: dict[str, str] = field(default_factory=dict)
    # dict col_name → label (SAV + DTA uniquement ; vide pour CSV/XLSX)

    def __repr__(self) -> str:
        return (
            f"SurveyReadMeta(format={self.format!r}, "
            f"encoding={self.encoding!r}, sep={self.sep!r}, "
            f"n_labels={len(self.variable_labels)})"
        )


# ---------------------------------------------------------------------------
# Constantes de sniffing CSV
# ---------------------------------------------------------------------------

_CSV_ENCODINGS = ["utf-8", "utf-8-sig", "latin-1", "cp1252"]
_CSV_SEPS = [",", ";", "\t"]
_SNIFF_BYTES = 16_384   # octets lus pour la détection


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _detect_encoding(raw: bytes) -> list[str]:
    """
    Retourne une liste d'encodages triés par probabilité décroissante.
    Utilise charset-normalizer si disponible, sinon fallback sur la liste fixe.
    """
    try:
        from charset_normalizer import from_bytes
        matches = from_bytes(raw)
        best = matches.best()
        if best:
            detected = str(best.encoding)
            # Met l'encodage détecté en tête de liste, sans doublon
            ordered = [detected] + [e for e in _CSV_ENCODINGS if e != detected]
            return ordered
    except ImportError:
        pass
    return list(_CSV_ENCODINGS)


def _try_read_csv(
    path: Path,
    encoding: str,
    sep: str,
    nrows: Optional[int] = None,
) -> pd.DataFrame:
    """Tente de lire le CSV avec les paramètres donnés. Lève si ça échoue."""
    kwargs: dict = {
        "sep": sep,
        "encoding": encoding,
        "low_memory": False,
        "on_bad_lines": "warn",
    }
    if nrows is not None:
        kwargs["nrows"] = nrows
    return pd.read_csv(path, **kwargs)


def _sniff_csv(path: Path, raw: bytes) -> tuple[str, str]:
    """
    Détecte l'encodage et le séparateur d'un CSV.
    Essaie toutes les combinaisons encodage × séparateur et retourne
    (encoding, sep) de la première qui lit >1 colonne sans erreur.
    Lève ValueError si aucune combinaison ne marche.
    """
    encodings = _detect_encoding(raw)
    best: Optional[tuple[str, str]] = None
    best_ncols = 1

    for enc in encodings:
        for sep in _CSV_SEPS:
            try:
                df = _try_read_csv(path, enc, sep, nrows=10)
                ncols = len(df.columns)
                if ncols > best_ncols:
                    best_ncols = ncols
                    best = (enc, sep)
                    # Optimisation : si on a beaucoup de colonnes, c'est bon
                    if ncols >= 5:
                        return best
            except Exception:
                pass

    if best is not None:
        return best

    raise ValueError(
        f"Impossible de lire {path.name} : aucune combinaison "
        f"encodage/séparateur n'a fonctionné parmi "
        f"{encodings} × {_CSV_SEPS}"
    )


# ---------------------------------------------------------------------------
# Lecteurs par format
# ---------------------------------------------------------------------------

def _read_csv(path: Path) -> tuple[pd.DataFrame, SurveyReadMeta]:
    with open(path, "rb") as f:
        raw = f.read(_SNIFF_BYTES)

    encoding, sep = _sniff_csv(path, raw)
    logger.debug(f"CSV sniff: {path.name} → encoding={encoding!r} sep={sep!r}")

    # Lecture complète : si l'encodage sniffé échoue sur le fichier entier
    # (octets non-ASCII hors des premières lignes), on descend la cascade.
    cascade = [encoding] + [e for e in _CSV_ENCODINGS if e != encoding]
    last_err: Exception = RuntimeError("no attempt made")
    for enc in cascade:
        try:
            df = _try_read_csv(path, enc, sep)
            if enc != encoding:
                logger.debug(f"CSV fallback encoding: {path.name} → {enc!r}")
            meta = SurveyReadMeta(
                file_path=path,
                format="csv",
                encoding=enc,
                sep=sep,
            )
            return df, meta
        except (UnicodeDecodeError, UnicodeError) as e:
            last_err = e
            continue

    raise ValueError(
        f"Impossible de lire {path.name} avec sep={sep!r} "
        f"pour aucun encodage parmi {cascade} : {last_err}"
    )


def _read_sav(path: Path) -> tuple[pd.DataFrame, SurveyReadMeta]:
    import pyreadstat  # type: ignore[import]

    df, prs_meta = pyreadstat.read_sav(str(path))

    # column_names_to_labels : {col_name: label_str} ou None
    raw_labels = getattr(prs_meta, "column_names_to_labels", None) or {}
    labels: dict[str, str] = dict(raw_labels)

    meta = SurveyReadMeta(
        file_path=path,
        format="sav",
        variable_labels=labels,
    )
    return df, meta


def _read_dta(path: Path) -> tuple[pd.DataFrame, SurveyReadMeta]:
    df_raw = pd.read_stata(str(path))
    df = df_raw if isinstance(df_raw, pd.DataFrame) else df_raw.read()

    # pandas ≥ 1.3 expose les variable labels dans df.attrs
    labels: dict[str, str] = {}
    if hasattr(df, "attrs") and isinstance(df.attrs, dict):
        labels = dict(df.attrs.get("variable_labels", {}))

    meta = SurveyReadMeta(
        file_path=path,
        format="dta",
        variable_labels=labels,
    )
    return df, meta


def _read_xlsx(path: Path) -> tuple[pd.DataFrame, SurveyReadMeta]:
    df = pd.read_excel(path)
    meta = SurveyReadMeta(file_path=path, format="xlsx")
    return df, meta


# ---------------------------------------------------------------------------
# Entrée publique
# ---------------------------------------------------------------------------

_READERS = {
    ".csv": _read_csv,
    ".sav": _read_sav,
    ".dta": _read_dta,
    ".xlsx": _read_xlsx,
    ".xls": _read_xlsx,
}


def read_survey_file(path: Path) -> tuple[pd.DataFrame, SurveyReadMeta]:
    """
    Lit n'importe quel fichier de données de sondage et retourne
    ``(DataFrame, SurveyReadMeta)``.

    Formats supportés : .csv, .sav, .dta, .xlsx, .xls

    Pour les CSV, l'encodage et le séparateur sont détectés automatiquement
    (UTF-8, UTF-8-BOM, latin-1, cp1252 ; virgule, point-virgule, tabulation).

    Parameters
    ----------
    path : Path
        Chemin vers le fichier de données.

    Returns
    -------
    df : pd.DataFrame
        Données brutes.
    meta : SurveyReadMeta
        Métadonnées de lecture (format, encodage, séparateur, labels).

    Raises
    ------
    ValueError
        Si le format n'est pas supporté ou si la lecture échoue pour tous
        les encodages/séparateurs essayés.
    FileNotFoundError
        Si le fichier n'existe pas.
    """
    path = Path(path)
    if not path.exists():
        raise FileNotFoundError(f"Fichier introuvable : {path}")

    suffix = path.suffix.lower()
    reader = _READERS.get(suffix)
    if reader is None:
        raise ValueError(
            f"Format non supporté : {suffix!r}. "
            f"Formats acceptés : {list(_READERS)}"
        )

    return reader(path)
