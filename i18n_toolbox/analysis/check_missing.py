from typing import Dict, List


def check_missing(
    base_lang: Dict[str, str],  # 基准语言，键为 namespace.嵌套键
    target_lang: Dict[str, str],  # 待检查语言
) -> List[str]:
    """
    检查 target_lang 相对于 base_lang 缺失的字段

    Args:
        base_lang (Dict[str, str]): 基准语言扁平化字典
        target_lang (Dict[str, str]): 待检查语言扁平化字典

    Returns:
        List[str]: 缺失字段列表
    """
    missing_keys: List[str] = []

    for key in base_lang.keys():
        if key not in target_lang:
            missing_keys.append(key)

    return missing_keys
