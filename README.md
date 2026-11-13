# 2 + 2 = 5

A tiny Python pixel-art project that draws **`2 + 2 = 5`** on the GitHub contribution graph using one dated commit per active pixel.

> This project targets **January 1, 2025 through December 31, 2025 only**. It does not generate dates in 2026.

## How it works

GitHub's contribution graph is a calendar: columns are weeks and rows are weekdays. This project uses a compact 3×5 bitmap font and maps its five pixel rows to Monday–Friday. Saturday and Sunday remain blank. The phrase is centered horizontally in the 53-week calendar grid for 2025.

- Phrase: `2 + 2 = 5`
- Target year: **2025**
- Date range: **2025-01-01 … 2025-12-31** (inclusive)
- Pixel font: 3×5
- Commits: **one empty commit per active pixel**
- Default behavior: preview only; no commits are created unless `--execute` is supplied
- No third-party Python dependencies

## Requirements

- Python 3.10+
- Git
- A GitHub account
- A verified email address configured for Git commits and associated with your GitHub account

## Quick start

Clone your repository, then run:

```bash
git clone https://github.com/aminhassanpour1999/2-plus-2-equals-5.git
cd 2-plus-2-equals-5
python3 two_plus_two.py
```

The default command prints a preview and the exact planned dates. It does not modify Git history.

To create the dated commits locally:

```bash
python3 two_plus_two.py --execute
```

Then inspect the result:

```bash
git log --format="%h %aI %s" -n 10
git status
```

When you are satisfied, push the branch:

```bash
git push origin main
```

## Important GitHub contribution requirements

For commits to appear on your profile, GitHub's contribution rules must be satisfied. In particular:

1. The commits must use an email address associated with your GitHub account.
2. The commits must be reachable from the repository's default branch (or another qualifying branch / qualifying pull request).
3. The repository must be public, unless your private-contribution display is enabled.
4. GitHub determines contribution dates from commit metadata; verify the year selector on your profile after pushing.

This project deliberately creates **synthetic empty commits** for a pixel-art experiment. They do not represent software work performed on those dates, and GitHub may change how it displays or counts contributions. Do not present the graph as a record of actual work.

## Safety

- Preview first. The script is dry-run by default.
- `--execute` creates local empty commits. It does not push.
- The script refuses to run outside a Git repository and refuses to proceed if the working tree is not clean.
- It checks that every generated commit date falls within 2025.
- It never resets, rewrites, or deletes existing history.

## Project structure

```text
.
├── README.md
├── LICENSE
├── .gitignore
├── two_plus_two.py
└── tests
    └── test_two_plus_two.py
```

## License

MIT. See [LICENSE](LICENSE).
