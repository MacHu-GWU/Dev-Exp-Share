# -*- coding: utf-8 -*-

"""
如果将 HTTP GET URL 背后的 HTML 保存到 S3 上, 那么要注意 S3 的 KEY 的字符集是有限制的.
而我们希望 URL <-> S3 Key 是互相可计算的, 所以我们使用 base64 对 URL 重编码, 并由于
S3 Key 不支持 ``=``, 所以我们人为的移除了 Padding 的等号, 然后再计算 URL 时, 人为的
加上等号.
"""

from base64 import b64encode, b64decode


def s3_key_safe_b64encode(text):
    return b64encode(text.encode("utf-8")).decode("utf-8").replace("=", "")


def s3_key_safe_b64decode(text):
    div, mod = divmod(len(text), 4)
    if mod != 0:
        text = text + "=" * (4 - mod)
    return b64decode(text.encode("utf-8")).decode("utf-8")


if __name__ == "__main__":
    url = "https://www.python.org"
    b64_url = s3_key_safe_b64encode(url)
    original_url = s3_key_safe_b64decode(b64_url)
