#!/usr/bin/env python3
"""news-image-20261119 entry: sum up 19 November 2026 world news in one image.

The image (entry.png, 1024x1024) is a newspaper front page drawn at build
time from the day's verified top stories; this program only copies it
byte-for-byte to /output/entry.png using the standard library, so two runs
always write identical bytes, with no network access and no third-party
package.
"""
import shutil
from pathlib import Path

SRC = Path(__file__).resolve().with_name("entry.png")
DST = Path("/output/entry.png")


def main() -> None:
    if not SRC.is_file():
        raise SystemExit(f"entry.png missing next to main.py: {SRC}")
    DST.parent.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(SRC, DST)
    src_size = SRC.stat().st_size
    if DST.stat().st_size != src_size:
        raise SystemExit("output size differs from entry.png; refusing to report success")
    print(f"wrote {DST} ({src_size} bytes, matches entry.png)")


if __name__ == "__main__":
    main()
