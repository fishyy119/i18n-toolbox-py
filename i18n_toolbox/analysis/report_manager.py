# pyright: standard
from pathlib import Path
from typing import Dict, List

from i18n_toolbox.utils.console import log_info, log_warn

from .check_missing import check_missing


class ReportManager:
    """管理 i18n 分析报告的生成和保存"""

    def __init__(self, report_dir: str | Path = "reports") -> None:
        self.report_dir: Path = Path(report_dir).resolve()
        self.report_dir.mkdir(parents=True, exist_ok=True)

    def save_json(self, data: Dict | List, filename: str) -> Path:
        """保存 JSON 报告"""
        path = self.report_dir / filename
        import json

        with path.open("w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        return path

    def run_missing_check(self, all_data: Dict[str, Dict[str, str]], base: str, target: str | List[str]) -> None:
        targets: List[str] = [target] if isinstance(target, str) else target

        for lang in targets:
            if lang not in all_data:
                log_warn(f"语言 {lang} 不存在于数据中，跳过")
                continue

            missing_keys = check_missing(all_data[base], all_data[lang])
            report = {
                "language": lang,
                "missing_count": len(missing_keys),
                "missing_keys": missing_keys,
            }
            report_path = self.save_json(report, f"{lang}_missing.json")
            log_info("报告已生成:", report_path)
