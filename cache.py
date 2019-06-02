#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import time
import pickle
import sqlite3

CACHE_FILENAME = os.path.expanduser("~/.ads/cache.db")


def get_value(key):
    if not os.path.exists(CACHE_FILENAME):
        return None

    with sqlite3.connect(CACHE_FILENAME) as conn:
        c = conn.cursor()
        c.execute("SELECT * FROM cache WHERE key=?", (key, ))

        result = c.fetchone()
        if result is None:
            return None

        key, value, expires = result
        if time.time() > expires:
            c.execute("DELETE FROM cache WHERE key=?", (key,))
            return None

    return pickle.loads(value)


def set_value(key, value, timeout=86400):  # 24 hours
    with sqlite3.connect(CACHE_FILENAME) as conn:
        c = conn.cursor()
        c.execute("CREATE TABLE IF NOT EXISTS cache "
                  "(key TEXT PRIMARY KEY, val BLOB, exp FLOAT)")

        expires = time.time() + timeout
        c.execute("INSERT OR REPLACE INTO cache (key, val, exp) "
                  "VALUES (?, ?, ?)",
                  (key, pickle.dumps(value), expires))


def clean():
    with sqlite3.connect(CACHE_FILENAME) as conn:
        c = conn.cursor()
        c.execute("DELETE FROM cache WHERE exp<=?", (time.time(),))
