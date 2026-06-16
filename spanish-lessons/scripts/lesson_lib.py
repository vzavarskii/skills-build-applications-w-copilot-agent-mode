"""Общие утилиты для скриптов урока испанского.

Парсинг `words.md` и `answer-log.md`, расчёт стабильности и интервалов.
Пути к данным вычисляются относительно расположения скрипта, поэтому
скрипты можно запускать из любой директории.
"""

from __future__ import annotations

import datetime as _dt
from pathlib import Path
from typing import Optional

# spanish-lessons/scripts/lesson_lib.py -> spanish-lessons/
DATA_DIR = Path(__file__).resolve().parent.parent
WORDS_PATH = DATA_DIR / "words.md"
LOG_PATH = DATA_DIR / "answer-log.md"

CORRECT = "✅"
WRONG = "❌"


def is_separator(line: str) -> bool:
    """True, если строка таблицы — разделитель вида |---|:--:|."""
    body = line.strip()
    return body.startswith("|") and set(body) <= set("|-: ")


def is_header(line: str) -> bool:
    return "Испанский" in line or "Дата" in line


def split_row(line: str) -> list[str]:
    """Разбить строку markdown-таблицы на ячейки (без крайних пайпов)."""
    return [c.strip() for c in line.strip().split("|")[1:-1]]


def parse_date(s: str) -> Optional[_dt.date]:
    s = s.strip()
    if not s or s == "—":
        return None
    y, m, d = (int(x) for x in s.split("-"))
    return _dt.date(y, m, d)


def parse_words(path: Path = WORDS_PATH) -> list[dict]:
    """Вернуть список слов. Каждое: es, ru, lvl, last(str), mnem, lineno(0-based)."""
    rows = []
    for i, line in enumerate(path.read_text(encoding="utf-8").splitlines()):
        if not line.strip().startswith("|"):
            continue
        if is_header(line) or is_separator(line):
            continue
        cells = split_row(line)
        if len(cells) < 5:
            continue
        es, ru, lvl, last, mnem = cells[:5]
        try:
            lvl = int(lvl)
        except ValueError:
            continue
        rows.append(
            {"es": es, "ru": ru, "lvl": lvl, "last": last, "mnem": mnem, "lineno": i}
        )
    return rows


def parse_log(path: Path = LOG_PATH) -> list[dict]:
    """Вернуть записи лога в порядке файла: date(str), es, res."""
    if not path.exists():
        return []
    rows = []
    for line in path.read_text(encoding="utf-8").splitlines():
        if not line.strip().startswith("|"):
            continue
        if is_header(line) or is_separator(line):
            continue
        cells = split_row(line)
        if len(cells) < 3:
            continue
        rows.append({"date": cells[0], "es": cells[1], "res": cells[2]})
    return rows


def history_by_word(log_rows: list[dict]) -> dict[str, list[str]]:
    """es -> список результатов в хронологическом порядке."""
    hist: dict[str, list[str]] = {}
    for row in log_rows:
        hist.setdefault(row["es"], []).append(row["res"])
    return hist


def is_unstable(word: dict, hist: dict[str, list[str]]) -> bool:
    """Слово (уровень >= 1) нестабильно: < 3 записей или хоть один ❌ в последних 3."""
    if word["lvl"] < 1:
        return False
    h = hist.get(word["es"], [])
    last3 = h[-3:]
    return len(h) < 3 or any(r == WRONG for r in last3)


def days_since(last: str, today: _dt.date) -> int:
    d = parse_date(last)
    if d is None:
        return 10**6
    return (today - d).days


def today() -> _dt.date:
    return _dt.date.today()


def parse_cli_date(s: Optional[str]) -> _dt.date:
    if not s:
        return today()
    y, m, d = (int(x) for x in s.split("-"))
    return _dt.date(y, m, d)
