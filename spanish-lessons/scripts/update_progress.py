#!/usr/bin/env python3
"""Обновление файлов после урока (ШАГ 7 скила) + статистика (ШАГ 5).

По результатам ПЕРВОГО квиза:
  - правильно  -> уровень += 1 (макс. 3), дата = дата урока;
  - неправильно/пропуск -> уровень не меняется, дата = дата урока.

Что делает:
  - переписывает только ячейки «Уровень» и «Последний повтор» для слов урока
    в words.md (остальные строки сохраняются дословно);
  - дописывает строки в answer-log.md (создаёт файл при отсутствии);
  - печатает статистику по уровням (сколько слов на 0/1/2/3).

Формат результатов — JSON-файл со списком объектов:
    [{"es": "Apto", "correct": true}, {"es": "Siendo", "correct": false}]
Поле es должно ТОЧНО совпадать с испанским из words.md.

Использование:
    python3 spanish-lessons/scripts/update_progress.py --results res.json [--date YYYY-MM-DD]
    # либо результаты из stdin:
    cat res.json | python3 spanish-lessons/scripts/update_progress.py --results -
    # предпросмотр без записи:
    python3 spanish-lessons/scripts/update_progress.py --results res.json --dry-run
"""

from __future__ import annotations

import argparse
import json
import sys

import lesson_lib as lib


def load_results(path: str) -> list[dict]:
    raw = sys.stdin.read() if path == "-" else open(path, encoding="utf-8").read()
    data = json.loads(raw)
    if not isinstance(data, list):
        raise SystemExit("Ошибка: результаты должны быть JSON-списком объектов {es, correct}.")
    for item in data:
        if "es" not in item or "correct" not in item:
            raise SystemExit(f"Ошибка: в записи нет полей es/correct: {item!r}")
    return data


def new_level(old: int, correct: bool) -> int:
    return min(old + 1, 3) if correct else old


def rewrite_words(results: dict[str, bool], date_iso: str, dry_run: bool) -> dict:
    words = lib.parse_words()
    by_es = {w["es"]: w for w in words}

    missing = [es for es in results if es not in by_es]
    if missing:
        raise SystemExit(
            "Ошибка: эти слова не найдены в words.md (проверь точное написание):\n  "
            + "\n  ".join(missing)
        )

    lines = lib.WORDS_PATH.read_text(encoding="utf-8").splitlines()
    changes = []
    for es, correct in results.items():
        w = by_es[es]
        nl = new_level(w["lvl"], correct)
        new_line = f"| {w['es']} | {w['ru']} | {nl} | {date_iso} | {w['mnem']} |"
        lines[w["lineno"]] = new_line
        changes.append((es, w["lvl"], nl))

    if not dry_run:
        lib.WORDS_PATH.write_text("\n".join(lines) + "\n", encoding="utf-8")

    # статистика по уровням после обновления
    counts = {0: 0, 1: 0, 2: 0, 3: 0}
    for w in words:
        lvl = new_level(w["lvl"], results[w["es"]]) if w["es"] in results else w["lvl"]
        counts[lvl] += 1

    return {"changes": changes, "counts": counts}


def append_log(results: list[dict], date_iso: str, dry_run: bool):
    header = "# Лог ответов\n\n| Дата | Испанский | Результат |\n|------|-----------|:---------:|\n"
    if not lib.LOG_PATH.exists():
        if not dry_run:
            lib.LOG_PATH.write_text(header, encoding="utf-8")
        existing = header
    else:
        existing = lib.LOG_PATH.read_text(encoding="utf-8")

    new_lines = []
    for item in results:
        mark = lib.CORRECT if item["correct"] else lib.WRONG
        new_lines.append(f"| {date_iso} | {item['es']} | {mark} |")

    if not dry_run:
        sep = "" if existing.endswith("\n") else "\n"
        lib.LOG_PATH.write_text(existing + sep + "\n".join(new_lines) + "\n", encoding="utf-8")
    return new_lines


def main():
    ap = argparse.ArgumentParser(description="Обновление прогресса после урока")
    ap.add_argument("--results", required=True, help="путь к JSON с результатами или '-' для stdin")
    ap.add_argument("--date", help="дата урока YYYY-MM-DD (по умолчанию сегодня)")
    ap.add_argument("--dry-run", action="store_true", help="показать изменения, ничего не записывая")
    args = ap.parse_args()

    date_iso = lib.parse_cli_date(args.date).isoformat()
    results_list = load_results(args.results)
    results_map = {item["es"]: bool(item["correct"]) for item in results_list}

    res = rewrite_words(results_map, date_iso, args.dry_run)
    log_lines = append_log(results_list, date_iso, args.dry_run)

    tag = "[DRY-RUN] " if args.dry_run else ""
    print(f"{tag}Дата урока: {date_iso}")
    print(f"{tag}Обновлено слов в words.md: {len(res['changes'])}")
    for es, old, nl in res["changes"]:
        arrow = f"{old}→{nl}" if old != nl else f"{nl} (без изменений)"
        print(f"  {es:42s} уровень {arrow}")
    print(f"{tag}Добавлено строк в answer-log.md: {len(log_lines)}")
    c = res["counts"]
    print(f"\nСтатистика по уровням: 0={c[0]}  1={c[1]}  2={c[2]}  3={c[3]}")


if __name__ == "__main__":
    main()
