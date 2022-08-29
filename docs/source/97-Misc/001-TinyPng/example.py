# -*- coding: utf-8 -*-

import mpire
import subprocess
from pathlib import Path

bin_pngquant = Path.home() / "pngquant" / "pngquant"


def compress_image(in_path: Path, out_path):
    print(f"compress image from {in_path}")
    print(f"  to {out_path}")
    subprocess.run([
        bin_pngquant, "8", str(in_path),
        "--quality", "0-70",
        "--output", str(out_path),
    ])


dir_here = Path(__file__).absolute().parent
dir_before = dir_here / "before"
dir_after = dir_here / "after"
dir_after.mkdir(parents=True, exist_ok=True)

args = list()
for in_path in dir_before.glob("**/*.png"):
    out_path = dir_after / in_path.name
    args.append(dict(
        in_path=in_path,
        out_path=out_path,
    ))

with mpire.WorkerPool() as pool:
    results = pool.map(compress_image, args)
