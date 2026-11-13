#!/usr/bin/env python3
"""Draw '2 + 2 = 5' on the 2025 GitHub contribution graph.

The program is a dry-run by default. Pass --execute to create one local
empty Git commit for each active pixel. It never pushes or rewrites history.
"""

from __future__ import annotations

import argparse
import os
import subprocess
import sys
from datetime import date, datetime, time, timedelta, timezone
from typing import Iterable

TARGET_YEAR = 2025
PHRASE = "2 + 2 = 5"
FIRST_SUNDAY = date(2024, 12, 29)  # First calendar column shown for 2025.
CALENDAR_WEEKS = 53
FONT: dict[str, tuple[str, ...]] = {
    "2": ("111", "001", "111", "100", "111"),
    "+": ("000", "010", "111", "010", "000"),
    "=": ("000", "111", "000", "111", "000"),
    "5": ("111", "100", "111", "001", "111"),
}


def build_bitmap() -> tuple[tuple[int, ...], ...]:
    """Return a 5-row bitmap for the phrase, with one blank column between glyphs."""
    rows: list[list[int]] = [[] for _ in range(5)]
    glyphs = [FONT[ch] for ch in PHRASE if ch != " "]
    for index, glyph in enumerate(glyphs):
        if index:
            for row in rows:
                row.append(0)
        for row_index, line in enumerate(glyph):
            rows[row_index].extend(int(pixel) for pixel in line)
    return tuple(tuple(row) for row in rows)


def phrase_start_column(bitmap_width: int | None = None) -> int:
    """Center the phrase in the 53-week contribution calendar."""
    width = bitmap_width if bitmap_width is not None else len(build_bitmap()[0])
    return (CALENDAR_WEEKS - width) // 2


def active_pixel_dates() -> list[date]:
    """Map active bitmap pixels to Monday–Friday dates in calendar year 2025."""
    bitmap = build_bitmap()
    start_column = phrase_start_column(len(bitmap[0]))
    planned: list[date] = []

    for row_index, row in enumerate(bitmap):
        for column_index, pixel in enumerate(row):
            if not pixel:
                continue
            # The graph's first column starts Sunday; row 0 is Monday (+1 day).
            pixel_date = FIRST_SUNDAY + timedelta(
                days=(start_column + column_index) * 7 + row_index + 1
            )
            if pixel_date.year != TARGET_YEAR:
                raise ValueError(f"Pixel date escaped target year: {pixel_date}")
            planned.append(pixel_date)

    return sorted(planned)


def is_git_repository() -> bool:
    result = subprocess.run(
        ["git", "rev-parse", "--is-inside-work-tree"],
        capture_output=True,
        text=True,
        check=False,
    )
    return result.returncode == 0 and result.stdout.strip() == "true"


def ensure_clean_worktree() -> None:
    result = subprocess.run(
        ["git", "status", "--porcelain"],
        capture_output=True,
        text=True,
        check=True,
    )
    if result.stdout.strip():
        raise RuntimeError(
            "Working tree is not clean. Commit or stash your changes before --execute."
        )


def create_empty_commit(commit_date: date, index: int, total: int) -> None:
    """Create one local empty commit with author and committer dates in 2025."""
    timestamp = datetime.combine(
        commit_date, time(hour=12), tzinfo=timezone.utc
    ).isoformat()
    env = os.environ.copy()
    env["GIT_AUTHOR_DATE"] = timestamp
    env["GIT_COMMITTER_DATE"] = timestamp

    subprocess.run(
        [
            "git",
            "commit",
            "--allow-empty",
            "-m",
            f"pixel: {index:03d}/{total:03d} for {TARGET_YEAR}",
        ],
        env=env,
        check=True,
    )


def preview(dates: Iterable[date]) -> None:
    dates = list(dates)
    print(f"Phrase:       {PHRASE}")
    print(f"Target year:  {TARGET_YEAR}")
    print(f"Date range:   {TARGET_YEAR}-01-01 through {TARGET_YEAR}-12-31")
    print(f"Bitmap:       {len(build_bitmap()[0])} columns × 5 rows")
    print(f"Active pixels / planned commits: {len(dates)}")
    if dates:
        print(f"First pixel:  {dates[0].isoformat()}")
        print(f"Last pixel:   {dates[-1].isoformat()}")
    print("\nDry run only. No Git history was changed.")
    print("Use --execute to create the local empty commits.")


def main() -> int:
    parser = argparse.ArgumentParser(
        description=f"Draw {PHRASE!r} on the {TARGET_YEAR} GitHub contribution graph."
    )
    parser.add_argument(
        "--execute",
        action="store_true",
        help="Create local empty commits (does not push to GitHub).",
    )
    args = parser.parse_args()

    dates = active_pixel_dates()
    if not args.execute:
        preview(dates)
        return 0

    if not is_git_repository():
        print("Error: run this script inside a Git repository.", file=sys.stderr)
        return 2

    try:
        ensure_clean_worktree()
        for index, commit_date in enumerate(dates, start=1):
            create_empty_commit(commit_date, index, len(dates))
    except (RuntimeError, subprocess.CalledProcessError) as exc:
        print(f"Error: {exc}", file=sys.stderr)
        return 1

    print(f"Created {len(dates)} local empty commits dated within {TARGET_YEAR}.")
    print("Nothing was pushed. Review the history, then push manually when ready.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
