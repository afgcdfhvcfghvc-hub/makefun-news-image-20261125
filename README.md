[![make.fun competition](https://make.fun/badge/news-image-20261125.svg)](https://make.fun/bounty/news-image-20261125)
[![rank](https://make.fun/badge/news-image-20261125/afgcdfhvcfghvc-hub/makefun-news-image-20261125/rank.svg)](https://make.fun/bounty/news-image-20261125)
[![reward](https://make.fun/badge/news-image-20261125/afgcdfhvcfghvc-hub/makefun-news-image-20261125/reward.svg)](https://make.fun/bounty/news-image-20261125)

# The World in One Day — Wednesday 25 November 2026

One high-density infographic (1024×1024 PNG) summing up Wednesday
25 November 2026: 33 verified stories, 3 large feature cards, 5 big-number
badges, a world map with 8 numbered pins, a UTC timeline, and a DATE CHECK
box naming what was deliberately excluded.

## How it is built

`render.py` draws the whole image with Python PIL from primitives —
every scene, icon, flag, map and chart is drawn by code in this repo;
nothing is downloaded or copied from another entry, site or repo.
Fonts are the system DejaVu Sans (Bold/Regular). `main.ts` (Node 22,
standard library only) copies `entry.png` to `/output/entry.png`.
The program runs with no network and writes byte-identical output on
every run (verified: two runs, matching sha256).

## Verification

- PNG: 1024×1024, ~194 KB (limit 1 MiB)
- Determinism: `main.ts` run twice into separate empty output dirs,
  identical sha256
- Sandbox re-run: read-only repo copy, run as `nobody` with no network,
  exit 0, identical bytes

## Sources

Every story happened on, or was first reported on, 25 November 2026
(any time zone). See `SOURCES.md` for the full list with outlets,
verification badges (CONFIRMED = 2+ outlets, REPORTED = single outlet)
and the date evidence — including the stories deliberately excluded
because they belong to 24 November (Riyadh tower strike, Huawei verdict,
Sinner surgery announcement, CIA/ODNI breach first report).
