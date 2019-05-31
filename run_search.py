#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys
import json
import calendar
from datetime import datetime

from parse_query import parse_query_string


RATELIMIT_FILE = os.path.expanduser("~/.ads/ratelimit")
URL_FORMAT = "https://ui.adsabs.harvard.edu/abs/{0}/abstract".format


def return_error(text, url, sub=None):
    error = dict(items=[dict(title=text, arg=url)])
    if sub is not None:
        error["items"][0]["subtitle"] = sub
    sys.stdout.write(json.dumps(error))
    sys.exit(0)


def get_ratelimit():
    if os.path.exists(RATELIMIT_FILE):
        with open(RATELIMIT_FILE, "r") as f:
            return json.load(f)
    return None


def set_ratelimit(ratelimit):
    with open(RATELIMIT_FILE, "w") as f:
        json.dump(ratelimit, f)


if __name__ == "__main__":
    try:
        import ads
    except ImportError:
        return_error("Install the 'ads' Python library to enable search",
                     "https://github.com/andycasey/ads",
                     sub=("Or set you prefered python interpreter in the "
                          "~/.ads/python file"))

    key = os.environ.get("ADS_DEV_KEY", None)
    if not len(key.strip()):
        key = None
        os.environ.pop("ADS_DEV_KEY")
    exists = os.path.exists(os.path.expanduser("~/.ads/dev_key"))
    if key is None and not exists:
        return_error(("Your ADS API key must be saved in the file "
                      "~/.ads/dev_key or set as an Alfred variable"),
                     "https://github.com/andycasey/ads")

    # Fail if we're over the rate limit
    ratelimit = get_ratelimit()
    if ratelimit is not None:
        current = calendar.timegm(datetime.utcnow().timetuple())
        delta = current - int(ratelimit.get("reset", 0))
        if ratelimit.get("remaining", "1") == "0" and delta < 0:
            return_error("Your ADS rate limit has been reached",
                         "https://github.com/andycasey/ads")

    # Parse the query
    query = " ".join(sys.argv[1:]).strip()
    query_string = parse_query_string(query)

    # Perform the search
    request = ads.SearchQuery(
        q=query_string,
        sort="pubdate+desc",
        fl=["title", "author", "year", "pubdate", "bibcode"],
        max_pages=1, rows=5)

    papers = []
    for paper in request:
        papers.append(dict(
            title="{0} ({1})".format(paper.title[0], paper.year),
            subtitle=", ".join(paper.author),
            arg=URL_FORMAT(paper.bibcode),
        ))

    # Save the rate limit
    ratelimit = request.response.get_ratelimits()
    set_ratelimit(ratelimit)

    results = dict(items=papers)
    sys.stdout.write(json.dumps(results))
