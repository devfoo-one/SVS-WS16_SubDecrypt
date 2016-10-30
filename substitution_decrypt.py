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


def score_text(text, fine=False):
    """
    Returns the number of edit operations needed to create a text out of dictionary words.
    :param text: String with words (separated by ' ')
    :param fine: Detailed scan
    :return: Edit-Distance, the lower the better
    """
    if fine:
        score = 0
        for word in text.split():
            score += DICT.best_edit_distance(word)
        return score
    else:
        words_list = text.split()
        score = len(text)
        for word in words_list:
            if DICT.check(word):
                score -= len(word)
    return score


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


# http://www.simonsingh.net/The_Black_Chamber/hintsandtips.html
FREQ_char_unigrams = ['e', 't', 'a', 'o', 'i', 'n', 's', 'h', 'r', 'd', 'l', 'u']

""" -------------------- BEGIN -------------------- """
KEY = {}
KEY_STORE = []

CYPHERTEXT = clean_text(get_text_from_file(get_first_commandline_argument()))
display_fancy('INPUT', CYPHERTEXT)

# find word separator
sep = get_top_chars(CYPHERTEXT, n=1)[0]
CYPHERTEXT = apply_substitution_dictionary(CYPHERTEXT, {sep: ' '})
VALID_CHARS.remove(' ')
display_fancy('SPACE DETECTION', CYPHERTEXT)

# find most common characters
for doc, eng in zip(get_top_chars(CYPHERTEXT, n=5)[1:], FREQ_char_unigrams):
    KEY[doc], KEY[eng] = eng, doc
KEY_STORE.append(KEY)
assert (len(list(KEY.values())) == len(set(KEY.values())))
display_fancy('FREQUENCY STAGE 1', apply_substitution_dictionary(CYPHERTEXT, KEY))

LEARNED_KEY = learn_from_dicts(KEY_STORE, threshold=1)
assert (len(list(LEARNED_KEY.values())) == len(set(LEARNED_KEY.values())))

second_iteration = False
while True:
    cypher_tokens = list(set(CYPHERTEXT.split()))
    if second_iteration:
        BEST_SCORE = score_text(apply_substitution_dictionary(CYPHERTEXT, LEARNED_KEY), fine=True)
    else:
        BEST_SCORE = score_text(apply_substitution_dictionary(CYPHERTEXT, LEARNED_KEY), fine=False)
    INITIAL_SCORE = BEST_SCORE
    cypher_tokens.sort(key=lambda x: len(x), reverse=True)
    LEARNED_KEY = learn_from_dicts(KEY_STORE, threshold=1)
    assert (len(list(LEARNED_KEY.values())) == len(set(LEARNED_KEY.values())))

    for cypher_token in cypher_tokens:
        TEST_KEY = LEARNED_KEY.copy()
        if second_iteration:
            query = apply_substitution_dictionary(cypher_token, TEST_KEY)
            if DICT.check(query):
                continue
            else:
                candidates = DICT.suggest(query)[:20]
        else:
            candidates = DICT.suggest(apply_substitution_dictionary(cypher_token, TEST_KEY))[:400]

        for candidate in candidates:
            if check_for_valid_chars(candidate, VALID_CHARS):
                for cypher_char, candidate_char in zip(cypher_token, candidate):
                    if candidate_char in TEST_KEY.values():
                        TEST_KEY.pop(list(TEST_KEY.keys())[list(TEST_KEY.values()).index(candidate_char)])
                    TEST_KEY[cypher_char] = candidate_char
                    assert (len(list(TEST_KEY.values())) == len(set(TEST_KEY.values())))

                CYPHERTEXT_testkey = apply_substitution_dictionary(CYPHERTEXT, TEST_KEY)
                if second_iteration:
                    errors_testkey = score_text(CYPHERTEXT_testkey, fine=True)
                else:
                    errors_testkey = score_text(CYPHERTEXT_testkey, fine=False)

                if errors_testkey <= BEST_SCORE:
                    KEY_STORE.append(TEST_KEY.copy())
                    LEARNED_KEY = learn_from_dicts(KEY_STORE, threshold=1)
                    if errors_testkey < BEST_SCORE:
                        KEY_STORE.append(TEST_KEY.copy())
                        LEARNED_KEY = learn_from_dicts(KEY_STORE, threshold=1)
                        BEST_SCORE = errors_testkey
                        display_fancy(
                            'GOT BETTER! ({}) {} -> {}'.format(INITIAL_SCORE / BEST_SCORE, cypher_token, candidate),
                            apply_substitution_dictionary(CYPHERTEXT, LEARNED_KEY))

    if second_iteration:
        display_fancy('FINAL'.format(BEST_SCORE), apply_substitution_dictionary(CYPHERTEXT, LEARNED_KEY))
        break
    else:
        second_iteration = True
        print('Second loop with finer search...')
        KEY_STORE = []
        CYPHERTEXT = apply_substitution_dictionary(CYPHERTEXT, LEARNED_KEY)
        display_fancy('TEXT AFTER FIRST RUN', CYPHERTEXT)
