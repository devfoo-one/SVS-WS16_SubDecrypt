from collections import defaultdict, Counter

dicts = [
    {'r': 'r', 'h': 'i', '_': 'e', 'n': 't', 'z': '-', 'l': 'l', 'i': 'o', 'k': 'n', 'e': 'h', 't': 'a', ' ': ' ',
     's': 'm'},
    {'r': 'r', 'h': 'i', '_': 'e', 'n': 't', 'z': '-', 'l': 'l', 'i': 'o', 'k': 'n', 'e': 'h', 't': 'a', ' ': ' ',
     's': 'm'},
    {'r': 'r', 'h': 'i', '_': 'e', 'n': 't', 'z': '-', 'l': 'l', 'i': 'o', 'k': 'n', 'e': 'h', 't': 'a', ' ': ' ',
     's': 'm'},
    {'i': 'o', 'h': 'i', 'l': 'n', '_': 'e', 't': 'a', 'k': 'y', 'n': 't', ' ': ' ', 'q': 'v', 'g': 'p', 'z': 'r'},
    {'c': 'f', 'i': 'o', 'h': 'i', 'e': 'n', '_': 'e', 'k': 'm', 't': 'a', 'b': 'c', 'n': 't', ' ': ' ', 'g': 'g'},
    {'c': 'f', 'i': 'o', 'h': 'i', 'e': 'n', '_': 'e', 'k': 'm', 't': 'a', 'b': 'c', 'n': 't', ' ': ' ', 'g': 'g'},
    {'c': 'f', 'i': 'o', 'h': 'i', 'e': 'n', '_': 'e', 'k': 'm', 't': 'a', 'b': 'c', 'n': 't', ' ': ' ', 'g': 'g'},
    {'c': 'f', 'i': 'o', 'h': 'i', 'e': 'n', '_': 'e', 'k': 'm', 't': 'a', 'b': 'c', 'n': 't', ' ': ' ', 'g': 'g'},

]

threshold = 1
############
retVal = {}
final_candidates = defaultdict(list)
aggregate = defaultdict(list)
clear_2_crypto = defaultdict(list)

for d in dicts:
    for crypto_char, clear_char_candidate in d.items():
        aggregate[crypto_char].append(clear_char_candidate)

for crypto_char, clear_char_candidate in aggregate.items():
    sorted_candidates = sorted(Counter(clear_char_candidate).items(), key=lambda x: x[1], reverse=True)
    most_common_candidate = sorted_candidates[0]
    try:
        next_most_common_candidate = sorted_candidates[1]
    except IndexError:
        next_most_common_candidate = ('', 0)

    difference = most_common_candidate[1] - next_most_common_candidate[1]
    if difference >= threshold:
        most_common_candidate_char = most_common_candidate[0]
        final_candidates[crypto_char].append(most_common_candidate_char)
        clear_2_crypto[most_common_candidate_char].append((crypto_char, difference))

# keep bijectivity
for clear_char_candidate, associated_crypto_chars in clear_2_crypto.items():
    sorted_associated_crypto_chars = sorted(associated_crypto_chars, key=lambda x: x[1], reverse=True)
    most_common_associated_crypto_char = sorted_associated_crypto_chars[0][0]
    print(most_common_associated_crypto_char)
    retVal[most_common_associated_crypto_char] = clear_char_candidate

assert (len(list(retVal.values())) == len(set(retVal.values())))
