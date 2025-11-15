# pyright: reportUnusedVariable=false
import argparse
from pathlib import Path

from i18n_toolbox.analysis.report_manager import ReportManager
from i18n_toolbox.config import I18nConfig, load_config
from i18n_toolbox.loader import I18nLoader


def main() -> None:
    """
    i18n_toolbox CLI 入口
    """
    parser = argparse.ArgumentParser(description="i18n 工具箱：整理、检查、分析 i18n JSON 文件")
    parser.add_argument(
        "-c", "--config", type=str, default="i18n_toolbox.toml", help="配置文件路径，默认为 i18n_toolbox.toml"
    )

    subparsers = parser.add_subparsers(dest="command", required=False)

    # --- scan 子命令 ---
    parser_scan = subparsers.add_parser("scan", help="扫描所有语言文件并加载")

    # --- check-missing 子命令 ---
    parser_missing = subparsers.add_parser("check-missing", help="检查不同语言间缺失的字段")
    parser_missing.add_argument("-b", "--base", required=True, type=str, help="基准语言代码，例如 en")
    parser_missing.add_argument("-t", "--target", default=None, nargs="+", type=str, help="目标语言代码，例如 zh ja ko")

    # --- check-duplicate 子命令 ---
    parser_duplicate = subparsers.add_parser("check-duplicate", help="检查字段重复性")

    # --- sync-order 子命令 ---
    parser_sync = subparsers.add_parser("sync-order", help="统一不同语言 JSON 的字段顺序")

    args = parser.parse_args()

    # --- 加载配置 ---
    cfg_path = Path(args.config)
    cfg: I18nConfig = load_config(cfg_path)
    loader = I18nLoader(cfg)
    all_data = loader.load_all()

    report_manager = ReportManager()

    # --- 根据子命令执行 ---
    command = args.command or "scan"
    if command == "scan":
        pass

    elif command == "check-missing":
        base_lang = args.base
        target_langs = args.target or [lang for lang in all_data.keys() if lang != base_lang]
        report_manager.run_missing_check(all_data, base=base_lang, target=target_langs)

    elif command == "check-duplicate":
        # check_duplicate(all_data)
        print("检查重复字段完成（示例输出）")

    elif command == "sync-order":
        # sync_field_order(all_data)
        print("字段顺序同步完成（示例输出）")


if __name__ == "__main__":
    main()
