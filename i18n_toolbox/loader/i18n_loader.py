import shutil
from pathlib import Path
from typing import Dict, List

from ..analysis.check_missing import check_missing
from ..config import I18nConfig
from ..utils.console import log_error, log_info, log_warn  # type: ignore
from ..utils.json_tools import load_json_file, save_json, unflatten_json  # type: ignore
from ..utils.path import expand_pattern


class I18nLoader:
    """加载并管理i18n文件"""

    def __init__(self, cfg: I18nConfig, bak_dir: str = "baks"):
        self.cfg = cfg
        self.all_data = {}  # 所有语言的扁平化数据
        self.bak_dir = Path(bak_dir).resolve()
        self.bak_dir.mkdir(parents=True, exist_ok=True)

    def load_all(self) -> Dict[str, Dict[str, str]]:
        """
        加载所有语言文件,每个语言存储为一个扁平化字典.
        键名顶层为i18n命名空间,随后为嵌套结构的键,如"game.details.xxx"
        """
        all_data: Dict[str, Dict[str, str]] = {}

        for lang in self.cfg.languages:
            files = expand_pattern(self.cfg.base_dir, self.cfg.pattern, lang)

            lang_data: Dict[str, str] = {}
            for path in files:
                lang_data.update(load_json_file(path))

            all_data[lang] = lang_data

        self.all_data = all_data
        return all_data

    def fill_missing(self, base: str, targets: List[str]) -> Dict[str, int]:
        """
        根据基准语言填充目标语言缺失字段，值设为空字符串

        Args:
            base (str): 基准语言
            target (str | List[str], optional): 目标语言代码，默认补齐除 base 外所有语言

        Returns:
            Dict[str, int]: 每个目标语言补充的字段数量
        """
        all_data = self.all_data

        if base not in all_data:
            log_error(f"基准语言 {base} 不存在于数据中")

        filled_counts: Dict[str, int] = {}

        for lang in targets:
            if lang not in all_data:
                log_warn(f"语言 {lang} 不存在于数据中，跳过")
                continue

            # 获取缺失字段
            base_data = all_data[base]
            target_data = all_data[lang]
            missing_keys = check_missing(base_data, target_data)

            # 填充空字符串
            for k in missing_keys:
                target_data[k] = ""

            # 写回原 JSON 文件
            files = expand_pattern(self.cfg.base_dir, self.cfg.pattern, lang)
            for path in files:
                # 只写回 namespace 对应的键
                namespace = path.stem
                json_to_write = unflatten_json(target_data, namespace)
                bak_file = self.bak_dir / lang / path.name
                bak_file.parent.mkdir(parents=True, exist_ok=True)
                shutil.copy2(path, bak_file)  # 备份

                save_json(path, json_to_write)

            filled_counts[lang] = len(missing_keys)
            log_info(f"为语言 {lang} 补充了 {len(missing_keys)} 个缺失字段")

        return filled_counts
