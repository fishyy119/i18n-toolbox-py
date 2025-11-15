from __future__ import annotations

from typing import Dict

from .config import I18nConfig
from .utils.json_tools import load_json_file
from .utils.path import expand_pattern


class I18nLoader:
    """
    Load and manage i18n files according to configuration.
    """

    def __init__(self, cfg: I18nConfig):
        self.cfg = cfg

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

        return all_data

    # def save_language(
    #     self,
    #     lang: str,
    #     data: dict[str, dict[str, Any]],
    #     *,
    #     sort_keys: bool = True,
    # ) -> None:
    #     """
    #     Save modified language data back to files.
    #     """

    #     for namespace, tree in data.items():
    #         path = self.cfg.base_dir / self.cfg.pattern.replace("{lang}", lang).split("/*")[0] / f"{namespace}.json"
    #         path.parent.mkdir(parents=True, exist_ok=True)
    #         save_json(path, tree, sort_keys=sort_keys)
