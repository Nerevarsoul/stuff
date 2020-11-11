import sys
from collections import Counter, defaultdict


def print_word(result: Counter):
    for word, frequency in result.most_common():
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


def word_count_defaultdict():
    result = defaultdict(lambda: 0)
    with open(filename, 'r') as text_file:
        for line in text_file:
            for word in line.split():
                result[word] += 1
    return result


def print_word_defaultdict(result: defaultdict):
    for word, frequency in sorted(result.items(), key=lambda res: (-res[1], res[0])):
        print(f'<{word}>: <{frequency}>')


def main_defaultdict():
    try:
        result = word_count_defaultdict()
        print_word_defaultdict(result)
    except IOError:
        print('File with {} does not exist'.format(filename))


if __name__ == "__main__":
    try:
        filename = sys.argv[1]
        main()
    except IndexError:
        print('You should specify the filename')
