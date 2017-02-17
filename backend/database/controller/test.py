
# coding=utf-8

import itertools

cols = ["vorname", "nachname", "geburtstag", "wohnort"]
words = ["alex", "daniel", "essen"]

result = []
# problem: kein zurücklegen
for c in itertools.permutations(cols, 3):
    result.extend(list(c))
print result
print
print

tmp_like = "{col} LIKE %{word}%"

or_list = []
for col in cols:
    like_list = []
    for word in words:
        like_list.append(tmp_like.format(col=col, word=word))
    or_list.append("(" + " AND ".join(like_list) + ")")

print "\nOR ".join(or_list)

# alle Permutationen von 3 aus 4 Elementen

