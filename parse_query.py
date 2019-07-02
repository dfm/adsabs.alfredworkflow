#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re
import sys
import shlex


def parse_query_string(query):
    # Remove parentheses
    query = query.replace("(", " ").replace(")", " ")

    # Tokenize the query
    tokens = shlex.split(query)
    years = []
    authors = []
    for token in tokens:
        token = token.strip()
        numbers = re.findall("[0-9]+", token)
        years += list(int(n) for n in numbers if len(n) == 4)
        if len(numbers) == 0:
            authors.append(token)
    years = list(sorted(years))

    # Fail fast if there are no authors
    if len(authors) == 0:
        return query

    # Construct the query in ADS's format
    q = []
    for author in authors:
        q.append("author:\"" + author + "\"")
    if len(years) == 1:
        q.append("year:{0}".format(years[0]))
    elif len(years) > 1:
        q.append("year:[{0} TO {1}]".format(min(years), max(years)))
    q = " ".join(q)
    return q


if __name__ == "__main__":
    query = " ".join(sys.argv[1:])
    query = parse_query_string(query)
    sys.stdout.write("https://ui.adsabs.harvard.edu/search/q="+query)
