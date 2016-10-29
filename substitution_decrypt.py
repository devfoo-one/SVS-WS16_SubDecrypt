"""
Takes a encrypted file (character substitution) as a command line argument, and tries to decrypt it automatically.
"""
import string
import sys
from collections import defaultdict, Counter
from FuzzyDictionary import Dictionary

VALID_CHARS = list(string.ascii_lowercase + ' _')
DICT = Dictionary('english.txt')


def get_text_from_file(path):
    """
    Gets text from text file.
    :param path: path to text file
    :return: text as string
    """
    retVal = ""
    with open(path) as file:
        for line in file:
            retVal += line.strip()
    return retVal


def get_first_commandline_argument():
    """
    Get first command line argument and return it.
    """
    try:
        return sys.argv[1]
    except IndexError:
        print("No file given. Please provide file path as command line argument.")
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
            if c == ' ':
                ret_val += '_'
            else:
                ret_val += c
    return ret_val


def apply_substitution_dictionary(cyphertext, key, placeholder=False):
    """
    Applies substitution dictionary on cyphertext.
    :param cyphertext: String to decrypt
    :param key: substitution dictionary
    :return: text
    """
    ret_val = ""
    for c in cyphertext:
        if c in key.keys():
            ret_val += key[c].upper()
        else:
            if placeholder:
                ret_val += '#'
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
    name = str(name)
    print('{:*^100}'.format(" " + name + " "))

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


def score_text(text):
    """
    Returns the number of edit operations needed to create a text out of dictionary words.
    :param text: String with words (separated by ' ')
    :return: Edit-Distance, the lower the better
    """
    words_list = text.split()
    # score = len(words_list)
    score = len(text)
    for word in words_list:
        if DICT.check(word):
            score -= len(word)
    return score
    # score = 0
    # for word in text.split():
    #     score += DICT.best_edit_distance(word)
    # return score


def learn_from_dicts(dicts, threshold=4):
    """
    Returns a dictionary, that includes all k/v pairs which occur more often than others.
    :param threshold: how hard is it to learn?
    :param dicts: list with dicts
    :return: dict
    """
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
        retVal[most_common_associated_crypto_char] = clear_char_candidate

    assert (len(list(retVal.values())) == len(set(retVal.values())))

    return retVal


def check_for_valid_chars(word, valid):
    """
    Returns True if word only contains valid chars
    :param word: String
    :param valid: List of valid chars
    :return: boolean
    """
    word = str(word)
    for c in word:
        if c not in valid:
            return False
    return True

""""------------------------------- DATA PART -------------------------------"""

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

""""------------------------------- FREQUENCY PART -------------------------------"""

CYPHERTEXT = clean_text(get_text_from_file(get_first_commandline_argument()))
KEY = {}
# KEY = {c: c for c in VALID_CHARS}
KEY_STORE = []
display_fancy('INPUT', CYPHERTEXT)
sep = get_top_chars(CYPHERTEXT, n=1)[0]
CYPHERTEXT = apply_substitution_dictionary(CYPHERTEXT, {sep: ' '})
VALID_CHARS.remove(' ')
display_fancy('SPACE DETECTION', CYPHERTEXT)


# find most common characters
for doc, eng in zip(get_top_chars(CYPHERTEXT, n=5)[1:], FREQ_char_unigrams):
    KEY[doc], KEY[eng] = eng, doc
# add key two times to give more weight
KEY_STORE.append(KEY)
# KEY_STORE.append(KEY)

assert (len(list(KEY.values())) == len(set(KEY.values())))
display_fancy('FREQUENCY STAGE 1', apply_substitution_dictionary(CYPHERTEXT, KEY))
LEARNED_KEY = learn_from_dicts(KEY_STORE, threshold=1)
BEST_SCORE = score_text(apply_substitution_dictionary(CYPHERTEXT, LEARNED_KEY))
while BEST_SCORE > 0:
    cypher_tokens = CYPHERTEXT.split()
    cypher_tokens = list(set(cypher_tokens))
    LEARNED_KEY = learn_from_dicts(KEY_STORE, threshold=1)
    cypher_tokens.sort(key=lambda x: len(x), reverse=True)
    # BEST_KEY = {}
    for cypher_token in cypher_tokens:
        TEST_KEY = LEARNED_KEY.copy()
        for candidate in DICT.suggest(apply_substitution_dictionary(cypher_token, TEST_KEY)):
            if check_for_valid_chars(candidate, VALID_CHARS):
                CYPHERTEXT_testkey_before = apply_substitution_dictionary(CYPHERTEXT, TEST_KEY)
                for cypher_char, candidate_char in zip(cypher_token, candidate):
                    if candidate_char in TEST_KEY.values():
                        TEST_KEY.pop(list(TEST_KEY.keys())[list(TEST_KEY.values()).index(candidate_char)])
                    TEST_KEY[cypher_char] = candidate_char

                    # check key for double target values
                    assert (len(list(TEST_KEY.values())) == len(set(TEST_KEY.values())))

                    # compare new test key with learned key
                    CYPHERTEXT_testkey_after = apply_substitution_dictionary(CYPHERTEXT, TEST_KEY)
                    errors_before = score_text(CYPHERTEXT_testkey_before)
                    errors_after = score_text(CYPHERTEXT_testkey_after)

                    # display_fancy('BEST KEY', apply_substitution_dictionary(CYPHERTEXT, BEST_KEY))
                    # display_fancy('{} -> {} ({}, {} keys)'.format(cypher_token, candidate, errors_after, len(KEY_STORE)), CYPHERTEXT_testkey_after)
                    # if errors_after < errors_before:
                    if errors_after <= BEST_SCORE:
                        BEST_SCORE = errors_after
                        # BEST_KEY = TEST_KEY.copy()
                        KEY_STORE.append(TEST_KEY.copy())
                        LEARNED_KEY = learn_from_dicts(KEY_STORE, threshold=1)
                        display_fancy('GOT BETTER! (SCORE {})'.format(BEST_SCORE), apply_substitution_dictionary(CYPHERTEXT, LEARNED_KEY))
    KEY_STORE = []
    CYPHERTEXT = apply_substitution_dictionary(CYPHERTEXT,LEARNED_KEY)