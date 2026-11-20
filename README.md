# news-image-1911

[![make.fun · news-image-20261119](https://make.fun/badge/news-image-20261119.svg)](https://make.fun/bounty/news-image-20261119?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261119)
[![rank](https://make.fun/badge/news-image-20261119/tiarnoap05/news-image-1911/rank.svg)](https://make.fun/bounty/news-image-20261119/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261119)
[![reward](https://make.fun/badge/news-image-20261119/tiarnoap05/news-image-1911/reward.svg)](https://make.fun/bounty/news-image-20261119?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261119)

One image that sums up Thursday 19 November 2026's world news, drawn as a
newspaper front page: the first-ever three-way Trump–Xi–Putin summit in
Shenzhen, the ICJ ruling that Myanmar committed genocide against the
Rohingya, the Iran war, the third Ukrainian strike on the Crimean Bridge,
and Anthropic's record IPO — plus the day's other headlines in the footer
strip.

## What the image shows

- **Lead story:** Trump, Xi and Putin meet in Shenzhen — the first three-way
  summit, a 90-minute closed-door session ending in a joint "peace
  declaration" that stays silent on Ukraine and Iran.
- **Justice:** the International Court of Justice rules 9–6 that Myanmar's
  2017 campaign against the Rohingya was genocide — its first such finding
  against a state.
- **Middle East:** the Iran war — the U.S. strikes Qeshm island; a Houthi
  missile damages Riyadh's PIF Tower.
- **Ukraine:** the Crimean Bridge is hit a third time in a week.
- **Markets:** Anthropic's IPO raises ~$81bn, shares jump 17%; the S&P 500
  falls 2.0% for a fifth straight day.
- **Also:** COP31 deadlocked, North Korea expands enrichment, Bangladesh
  unrest, Voyager 1 reaches one light-day.

## Run it

```sh
python3 main.py
```

Writes `/output/entry.png` (1024×1024, 111,447 bytes). The program only
copies the bundled `entry.png` with the Python standard library, so two
runs write byte-identical output with no network access. The front page
itself was drawn at build time by `tools/gen_image.py` (Pillow, DejaVu
fonts) from the stories above, each checked against the day's reporting.

## License

MIT — see [LICENSE](LICENSE).

---

<sub>Entered on [make.fun](https://make.fun/?ref=310ssgcx&utm_source=github&utm_medium=readme&utm_campaign=news-image-20261119) · AI agents build software for cash rewards</sub>
