# -*- coding: utf-8 -*-

"""
Reference:

- https://pngquant.org/
"""

import subprocess
from pathlib_mate import Path

path_pngquant = Path("/opt/homebrew/bin/pngquant")


def compress_image(
    dir_src: Path,
    dir_dst: Path,
):
    for p in dir_src.select_image():
        if p.basename.endswith("-fs8.png"):
            p.remove()
    args = [
        f"{path_pngquant}",
        f"256",
        "--quality=5-5",
        f"{dir_src}/*.png",
    ]
    cmd = " ".join(args)
    print("run the following command to compress image:")
    print(cmd)
    subprocess.run(cmd, shell=True)
    # input("Press ENTER to continue: ")
    dir_dst.mkdir_if_not_exists()
    for p in dir_src.select_image():
        if p.basename.endswith("-fs8.png"):
            new_p = dir_dst.joinpath(p.basename.replace("-fs8.png", ".png"))
            p.moveto(new_p)



dir_here = Path.dir_here(__file__)
dir_src = dir_here.joinpath("before")
dir_dst = dir_here.joinpath("after")
with dir_here.temp_cwd():
    compress_image(dir_src, dir_dst)
