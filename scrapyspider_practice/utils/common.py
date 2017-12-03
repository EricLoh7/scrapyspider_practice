# !/usr/bin/env python
# -*- coding:utf-8 -*-

import hashlib

def get_md5(url):
    m = hashlib.md5()
    if isinstance(url,str):
        m.update(url.encode("utf-8"))
    else:
        m.update(url)
    return m.hexdigest()

if __name__ == "__main__":
    print(get_md5("python.jobbole.com"))