"""
Takes an encrypted string (character substitution) as a command line argument, and tries to decrypt it automatically.
"""
import string
import sys
from collections import defaultdict

VALID_CHARS = list(string.ascii_lowercase + ' .,-!?"')
KEY = {}


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




def stage1(cyphertext):
    """
    Searches for most common characters and replaces them with the most common characters of the english language.
    http://www.simonsingh.net/The_Black_Chamber/hintsandtips.html
    :param c: cyphertext after stage 1
    :return: new cyphertext, sub-key
    """
    MOST_COMMON_CHARS_ENG = ' et'
    # MOST_COMMON_CHARS_ENG = ' etaoin'
    # MOST_COMMON_CHARS_ENG = ' etaoinshrdlu'
    char_counter = defaultdict(int)
    for char in cyphertext:
        char_counter[char] += 1
    MOST_COMMON_CHARS_DOC = ''.join([x[0] for x in sorted(char_counter.items(), key=lambda x: x[1], reverse=True)])
    sub_key = {}
    print(sorted(char_counter.items(), key=lambda x: x[1], reverse=True))
    for x, X in zip(MOST_COMMON_CHARS_DOC, MOST_COMMON_CHARS_ENG):
        sub_key[x] = X
    return apply_substitution_dictionary(cyphertext, sub_key), sub_key


def stage2(cyphertext):
    """
    Searches for most common short words
    :param cyphertext: after stage 2
    :return: new cyphertext, sub-key
    """
    one_char_word_counter = defaultdict(int)
    two_char_word_counter = defaultdict(int)
    three_char_word_counter = defaultdict(int)

    for token in cyphertext.split():
        if len(token) == 1:
            one_char_word_counter[token] += 1
        if len(token) == 2:
            two_char_word_counter[token] += 1
        if len(token) == 3:
            three_char_word_counter[token] += 1
    print(sorted(one_char_word_counter.items(), key=lambda x: x[1], reverse=True))
    print(sorted(two_char_word_counter.items(), key=lambda x: x[1], reverse=True))
    print(sorted(three_char_word_counter.items(), key=lambda x: x[1], reverse=True))

    return 'nothing', 'nothing'


##############################################################################
cyphertext = clean_text(get_text_from_file(get_first_commandline_argument()))
display_fancy('INPUT', cyphertext)

cypher_stage1, key_stage_1 = stage1(cyphertext)
display_fancy('STAGE 1 - CHARACTER STATS', cypher_stage1)
cypher_stage2, key_stage_2 = stage2(cypher_stage1)
display_fancy('STAGE 2 - BIGRAM STATISTICS', cypher_stage2)
