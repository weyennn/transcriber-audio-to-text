from html import escape
from typing import Any


def format_time(seconds: float) -> str:
    minutes, seconds = divmod(int(seconds), 60)
    return f"{minutes:02d}:{seconds:02d}"


def srt_time(seconds: float) -> str:
    hours = int(seconds // 3600)
    minutes = int((seconds % 3600) // 60)
    whole_seconds = int(seconds % 60)
    milliseconds = int((seconds - int(seconds)) * 1000)
    return f"{hours:02d}:{minutes:02d}:{whole_seconds:02d},{milliseconds:03d}"


def safe_html(value: Any) -> str:
    return escape(str(value), quote=True)


def bars(level: int, total: int = 5) -> str:
    return "".join(
        (
            '<span class="bar-fill"></span>'
            if i < level
            else '<span class="bar-empty"></span>'
        )
        for i in range(total)
    )
