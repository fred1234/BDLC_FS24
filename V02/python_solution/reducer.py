#!/usr/bin/python3

import sys
current_word = None
current_count = 0
word = None
for line in sys.stdin:
    line = line.strip()
    try:
        # convert count (currently a string) to int
        word, count = line.split('\t', 1)
        count = int(count)
    except ValueError:
        # split was not right or count was not a number, so silently
        # ignore/discard this line
        continue
    if current_word == word:
        current_count += count
    else:
        if current_word:
            print(f"{current_word}\t{current_count}")
        current_count = count
        current_word = word

if current_word == word:
    print(f"{current_word}\t{current_count}")
