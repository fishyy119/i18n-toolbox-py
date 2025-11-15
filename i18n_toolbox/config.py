# pyright: standard

import tomllib
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict, List


@dataclass(frozen=True)
class I18nConfig:
    project_root: Path
    base_dir: Path
    pattern: str
    languages: List[str]
    scan_dirs: List[Path]


def load_config(path: str | Path) -> I18nConfig:
    """
    加载并解析项目的配置文件（TOML 格式），并构建 I18nConfig 对象。

    Args:
        path (str | Path): 配置文件路径，可以是字符串或 Path 对象。

    Raises:
        FileNotFoundError: 配置文件不存在。
        ValueError: 缺少 project_root 字段。
        ValueError: 缺少 [i18n] 配置段。
        ValueError: 缺少 i18n.pattern 字段。

    Returns:
        I18nConfig: 已解析的项目配置对象。
    """
    cfg_path = Path(path).resolve()
    if not cfg_path.exists():
        raise FileNotFoundError(f"Config file not found: {cfg_path}")

    with cfg_path.open("rb") as f:
        raw = tomllib.load(f)

    # 项目根目录，必须提供
    raw_root = raw.get("project_root")
    if raw_root is None:
        raise ValueError("Missing required field: project_root")

    project_root = Path(raw_root).expanduser().resolve()

    # ----------------------------- i18n 部分 -----------------------------
    i18n = raw.get("i18n")
    if not isinstance(i18n, dict):
        raise ValueError("[i18n] section missing in config")

    # i18n.base_dir：语言文件所在基础路径（相对项目根目录）
    base_dir = project_root / i18n.get("base_dir", "")

    # i18n.pattern：文件命名模式（必须提供）
    pattern = i18n.get("pattern")
    if not pattern:
        raise ValueError("[i18n.pattern] is required")

    # i18n.languages：语言列表，可为空，空时自动检测
    langs_raw = i18n.get("languages", [])
    langs: List[str] = langs_raw if langs_raw else _detect_languages(base_dir)

    # i18n.scan_dirs：额外扫描路径列表（相对项目根目录）
    scan_dirs_raw: List[str] = i18n.get("scan_dirs", [])
    scan_dirs: List[Path] = [(project_root / p).resolve() for p in scan_dirs_raw]

    # ---------------------------- 返回配置对象 ----------------------------
    return I18nConfig(
        project_root=project_root,
        base_dir=base_dir,
        pattern=pattern,
        languages=langs,
        scan_dirs=scan_dirs,
    )


def _detect_languages(base_dir: Path) -> list[str]:
    """
    检测所有语言文件,返回文件夹名词
    """
    if not base_dir.exists():
        return []

    langs = []
    for p in base_dir.iterdir():
        if p.is_dir():
            langs.append(p.name)

    return sorted(langs)
