# pyright: standard

import json
from pathlib import Path
from typing import Any, Dict


def flatten_json(nested: Dict[str, Any], parent_key: str = "") -> Dict[str, str]:
    """
    扁平化嵌套 JSON 为一级字典，键使用 '.' 分隔每一层嵌套

    Args:
        nested (Dict[str, Any]): 原始嵌套字典
        parent_key (str): 递归时的前缀键，外部调用无需提供

    Returns:
        Dict[str, Any]: 扁平化后的字典
    """
    items: Dict[str, str] = {}

    for k, v in nested.items():
        new_key = f"{parent_key}.{k}" if parent_key else k

        if isinstance(v, dict):
            # 递归展开子字典
            items.update(flatten_json(v, new_key))
        else:
            # leaf 值直接添加
            items[new_key] = v

    return items


def load_json_file(path: Path) -> Dict[str, str]:
    """读取 JSON 文件并扁平化为一级字典"""

    with path.open("r", encoding="utf-8") as f:
        data = json.load(f)

    if not isinstance(data, dict):
        raise ValueError(f"JSON 文件内容必须是对象: {path}")

    namespace = path.stem
    return flatten_json(data, parent_key=namespace)
