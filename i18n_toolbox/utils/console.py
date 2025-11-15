# pyright: standard

from typing import Literal

Color = Literal["red", "green", "yellow", "blue", "magenta", "cyan", "white", "reset"]

COLOR_CODES: dict[Color, str] = {
    "red": "\033[31m",
    "green": "\033[32m",
    "yellow": "\033[33m",
    "blue": "\033[34m",
    "magenta": "\033[35m",
    "cyan": "\033[36m",
    "white": "\033[37m",
    "reset": "\033[0m",
}


def cprint(*args, color: Color = "reset", **kwargs) -> None:
    """
    彩色打印文本，兼容原生 print 的所有参数
    """
    sep: str = kwargs.pop("sep", " ")
    text = sep.join(str(arg) for arg in args)
    colored_text = f"{COLOR_CODES.get(color, COLOR_CODES['reset'])}{text}{COLOR_CODES['reset']}"
    print(colored_text, **kwargs)


def log_info(*args, **kwargs) -> None:
    """信息消息，绿色"""
    cprint("[INFO]", *args, color="green", **kwargs)


def log_warn(*args, **kwargs) -> None:
    """警告消息，黄色"""
    cprint("[WARN]", *args, color="yellow", **kwargs)


def log_error(*args, **kwargs) -> None:
    """错误消息，红色"""
    cprint("[ERROR]", *args, color="red", **kwargs)


def log_debug(*args, **kwargs) -> None:
    """调试消息，蓝色"""
    cprint("[DEBUG]", *args, color="blue", **kwargs)
