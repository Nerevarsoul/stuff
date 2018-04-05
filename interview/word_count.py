#!/usr/bin/env python
import sys
from collections import Counter


def print_word(result):
    for word, frequency in sorted(result.most_common(), key=lambda res: (-res[1], res[0])):
        print('<{}>: <{}>'.format(word, frequency))


def word_count():
    result = Counter()
    with open(filename, 'r') as text_file:
        for line in text_file:
            for word in line.split():
                result[word] += 1
    return result


def main():
    try:
        result = word_count()
        print_word(result)
    except IOError:
        print('File with {} does not exist'.format(filename))


if __name__ == "__main__":
    try:
        filename = sys.argv[1]
        main()
    except IndexError:
        print('You should specify the filename')
