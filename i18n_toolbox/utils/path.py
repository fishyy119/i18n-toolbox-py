from pathlib import Path


def expand_pattern(base: Path, pattern: str, lang: str) -> list[Path]:
    """
    Expand a pattern like "{lang}/*.json" to actual paths.

    Parameters
    ----------
    base : Path
        Base directory for i18n files.
    pattern : str
        Pattern string, e.g. "{lang}/*.json".
    lang : str
        Language code.

    Returns
    -------
    list[Path]
    """
    real_pattern = pattern.replace("{lang}", lang)
    return sorted(base.glob(real_pattern))
