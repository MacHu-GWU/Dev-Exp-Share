#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""
A python script that can detect current Operational System.

This script works on Python2.7, Python3.3 +

Note:

- this script depends on ``platform.system()`` standard lib to identify
    Windows / MacOS / Linux
- this script depends on ``/etc/os-release`` file to identify
    Linux release version. You can find more info about this file at
    https://man7.org/linux/man-pages/man5/os-release.5.html#:~:text=The%20%2Fetc%2Fos%2Drelease,like%20shell%2Dcompatible%20variable%20assignments.
"""

import os
import platform

IS_WINDOWS = False
IS_MACOS = False
IS_LINUX = False

IS_AMZ_LINUX = False
IS_CENTOS = False
IS_REDHAT = False
IS_FEDORA = False
IS_UBUNTU = False
IS_DEBIAN = False

OS_NAME = None


class OSEnum:
    WINDOWS = "Windows"
    MACOS = "MacOS"
    AMAZON_LINUX = "Amazon Linux"
    CENTOS = "CentOS"
    REDHAT = "Redhat"
    FEDORA = "Fedora"
    UBUNTU = "Ubuntu"
    DEBIAN = "Debian"


def parse_etc_os_release():
    """
    Parse key value pair from the /etc/os-release file.

    This function only work on Linux:

    Ref:

    - https://man7.org/linux/man-pages/man5/os-release.5.html#:~:text=The%20%2Fetc%2Fos%2Drelease,like%20shell%2Dcompatible%20variable%20assignments.

    :rtype: dict
    """
    with open("/etc/os-release", "rb") as f:
        content = f.read().decode("utf-8")
        data = dict()
        for line in content.strip().split("\n"):
            key, value = line.strip().split("=", 1)
            value = value[1:-1]
            data[key] = value
    return data


print(f"Try to detect Operation System (OS) ...")

unable_to_detect_os_error = NotImplementedError("Unable to detect OS!")

platform_system = platform.system()
if platform_system == "Windows":
    IS_WINDOWS = True
    OS_NAME = OSEnum.WINDOWS
elif platform_system == "Darwin":
    IS_MACOS = True
    OS_NAME = OSEnum.MACOS
elif platform_system == "Linux":
    IS_LINUX = True
    if os.path.exists("/etc/os-release"):
        data = parse_etc_os_release()
        if data["ID"] == "amzn":
            IS_AMZ_LINUX = True
            OS_NAME = OSEnum.AMAZON_LINUX
        elif data["ID"] == "centos":
            IS_CENTOS = True
            OS_NAME = OSEnum.CENTOS
        elif data["ID"] == "rhel":
            IS_REDHAT = True
            OS_NAME = OSEnum.REDHAT
        elif data["ID"] == "fedora":
            IS_FEDORA = True
            OS_NAME = OSEnum.FEDORA
        elif data["ID"] == "ubuntu":
            IS_UBUNTU = True
            OS_NAME = OSEnum.UBUNTU
        elif data["ID"] == "debian":
            IS_DEBIAN = True
            OS_NAME = OSEnum.DEBIAN
        else:
            raise unable_to_detect_os_error
    else:
        raise unable_to_detect_os_error
else:
    raise unable_to_detect_os_error
print(f"  current OS is {OS_NAME!r}")
