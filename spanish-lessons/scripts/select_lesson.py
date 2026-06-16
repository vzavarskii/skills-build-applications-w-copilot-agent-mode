#!/usr/bin/env python3
"""Анализ лога и подбор слов для урока (ШАГ 2 скила).

Считает стабильность, интервалы и счётчики БЕЗ ручной арифметики и выводит:
  - сколько новых слов (уровень 0) и их список с переводом/мнемоникой;
  - нестабильные слова (уровень >= 1) с историей последних попыток;
  - кандидатов на обычный повтор, отсортированных по правилу;
  - готовый предлагаемый состав урока (10 слотов).

Педагогический подбор новых слов (когнаты, ШАГ 3) и чередование тем (ШАГ 4)
скрипт НЕ выполняет — это остаётся за репетитором. Скрипт даёт данные и
дефолтный состав, который репетитор при необходимости корректирует.

Использование:
    python3 spanish-lessons/scripts/select_lesson.py [--date YYYY-MM-DD] [--size 10]
    python3 spanish-lessons/scripts/select_lesson.py --json   # машинный вывод
"""

from __future__ import annotations

import argparse
import json

import lesson_lib as lib


def build(date, size):
    words = lib.parse_words()
    log = lib.parse_log()
    hist = lib.history_by_word(log)

    new_words = [w for w in words if w["lvl"] == 0]

    unstable = []
    for w in words:
        if lib.is_unstable(w, hist):
            h = hist.get(w["es"], [])
            last3 = h[-3:]
            unstable.append(
                {
                    **w,
                    "last3": last3,
                    "fails3": sum(1 for r in last3 if r == lib.WRONG),
                    "days": lib.days_since(w["last"], date),
                }
            )
    # приоритет нестабильных: больше недавних ошибок -> дольше не повторялись -> ниже уровень
    unstable.sort(key=lambda x: (-x["fails3"], -x["days"], x["lvl"]))

    review = []
    for w in words:
        if w["lvl"] in (1, 2):
            days = lib.days_since(w["last"], date)
            if days >= 3:
                h = hist.get(w["es"], [])
                review.append(
                    {
                        **w,
                        "days": days,
                        "last_result": h[-1] if h else None,
                    }
                )
    # сначала дольше не повторявшиеся, затем меньший уровень, затем ❌ в последней попытке
    review.sort(
        key=lambda x: (-x["days"], x["lvl"], 0 if x["last_result"] == lib.WRONG else 1)
    )

    # --- дефолтный состав урока ---
    n_new = len(new_words)
    reserved = 3 if n_new >= 3 else n_new

    chosen, seen = [], set()

    def take(word, role):
        if word["es"] in seen:
            return
        seen.add(word["es"])
        chosen.append({"es": word["es"], "ru": word["ru"], "lvl": word["lvl"], "role": role})

    for w in new_words[:reserved]:
        take(w, "новое")
    for w in unstable[:4]:
        if len(chosen) >= size:
            break
        take(w, "нестабильное")
    for w in review:
        if len(chosen) >= size:
            break
        take(w, "повтор")
    for w in new_words[reserved:]:  # добор новыми
        if len(chosen) >= size:
            break
        take(w, "новое (добор)")

    return {
        "date": date.isoformat(),
        "size": size,
        "new_count": n_new,
        "reserved_new": reserved,
        "new_words": new_words,
        "unstable": unstable,
        "review": review,
        "suggested": chosen[:size],
    }


def print_human(r):
    print(f"=== Подбор урока на {r['date']} (слотов: {r['size']}) ===\n")

    print(f"НОВЫЕ СЛОВА (уровень 0): {r['new_count']}, зарезервировано {r['reserved_new']}")
    for w in r["new_words"]:
        print(f"  🆕 {w['es']}  |  {w['ru']}  |  {w['mnem']}")
    print()

    print(f"НЕСТАБИЛЬНЫЕ (уровень >= 1): {len(r['unstable'])}  (показаны первые 20 по приоритету)")
    for w in r["unstable"][:20]:
        print(
            f"  {w['es']:42s} lvl={w['lvl']} дней={w['days']:>4} последние3={''.join(w['last3']) or '—'}"
        )
    print()

    print(f"КАНДИДАТЫ НА ПОВТОР (уровень 1-2, >=3 дней): {len(r['review'])}  (первые 15)")
    for w in r["review"][:15]:
        lr = w["last_result"] or "—"
        print(f"  {w['es']:42s} lvl={w['lvl']} дней={w['days']:>4} посл.={lr}")
    print()

    print("=== ПРЕДЛАГАЕМЫЙ СОСТАВ (черновик — примени ШАГ 3 когнаты и ШАГ 4 чередование) ===")
    for i, w in enumerate(r["suggested"], 1):
        print(f"  {i:2}. {w['es']:42s} [{w['role']}]")
    print(
        "\nНапоминание: новые слова можно заменить на более удачные когнаты из списка выше;"
        "\nесли все повторы из одной темы — заменить 1-2 словами другой темы."
    )


def main():
    ap = argparse.ArgumentParser(description="Подбор слов для урока испанского")
    ap.add_argument("--date", help="дата урока YYYY-MM-DD (по умолчанию сегодня)")
    ap.add_argument("--size", type=int, default=10, help="размер урока (по умолчанию 10)")
    ap.add_argument("--json", action="store_true", help="машинный JSON-вывод")
    args = ap.parse_args()

    date = lib.parse_cli_date(args.date)
    r = build(date, args.size)

    if args.json:
        print(json.dumps(r, ensure_ascii=False, indent=2))
    else:
        print_human(r)


if __name__ == "__main__":
    main()
