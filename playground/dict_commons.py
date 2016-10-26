from collections import Counter
from statistics import mean

dicts = [{'x': 'o', 'r': 'l', ',': 'k', 'v': 'n', '!': 'e', '-': 'r', 'c': 'f', 's': 'z', 'i': 'y', 'p': 'a', 'a': ' ', 'h': 'g', 'b': 'b', 'd': 'p', 'f': '"', 'z': 'm', 'j': 'i', 'q': 't', 'm': 'u', 'g': ',', 'n': '-', 'u': 'x', 't': 'q', 'l': 's', 'y': 'v'},
{'x': 'b', 'r': 'c', ',': 's', 'v': 'f', '!': '-', '-': 'y', 'c': ' ', 's': 'p', 'i': 'r', 'p': '!', 'a': 'x', 'h': ',', 'b': 'z', 'd': 'g', 'f': 'd', 'z': 'u', 'j': '?', 'q': 'j', 'm': 'o', 'g': 'l', 'n': 'h', 'u': 'v', 't': 'n', 'l': 'i', 'y': 'q'},
{'x': 'b', 'r': 'v', ',': 'h', 'v': 'k', '!': '!', '-': 'g', 'c': '-', 's': '"', 'i': 'r', 'p': 'm', 'a': 'n', 'h': '?', 'b': 'j', 'd': 'i', 'f': 'f', 'z': 'w', 'j': 'o', 'q': 'p', 'm': 's', 'g': 'a', 'n': ',', 'u': 'z', 't': 'u', 'l': 'y', 'y': 'd'},
{'x': 'a', 'r': 'y', ',': '-', 'v': 'v', '!': 'b', '-': 't', 'c': 'n', 's': ' ', 'i': 'q', 'p': 'i', 'a': 'o', 'h': 'h', 'b': 'l', 'd': 'c', 'f': 'g', 'z': 'w', 'j': 's', 'q': '!', 'm': '"', 'g': 'd', 'n': 'f', 'u': 'm', 't': 'j', 'l': 'x', 'y': 'e'},
{'x': '-', 'r': '!', ',': '"', 'v': ' ', '!': 'e', '-': 'i', 'c': 'v', 's': 'n', 'i': 'q', 'p': '.', 'a': 'h', 'h': 'y', 'b': 'x', 'd': 'b', 'f': 'l', 'z': 'w', 'j': 'p', 'q': 'f', 'm': 'g', 'g': 'o', 'n': 'j', 'u': 'k', 't': 't', 'l': 'r', 'y': 'u'},
{'x': 'o', 'r': 'l', ',': 'd', 'v': 'z', '!': 'i', '-': 'y', 'c': 'n', 's': ' ', 'i': 'h', 'p': 'f', 'a': '?', 'h': 'k', 'b': 'e', 'd': 'm', 'f': 'v', 'z': 'w', 'j': 'a', 'q': 'q', 'm': 'c', 'g': 'g', 'n': 'u', 'u': 'b', 't': 't', 'l': '.', 'y': ','},
{'x': 'b', 'r': 'v', ',': 'y', 'v': 'k', '!': 'h', '-': 'q', 'c': '"', 's': 'p', 'i': '-', 'p': 'l', 'a': '.', 'h': ',', 'b': 't', 'd': 'j', 'f': 'n', 'z': 'w', 'j': '?', 'q': ' ', 'm': 'o', 'g': 'd', 'n': 'u', 'u': 'f', 't': 'e', 'l': 'g', 'y': 'r'},
{'x': 'p', 'r': 'h', ',': ' ', 'v': 'k', '!': 'c', '-': 'x', 'c': 'g', 's': '!', 'i': 'n', 'p': 'e', 'a': 'q', 'h': '?', 'b': 'a', 'd': 'b', 'f': '"', 'z': 'w', 'j': 'd', 'q': 'i', 'm': 'o', 'g': 'z', 'n': 'f', 'u': 't', 't': 'u', 'l': ',', 'y': '-'},
]

def most_common_dict(dicts):
    """
    Calculates an average dictionary out of given dicts of the same dimensions and keys.
    Includes only items that occour as twice as much as the average.
    :param dicts: list with dicts
    :return: dict
    """
    retVal = {}
    keys = dicts[0].keys()
    for k in keys:
        values = []
        for d in dicts:
            values.append(d[k])

        print(sorted(Counter(values).items(), key=lambda x: x[1], reverse=True))
        most_common_item_for_k = sorted(Counter(values).items(), key=lambda x: x[1], reverse=True)[0]
        if most_common_item_for_k[1] > 2 * mean(Counter(values).values()):
            retVal[k] = most_common_item_for_k[0]
    return retVal


print(most_common_dict(dicts))