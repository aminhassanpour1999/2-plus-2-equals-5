# Design and calendar mapping

## Fixed target

The project is intentionally scoped to the calendar year **2025**:

- First date allowed: `2025-01-01`
- Last date allowed: `2025-12-31`
- Target calendar columns: 53
- Phrase: `2 + 2 = 5`

No 2026 dates are part of the design or generated commit plan.

## Pixel font

Each symbol uses a 3-column × 5-row bitmap. The five glyph instances are:

- `2`
- `+`
- `=`
- `5`

The phrase has five glyphs and four one-column separators, so its total width is:

`(5 × 3) + (4 × 1) = 19 columns`

The phrase is centered in the 53-column calendar:

`floor((53 - 19) / 2) = 17`

So the first phrase column is calendar column 17 (zero-based).

## Weekday mapping

GitHub's contribution calendar is arranged Sunday through Saturday. The script maps the five bitmap rows to Monday through Friday:

| Bitmap row | Calendar weekday |
| --- | --- |
| 0 | Monday |
| 1 | Tuesday |
| 2 | Wednesday |
| 3 | Thursday |
| 4 | Friday |

Saturday and Sunday are never assigned pixels.

The first displayed Sunday column for the 2025 calendar is December 29, 2024. This is only a calendar-grid anchor; no pixel is placed on a 2024 date. With the phrase centered, active pixels fall between **April 28, 2025 and September 5, 2025**.

## Commit count

The bitmap contains **44 active pixels**, therefore the script plans exactly **44 commits**. Each active pixel maps to one unique weekday date. Every planned date is validated to be in 2025 before any commit is created.

## Why the commits are empty

A contribution graph is a calendar visualization, not a pixel API. The project uses empty Git commits with explicit author and committer timestamps to represent active pixels. This is an artificial visual experiment, not a record of work completed on those dates.

The generator defaults to preview mode. The `--execute` flag creates commits locally only; pushing is always a separate, manual action.
