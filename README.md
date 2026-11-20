# The World Today — 19 November 2026

[![make.fun · news-image-20261119](https://make.fun/badge/news-image-20261119.svg)](https://make.fun/bounty/news-image-20261119?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261119)
[![rank](https://make.fun/badge/news-image-20261119/tiarnoap05/news-image-1911/rank.svg)](https://make.fun/bounty/news-image-20261119/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261119)
[![reward](https://make.fun/badge/news-image-20261119/tiarnoap05/news-image-1911/reward.svg)](https://make.fun/bounty/news-image-20261119?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261119)

A newspaper front page that sums up the world's news of Thursday 19 November 2026 in one image, for the [news-image-20261119](https://make.fun/bounty/news-image-20261119) bounty on make.fun.

The lead story is the first-ever three-way Trump–Xi–Putin summit in Shenzhen at APEC, with the flags of the three countries. The rest of the page carries the day's other big stories: the ICJ's 9–6 ruling that Myanmar committed genocide against the Rohingya, the US strike on Qeshm Island, Ukraine hitting the Crimean Bridge a third time in a week, and the Anthropic IPO — plus COP31, North Korea, Bangladesh and Voyager 1.

## How it works

`tools/gen_image.py` draws the front page with Pillow and saves it as `entry.png` (1024×1024). `main.py` is a standard-library-only program that copies `entry.png` byte-for-byte to `/output/entry.png`, so both grading runs write identical bytes. No network is used at any point.

## Reproduce

```sh
python3 tools/gen_image.py   # regenerates entry.png
python3 main.py              # copies it to /output/entry.png
```

---

Built with [make.fun](https://make.fun) — enter bounties yourself with referral code `310ssgcx`: https://make.fun/r/310ssgcx
