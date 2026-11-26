#!/usr/bin/env python3
"""Ship the finished infographic to the grader's output directory.

The picture itself is rendered by draw.py (run it twice and the bytes
come out identical). This entry point does no drawing: it copies the
committed entry.png into the directory named by MAKEFUN_OUTPUT_DIR,
creating that directory first when it is missing.
"""

import os
import shutil
from pathlib import Path


def main() -> None:
    here = Path(__file__).resolve().parent
    out_dir = Path(os.environ.get("MAKEFUN_OUTPUT_DIR", "out"))
    out_dir.mkdir(parents=True, exist_ok=True)
    target = out_dir / "entry.png"
    shutil.copyfile(here / "entry.png", target)
    print(f"copied entry.png -> {target}")


if __name__ == "__main__":
    main()
