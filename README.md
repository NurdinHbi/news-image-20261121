[![make.fun · news-image-20261121](https://make.fun/badge/news-image-20261121.svg)](https://make.fun/bounty/news-image-20261121?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261121) [![rank](https://make.fun/badge/news-image-20261121/NurdinHbi/news-image-20261121/rank.svg)](https://make.fun/bounty/news-image-20261121/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261121) [![reward](https://make.fun/badge/news-image-20261121/NurdinHbi/news-image-20261121/reward.svg)](https://make.fun/bounty/news-image-20261121?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261121) [![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE) [![Node](https://img.shields.io/badge/Node-22%2B-green)](main.ts) [![Python](https://img.shields.io/badge/Python-3-blue)](generate_poster.py)

# The World Today — 21 November 2026 in one image

A newspaper front page drawn entirely in code (PIL shapes + text, no photos,
no downloads) summing up Saturday 21 November 2026 in six panels: Mexico
captures "El Chapo Isidro", drones hit the Russian ship Sparta II in the
Baltic, a missile hits Zelensky's hometown Kryvyi Rih, the AI sell-off drags
markets down, COP31 talks run past their deadline, and French protests ebb.

## Run it

```sh
python3 generate_poster.py   # writes entry.png (1024x1024, deterministic)
mkdir -p out && MAKEFUN_OUTPUT_DIR=out node main.ts
```

`main.ts` copies the generated `entry.png` to `$MAKEFUN_OUTPUT_DIR/entry.png`
(`output` by default). Running the generator twice produces byte-identical
output; there are no network calls at runtime.

## The six stories

1. **MEXICO** — Mexico nabs "El Chapo Isidro": FBI Top 10 fugitive seized in Sinaloa.
2. **BALTIC** — Drones hit Russian ship Sparta II; it burns and drifts into Finnish waters.
3. **UKRAINE** — Missile hits Zelensky's hometown Kryvyi Rih: 2 killed, 60 wounded.
4. **MARKETS** — AI sell-off drags markets down: S&P -3.7%, Nikkei -5.1%.
5. **CLIMATE** — COP31 talks run past deadline in Antalya, stalled over fossil fuels.
6. **FRANCE** — French protests ebb: 82,500 march over living costs, turnout down.

All six were first reported on Saturday 21 November 2026.
