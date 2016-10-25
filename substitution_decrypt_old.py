"""
Takes an encrypted string (character substitution) as a command line argument, and tries to decrypt it automatically.
"""
import string
import sys
from collections import defaultdict, Counter

VALID_CHARS = list(string.ascii_lowercase + ' .,-!?"')


def get_text_from_file(path):
    """
    Gets text from text file.
    :param path: path to text file
    :return: text as string
    """
    retVal = ""
    with open(path) as file:
        for line in file:
            retVal += line + ' '
    return retVal


def get_first_commandline_argument():
    """
    Get first command line argument and return it.
    """
    try:
        return sys.argv[1]
    except IndexError:
        print("No cyphertext given. Please provide cyphertext as command line argument.")
        exit(1)


def clean_text(text):
    """
    Simplifies text according to assignment.
    :return: text, only with characters out of VALID_CHARS
    """
    text = text.lower()
    ret_val = ""
    for c in text:
        if c in VALID_CHARS:
            ret_val += c
    return ret_val


def apply_substitution_dictionary(cyphertext, key):
    """
    Applies substitution dictionary on cyphertext.
    :param cyphertext: String to decrypt
    :param key: substitution dictionary
    :return: text
    """
    ret_val = ""
    for c in cyphertext:
        if c in key.keys():
            ret_val += key[c]
        else:
            ret_val += c
    return ret_val


def display_fancy(name, text):
    """
    Displays fancy box
    :param name: Box name
    :param text: text
    :param key: current key
    """
    print()
    print('{:*^100}'.format(name))
    while True:
        display = text[0:96]
        text = text[96:]
        if len(display) == 0:
            break
        print('*', '{:<96}'.format(display), '*')
    print('{:*^100}'.format(''))


def get_top_chars(cyphertext, n=None):
    """
    Get top chars, ordered by occurrence

    :param cyphertext: cyphertext
    :param n: return n chars
    :return list with chars, sorted by occurrence:
    """
    char_counter = defaultdict(int)
    for char in cyphertext:
        char_counter[char] += 1
    return [x[0] for x in sorted(char_counter.items(), key=lambda x: x[1], reverse=True)][:n]


def get_top_short_words(cyphertext, length, separator=' ', n=None):
    """
    Get top short words with specified length, ordered by occurrence.
    Word separators must be space, or given.

    :param cyphertext: cyphertext
    :param length: word length to search
    :param separator: separator (cyphertext must be split into tokens)
    :param n: return n words
    :return: list of words
    """
    word_counter = defaultdict(int)
    for token in cyphertext.split(separator):
        if len(token) == length:
            word_counter[token] += 1
    return [x[0] for x in sorted(word_counter.items(), key=lambda x: x[1], reverse=True)][:n]


def get_top_double_chars(cyphertext, n=None):
    """
    Get top double chars ('nn',...)
    :param cyphertext: cyphertext
    :param n: return n double chars
    :return: list of double chars
    """
    char_double_counter = defaultdict(int)
    for i in range(len(cyphertext) - 1):
        a, b = cyphertext[i], cyphertext[i + 1]
        if a == b and a != ' ':
            char_double_counter[a + b] += 1
    return [x[0] for x in sorted(char_double_counter.items(), key=lambda x: x[1], reverse=True)][:n]


def get_top_char_ngrams(cyphertext, ngram=2, separator=' ', n=None):
    """
    Get top n-grams, ordered by occurrence
    Word separators must be space, or given.

    :param cyphertext: cyphertext
    :param ngram: n of ngrams
    :param separator: word separator, default is space
    :param n: return top n n-grams
    :return: list of n-grams, ordered by occurrence
    """
    char_ngram_counter = defaultdict(int)
    for word in cyphertext.split(separator):
        for i in range(len(word) - (ngram - 1)):
            _token = word[i:i + ngram]
            char_ngram_counter[_token] += 1
    return [x[0] for x in sorted(char_ngram_counter.items(), key=lambda x: x[1], reverse=True)][:n]


def get_top_initial_letters(cyphertext, separator=' ', n=None):
    """
    Get top initial word letters.
    Word separators must be space, or given.

    :param cyphertext: cyphertext
    :param separator: word separator, default is space
    :param n: return n letters
    :return: list of initial letters, ordered by occurrence
    """
    letter_counter = defaultdict(int)
    for token in cyphertext.split(separator):
        letter_counter[token[0:1]] += 1
    return [x[0] for x in sorted(letter_counter.items(), key=lambda x: x[1], reverse=True)][:n]


def get_top_final_letters(cyphertext, separator=' ', n=None):
    """
    Get top final word letters.
    Word separators must be space, or given.

    :param cyphertext: cyphertext
    :param separator: word separator, default is space
    :param n: return n letters
    :return: list of final letters, ordered by occurrence
    """
    letter_counter = defaultdict(int)
    for token in cyphertext.split(separator):
        letter_counter[token[-1:]] += 1
    return [x[0] for x in sorted(letter_counter.items(), key=lambda x: x[1], reverse=True)][:n]


def word_pattern(word):
    """
    Generates word pattern.

    ('ADAM' -> (0,1,0,2)
    :param word: String
    :return: pattern tuple
    """
    chars = []
    ret_val = []
    for c in word:
        if c not in chars:
            chars.append(c)
        ret_val.append(chars.index(c))
    return tuple(ret_val)


##############################################################################

# http://www.simonsingh.net/The_Black_Chamber/hintsandtips.html
FREQ_char_unigrams = ['e', 't', 'a', 'o', 'i', 'n', 's', 'h', 'r', 'd', 'l', 'u']
FREQ_char_bigrams = ['th', 'er', 'on', 'an', 're', 'he', 'in', 'ed', 'nd', 'ha', 'at', 'en', 'es', 'of', 'or', 'nt',
                     'ea', 'ti', 'to', 'it', 'st', 'io', 'le', 'is', 'ou', 'ar', 'as', 'de', 'rt', 've']
FREQ_char_trigrams = ['the', 'and', 'tha', 'ent', 'ion', 'tio', 'for', 'nde', 'has', 'nce', 'edt', 'tis', 'oft', 'sth',
                      'men']
FREQ_char_doubles = ['ss', 'ee', 'tt', 'ff', 'll', 'mm', 'oo']
FREQ_word_initial_chars = ['t', 'o', 'a', 'w', 'b', 'c', 'd', 's', 'f', 'm', 'r', 'h', 'i', 'y', 'e', 'g', 'l', 'n',
                           'p', 'u', 'j', 'k']
FREQ_word_final_chars = ['e', 's', 't', 'd', 'n', 'r', 'y', 'f', 'l', 'o', 'g', 'h', 'a', 'k', 'm', 'p', 'u', 'w']
FREQ_words_one_char = ['a', 'i']
FREQ_words_two_char = ['of', 'to', 'in', 'it', 'is', 'be', 'as', 'at', 'so', 'we', 'he', 'by', 'or', 'on', 'do', 'if',
                       'me', 'my', 'up', 'an', 'go', 'no', 'us', 'am']
FREQ_words_three_char = ['the', 'and', 'for', 'are', 'but', 'not', 'you', 'all', 'any', 'can', 'had', 'her', 'was',
                         'one', 'our', 'out', 'day', 'get', 'has', 'him', 'his', 'how', 'man', 'new', 'now', 'old',
                         'see', 'two', 'way', 'who', 'boy', 'did', 'its', 'let', 'put', 'say', 'she', 'too', 'use']
FREQ_words_four_char = ['that', 'with', 'have', 'this', 'will', 'your', 'from', 'they', 'know', 'want', 'been', 'good',
                        'much', 'some', 'time']

cyphertext = clean_text(get_text_from_file(get_first_commandline_argument()))
# display_fancy('INPUT', cyphertext)

# try to find word separator
sep = get_top_chars(cyphertext, 1)[0]
cyphertext = apply_substitution_dictionary(cyphertext, {sep: ' '})
# display_fancy('SPACE DETECTION', cyphertext)

# combine all candidates for all keys
WEIGHTED_KEY_CANDIDATES = defaultdict(list)

# analyse top char unigrams WEIGHT = 0.8
for doc, eng in zip(get_top_chars(cyphertext)[1:], FREQ_char_unigrams):
    WEIGHTED_KEY_CANDIDATES[doc].extend(list(eng) * 80)

# analyse char doubles WEIGHT = 0.14
for doc, eng in zip(get_top_double_chars(cyphertext), FREQ_char_doubles):
    WEIGHTED_KEY_CANDIDATES[doc[-1]].extend(list(eng[:-1]) * 14)

# analyse character bi- and trigrams WEIGHT 0.3 (both)
for doc, eng in zip(get_top_char_ngrams(cyphertext, ngram=2), FREQ_char_bigrams):
    for x, Y in zip(doc, eng):
        WEIGHTED_KEY_CANDIDATES[x].extend(list(Y) * 3)
for doc, eng in zip(get_top_char_ngrams(cyphertext, ngram=3), FREQ_char_trigrams):
    for x, Y in zip(doc, eng):
        WEIGHTED_KEY_CANDIDATES[x].extend(list(Y) * 3)

# analyse short(1) words WEIGHT = 1.0
for doc, eng in zip(get_top_short_words(cyphertext, length=1), FREQ_words_one_char):
    for x, Y in zip(doc, eng):
        WEIGHTED_KEY_CANDIDATES[x].extend(list(Y) * 10)
# analyse short(2) words WEIGHT = 0.1
for doc, eng in zip(get_top_short_words(cyphertext, length=2), FREQ_words_two_char):
    if word_pattern(doc) == word_pattern(eng):
        for x, Y in zip(doc, eng):
            WEIGHTED_KEY_CANDIDATES[x].extend(list(Y) * 10)
# analyse short(3) words WEIGHT = 0.4
for doc, eng in zip(get_top_short_words(cyphertext, length=3), FREQ_words_three_char):
    if word_pattern(doc) == word_pattern(eng):
        for x, Y in zip(doc, eng):
            WEIGHTED_KEY_CANDIDATES[x].extend(list(Y) * 4)
# analyse short(4) words WEIGHT 0.42
for doc, eng in zip(get_top_short_words(cyphertext, length=4), FREQ_words_four_char):
    if word_pattern(doc) == word_pattern(eng):
        for x, Y in zip(doc, eng):
            WEIGHTED_KEY_CANDIDATES[x].extend(list(Y) * 4)

# analyse initial/final characters WEIGHT 0.1 (both)
for doc, eng in zip(get_top_initial_letters(cyphertext), FREQ_word_initial_chars):
    WEIGHTED_KEY_CANDIDATES[doc].extend(list(eng) * 1)
for doc, eng in zip(get_top_final_letters(cyphertext), FREQ_word_final_chars):
    WEIGHTED_KEY_CANDIDATES[doc].extend(list(eng) * 1)

print('Trying with this setup:')
KEY_STATISTICS = {}
for cypher_char, candidates in WEIGHTED_KEY_CANDIDATES.items():
    # A test has shown that the right candidate is never at the second or less position. (Either top or not found).
    candidate = sorted(Counter(candidates).items(), key=lambda x: x[1], reverse=True)[:1][0][0]
    candidate_count = sorted(Counter(candidates).items(), key=lambda x: x[1], reverse=True)[:1][0][1]
    total_candidate_count = len(candidates)
    # if total_candidate_count > 100 and candidate_count / total_candidate_count > 0.5:
    print(cypher_char, candidate, len(candidates), '{:.2%}'.format(candidate_count / len(candidates)))
    KEY_STATISTICS[cypher_char] = candidate

display_fancy('AFTER STATISTICS', apply_substitution_dictionary(cyphertext, KEY_STATISTICS))

print(word_pattern('abcdefg'))
print(word_pattern('alla'))

"""
TODO ICH NOTIERE:
1. Es muss sichergestellt sein, dass die Keys ihre Bijektivität nicht verlieren!
2. Ein Wörterbuch muss her!
"""