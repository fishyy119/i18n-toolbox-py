# pyright: standard

from typing import Dict, List

from ..utils.console import log_warn


def lang_scan(
    all_data: Dict[str, Dict[str, str]],
    targets: List[str],
) -> Dict[str, Dict]:
    res = {}
    report_by_lang = {}
    report_by_ns = {}

    for lang in targets:
        if lang not in all_data:
            log_warn(f"语言 {lang} 不存在于数据中，跳过")
            continue

        data = all_data[lang]
        if not data:
            log_warn(f"语言 {lang} 数据为空")

        res[f"{lang}_scan.json"] = data

        ns_count: Dict[str, int] = {}
        for key in data.keys():
            namespace = key.split(".")[0]
            ns_count[namespace] = ns_count.get(namespace, 0) + 1

            # 构建按 namespace 索引的总报告
            if namespace not in report_by_ns:
                report_by_ns[namespace] = {}
            report_by_ns[namespace][lang] = ns_count[namespace]

        report_by_lang[lang] = {
            "field_count": len(data),
            "fields": ns_count,
        }

    res["scan_report_lang.json"] = report_by_lang
    res["scan_report_ns.json"] = report_by_ns
    return res
