# -*- coding: utf-8 -*-
# content of screen_session_manager.py

"""
保持 Session 不中断, 长期运行某一个脚本的 Python 自动化程序. 本质是对 Screen 命令的封装.

面向最终用户的函数:

- :func:`run_script`: 用 Screen 长期运行某个脚本, 并给这个 Session 一个名字.
- :func:`list_session`: 列出正在运行着的 screen session 列表.
- :func:`stop_script`: 根据 Session 名字, 停止在后台运行的 Screen session 长期运行某个脚本.
- :func:`enter_session`: 恢复并交互式 Session.

面向开发者的底层函数:

- :func:`make_it_executable`: 该函数可以将任意 Path 路径对象所指向的文件设置为可执行.
- :func:`run_script_in_screen`: 用 Screen 在后台运行指定脚本, 并给与一个 session 名称.
- :func:`stop_script_in_screen`: 根据 session (id) 关闭 Screen 在后台运行的脚本.
- :func:`filter_session`: 检测并返回已经正在运行着的 session id 列表.
"""

import typing as T
import os
import stat
import subprocess
from pathlib import Path


# ------------------------------------------------------------------------------
# Low level function
# ------------------------------------------------------------------------------
def make_it_executable(p) -> Path:
    """
    该函数可以将任意 Path 路径对象所指向的文件设置为可执行. 其原理是先用 os.stat 获得
    当前的文件模式码, 然后再用 | (相当于集合运算中的添加) 运算法添加上 stat.S_IEXEC, 即
    chmod +x 的权限 (这里的 + 就是添加的意思, 和 | 等效. x 则是 executable, 和 stat.S_IEXEC
    等效).
    """
    p = Path(p)
    if p.is_file() is False:
        raise TypeError(f"{p} is not a file!")
    st = os.stat(p)  # get current stat of the file
    os.chmod(p, st.st_mode | stat.S_IEXEC)  # add 'executable' bit (| is bitwise OR)
    return p


def run_script_in_screen(p, name: str):
    """
    用 Screen 在后台运行指定脚本, 并给与一个 session 名称.

    以下是 screen 命令选项的说明::

        -A    -- adapt all windows to the new display width & height
        -dmS  -- start as daemon, screen session in detached mode
    """
    p = Path(p)
    subprocess.run(["screen", "-AdmS", name, f"{p}"])


def stop_script_in_screen(session: str):
    """
    根据 session (id) 关闭 Screen 在后台运行的脚本.

    以下是 screen 命令选项的说明::

        -S sockname   Name this session <pid>.sockname instead of <pid>.<tty>.<host>.
        -X            Execute <cmd> as a screen command in the specified session.

    """
    subprocess.run(["screen", "-X", "-S", session, "quit"])


def filter_session(name: T.Union[str, T.List[str]]) -> T.List[str]:
    """
    检测并返回已经正在运行着的 session id 列表. 其原理是用 screen -ls 命令打印出所有
    正在运行的 session, 并用 Python 进行字符串分析, 找出相关的 session id.

    :param name: 可以是一个 session 名也可以是多个. 只要 match 其中的任何一个则视为 match.

    :return: 跟 name 相关的 session id 列表.
    """
    if isinstance(name, str):
        names = [name]
    else:
        names = name
    suffixes = [f".{v}\t(Detached)" for v in names]
    res = subprocess.run(["screen", "-ls"], capture_output=True)
    content = res.stdout.decode("utf-8")
    sessions = list()
    for line in content.splitlines():
        for suffix in suffixes:
            if line.endswith(suffix):
                session_id = [
                    token.strip() for token in line.strip().split("\t") if token.strip()
                ][0]
                sessions.append(session_id)
    return sessions


# ------------------------------------------------------------------------------
# High level function
# ------------------------------------------------------------------------------
def run_script(
    p,
    name: str,
    verbose: bool = True,
    print_func: T.Callable = print,
):
    """
    用 Screen 长期运行某个脚本, 并给这个 Session 一个名字.
    """
    p = make_it_executable(p)  # 先将该脚本设置为可执行
    if verbose:
        print_func(f"run {p.name!r} in screen")
    sessions = filter_session(name=name)
    if len(sessions) == 0:
        if verbose:
            print_func(f"  start session {name!r} ...")
        run_script_in_screen(p, name)
    else:
        if verbose:
            print_func("  session is already running, skip ...")
    pass


def list_session():
    """
    列出正在运行着的 screen session 列表.

    以下是 screen 命令选项的说明::

        -list         or -ls. Do nothing, just list our SockDir.
    """
    subprocess.run(["screen", "-ls"])


def stop_script(
    name: str,
    verbose: bool = True,
    print_func: T.Callable = print,
):
    """
    根据 Session 名字, 停止在后台运行的 Screen session 长期运行某个脚本. 该函数会根据名字
    找到对应 session 的 id, 然后根据 id 关闭 session. 这里注意你要避免你的 session 名字
    刚好是其他 session 的字符串前缀, 否则会误杀其他 session.
    """
    if verbose:
        print_func(f"stop session {name!r}")
    sessions = filter_session(name=name)
    for session in sessions:
        print(f"  stop session id: {session!r}")
        stop_script_in_screen(session)
    if len(sessions) == 0:
        print(f"  didn't found any matched sessions")


def enter_session(
    name: str,
    prompt: bool = True,
    verbose: bool = True,
    print_func: T.Callable = print,
):
    """
    恢复并交互式 Session.
    """
    if verbose:
        print_func(f"Try to enter session {name!r}")
    sessions = filter_session(name=name)
    if len(sessions) == 0:
        if verbose:
            print_func(f"  didn't found any matched sessions")
        return
    if verbose:
        print_func(f"Run 'screen -r {name}' command to enter interactive shell")
        print_func("To exit the shell without killing it, hit 'Ctrl + A' then hit 'D'")
    if prompt:
        answer = input(f"Found session! Enter interactive shell? [y/n]: ")
        if answer.lower() != "y":
            if verbose:
                print_func(f"you entered {answer}, exit ...")
            return
    cmd = f"screen -r {name}"
    subprocess.run(cmd, shell=True)


if __name__ == "__main__":
    path_long_running_script_sh = (
        Path(__file__).absolute().parent.joinpath("long_running_script.sh")
    )
    name = "long_running_script"

    # run_script(path_long_running_script_sh, name)
    # list_session()
    # enter_session(name)
    # stop_script(name)
