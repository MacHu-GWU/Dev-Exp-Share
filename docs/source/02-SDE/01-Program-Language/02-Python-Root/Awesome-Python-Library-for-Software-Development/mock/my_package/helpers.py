# -*- coding: utf-8 -*-
# content of ``my_package/constant.py``

from datetime import datetime, timezone


def utc_now() -> datetime:
    return datetime.utcnow().replace(tzinfo=timezone.utc)
