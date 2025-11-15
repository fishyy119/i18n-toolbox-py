from pathlib import Path
from typing import Dict


def fill_missing_fields(base_data: Dict[str, str], target_path: Path) -> int:
    """
    根据基准语言填充目标语言缺失字段，值设为空字符串

    Args:
        base_data (Dict[str, str]): 基准语言的扁平化数据
        target_path (Path): 目标语言 JSON 文件路径

    Returns:
        int: 填充的字段数量
    """
    import json

    if not target_path.exists():
        raise FileNotFoundError(f"目标语言文件不存在: {target_path}")

    # 读取目标语言原始 JSON
    with target_path.open("r", encoding="utf-8") as f:
        target_data = json.load(f)

    # 扁平化目标语言 JSON（如果尚未扁平化，需要使用你的扁平化工具）
    # 这里假设 target_data 已经是扁平化的 { "namespace.key": "value", ... }
    missing_keys = [k for k in base_data if k not in target_data]

    for k in missing_keys:
        target_data[k] = ""  # 自动填充空字符串

    # 写回原 JSON，保持可读缩进
    with target_path.open("w", encoding="utf-8") as f:
        json.dump(target_data, f, ensure_ascii=False, indent=2)

    return len(missing_keys)
