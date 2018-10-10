"""
The goal of this interview is to implement trie (or prefix tree) using dictionaries (aka hash maps or hash tables), where:

    1. the dictionary keys are the prefixes
    2. the value of a leaf node is None.
    3. the value for empty input is {}.

>>> build_trie()
{}
>>> build_trie("")
{}
>>> build_trie("trie")
{'t': {'tr': {'tri': {'trie': None}}}}
>>> build_trie("tree")
{'t': {'tr': {'tre': {'tree': None}}}}
>>> build_tree("A","to", "tea", "ted", "ten", "i", "in", "inn")
{'A': None, 't': {'to': None, 'te': {'tea': None, 'ted': None, 'ten': None}}, 'i': {'in': {'inn': None}}}
>>> build_trie("true", "trust")
{'t': {'tr': {'tru': {'true': None, 'trus': {'trust': None}}}}}
"""


def add_string(string, index, dictionary):
    key = string[:index]
    if key != string:
        if key in dictionary:
            add_string(string, index+1, dictionary[key])
        else:
            dictionary[key] = add_string(string, index+1, {})
    else:
        if key and key not in dictionary:
            dictionary[key] = None
    return dictionary


def build_trie(*args):
    result = {}
    for word in args:
        add_string(word, 1, result)
    return result
    
