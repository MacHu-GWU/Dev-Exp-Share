# -*- coding: utf-8 -*-

"""
This script can convert a concrete project into a cookiecutter template project.
"""

import typing as T
from pathlib_mate import Path
from rich import print as rprint

dir_here = Path.dir_here(__file__)
dir_tmp = dir_here / "tmp"


def mirror_dir(
    dir_before: Path,
    dir_src: Path,
    dir_dst: Path,
    mapper: dict,
    debug: bool = False,
) -> Path:
    dir_after = dir_dst.joinpath(dir_src.basename, dir_before.relative_to(dir_src))
    abspath = dir_after.abspath
    for k, v in mapper.items():
        abspath = abspath.replace(k, f"{{{{ cookiecutter.{v} }}}}")
    dir_new = Path(abspath)
    if debug:
        rprint(f"{str(dir_before.relative_to(dir_src.parent))!r} ->")
        rprint(f"    {str(dir_new.relative_to(dir_dst))!r}")
    dir_new.mkdir_if_not_exists()
    return dir_new


def mirror_file(
    path_before: Path,
    dir_src: Path,
    dir_dst: Path,
    mapper: dict,
    debug: bool = False,
) -> Path:
    path_after = dir_dst.joinpath(dir_src.basename, path_before.relative_to(dir_src))
    abspath = path_after.abspath
    for k, v in mapper.items():
        abspath = abspath.replace(k, f"{{{{ cookiecutter.{v} }}}}")
    path_new = Path(abspath)
    if debug:
        rprint(f"{str(path_before.relative_to(dir_src.parent))!r} ->")
        rprint(f"    {str(path_new.relative_to(dir_dst))!r}")

    content = path_before.read_bytes()
    try:
        text = content.decode("utf-8", errors="strict")
        text = text.replace("{{", "{% raw %}{{{% endraw %}").replace("}}", "{% raw %}}}{% endraw %}")
        for k, v in mapper.items():
            text = text.replace(k, f"{{{{ cookiecutter.{v} }}}}")
        path_new.write_text(text)
    except UnicodeDecodeError:
        path_before.copyto(path_new)
    return path_new


def templaterize(
    dir_src: Path,
    dir_dst: Path,
    mapper: dict,
    ignore_dirs: T.List[str],
    ignore_files: T.List[str],
    debug: bool = False,
    _is_root: bool = True,
):
    """
    Example::

    - dir_src: ``/tmp/my_project/README.md``
    - dir_dst: ``/GitHub/``
    - mapper: ``{"my_project": "project_name"}``

    Then it creates ``/GitHub/{{ cookiecutter.project_name }}/README.md``.
    """
    if _is_root:
        dir_dst.remove_if_exists()
        dir_dst.mkdir_if_not_exists()
        mirror_dir(dir_src, dir_src, dir_dst, mapper, debug)

    for p in dir_src.iterdir():
        if p.is_dir():
            if p.basename not in ignore_dirs:
                dir_new = mirror_dir(p, dir_src, dir_dst, mapper, debug)
                templaterize(
                    dir_src=p,
                    dir_dst=dir_new.parent,
                    mapper=mapper,
                    ignore_dirs=ignore_dirs,
                    ignore_files=ignore_files,
                    debug=debug,
                    _is_root=False,
                )

        elif p.is_file():
            if p.basename not in ignore_files:
                mirror_file(p, dir_src, dir_dst, mapper, debug)
        else:
            pass


if __name__ == "__main__":
    templaterize(
        dir_src=Path("/Users/sanhehu/Documents/CodeCommit/aws_python-project"),
        dir_dst=dir_tmp,
        mapper={
            "aws_python": "package_name",
            "Sanhe Hu": "author_name",
            "husanhe@gmail.com": "author_email",
        },
        ignore_dirs=[
            ".idea",
            ".git",
            ".venv",
            ".pytest_cache",
            "build",
            "dist",
            "htmlcov",
        ],
        ignore_files=[
            ".coverage",
            ".current-env-name.json",
            ".poetry-lock-hash.json",
            "requirements-main.txt",
            "requirements-dev.txt",
            "requirements-test.txt",
            "requirements-doc.txt",
        ],
        debug=True,
    )
