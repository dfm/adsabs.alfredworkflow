import re
import sys
import shlex
from collections import namedtuple

def tokenize(query):
    tokens = shlex.split(query)
    years = []
    authors = []
    for token in tokens:
        token = token.strip()
        numbers = re.findall("[0-9]+", token)
        years += list(int(n) for n in numbers if len(n) == 4)
        if len(numbers) == 0:
            authors.append(token)
    return list(sorted(years)), authors

query = sys.argv[1]

years, authors = tokenize(query)
if len(authors) == 0:
    sys.stdout.write(query)
    sys.exit(0)

# Construct the query
q = []
for author in authors:
    q.append("author:\"" + author + "\"")
if len(years) == 1:
    q.append("year:{0}".format(years[0]))
elif len(years) > 1:
    q.append("year:[{0} TO {1}]".format(
        min(tokens.years), max(years)))
q = " ".join(q)

sys.stdout.write(q)
