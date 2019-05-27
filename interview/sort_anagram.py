from collections import defaultdict
from typing import List


def sort_anagram_list(word_list: List[str]) -> List[List[str]]:
    word_dict = defaultdict(list)
    for word in word_list:
        word_dict[''.join(sorted(word))].append(word)
    return list(word_dict.values())


if __name__ == "__main__":
    input_list = ['торт', 'сорт', 'трос', 'сон', 'нос', 'рост']
    print(sort_anagram_list(input_list))
