"""
Takes an encrypted string (character substitution) as a command line argument, and tries to decrypt it automatically.
"""
import string
import sys
from collections import defaultdict

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


def display_fancy(name, text, key=None):
    """
    Displays fancy box
    :param name: Box name
    :param text: text
    :param key: current key
    """
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


##############################################################################

# http://www.simonsingh.net/The_Black_Chamber/hintsandtips.html
FREQ_single_letters = ['e', 't', 'a', 'o', 'i', 'n', 's', 'h', 'r', 'd', 'l', 'u']
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
display_fancy('INPUT', cyphertext)
print(get_top_chars(cyphertext))
print(get_top_short_words(cyphertext, 1))
print(get_top_short_words(cyphertext, 2))
print(get_top_short_words(cyphertext, 3))
print(get_top_double_chars(cyphertext))
print(get_top_initial_letters(cyphertext))
print(get_top_final_letters(cyphertext))
