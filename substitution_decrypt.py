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
    # MOST_COMMON_CHARS_ENG = ' etaoinshrdlu'
    MOST_COMMON_CHARS_ENG = ' et'
    char_counter = defaultdict(int)
    for char in cyphertext:
        char_counter[char] += 1
    MOST_COMMON_CHARS_DOC = ''.join([x[0] for x in sorted(char_counter.items(), key=lambda x: x[1], reverse=True)])
    sub_key = {}
    for x, Y in zip(MOST_COMMON_CHARS_DOC, MOST_COMMON_CHARS_ENG):
        sub_key[x] = Y
    return apply_substitution_dictionary(cyphertext, sub_key), sub_key


def stage2(cyphertext):
    """
    Searches for most common short words
    :param cyphertext: after stage 2
    :return: new cyphertext, sub-key
    """
    # MOST_COMMON_ONE_CHAR_WORDS_ENG = ['a', 'i']
    # MOST_COMMON_TWO_CHAR_WORDS_ENG = ['of', 'to', 'in']
    # MOST_COMMON_THREE_CHAR_WORDS_ENG = ['the', 'and', 'for']
    MOST_COMMON_ONE_CHAR_WORDS_ENG = ['a']
    MOST_COMMON_TWO_CHAR_WORDS_ENG = ['of']
    MOST_COMMON_THREE_CHAR_WORDS_ENG = ['the']
    one_char_word_counter = defaultdict(int)
    two_char_word_counter = defaultdict(int)
    three_char_word_counter = defaultdict(int)
    sub_key = {}
    for token in cyphertext.split():
        if len(token) == 1:
            one_char_word_counter[token] += 1
        if len(token) == 2:
            two_char_word_counter[token] += 1
        if len(token) == 3:
            three_char_word_counter[token] += 1
    MOST_COMMON_ONE_CHAR_WORDS_DOC = [x[0] for x in
                                      sorted(one_char_word_counter.items(), key=lambda x: x[1], reverse=True)]
    MOST_COMMON_TWO_CHAR_WORDS_DOC = [x[0] for x in
                                      sorted(two_char_word_counter.items(), key=lambda x: x[1], reverse=True)]
    MOST_COMMON_THREE_CHAR_WORDS_DOC = [x[0] for x in
                                        sorted(three_char_word_counter.items(), key=lambda x: x[1], reverse=True)]
    for x, Y in zip(MOST_COMMON_ONE_CHAR_WORDS_DOC, MOST_COMMON_ONE_CHAR_WORDS_ENG):
        sub_key[x] = Y
    for x, Y in list(zip(MOST_COMMON_TWO_CHAR_WORDS_DOC, MOST_COMMON_TWO_CHAR_WORDS_ENG)) + list(
            zip(MOST_COMMON_THREE_CHAR_WORDS_DOC, MOST_COMMON_THREE_CHAR_WORDS_ENG)):
        for x_c, X_c in zip(x, Y):
            sub_key[x_c] = X_c
    return apply_substitution_dictionary(cyphertext, sub_key), sub_key


def stage3(cyphertext):
    """
    Searches for most common char doubles
    :param cyphertext: after stage 3
    :return: new cyphertext, sub-key
    """
    sub_key = {}
    char_double_counter = defaultdict(int)
    print(len(cyphertext))
    for i in range(len(cyphertext)-1):
        a, b = cyphertext[i], cyphertext[i + 1]
        if a == b and a != ' ':
            print(a+b,a, b)
            char_double_counter[a + b] += 1
    print(char_double_counter)
    return apply_substitution_dictionary(cyphertext, sub_key), sub_key


##############################################################################
cyphertext = clean_text(get_text_from_file(get_first_commandline_argument()))
display_fancy('INPUT', cyphertext)

cypher_stage1, key_stage_1 = stage1(cyphertext)
display_fancy('STAGE 1 - CHARACTER STATS', cypher_stage1)
cypher_stage2, key_stage_2 = stage2(cypher_stage1)
display_fancy('STAGE 2 - SHORT WORDS STATISTICS', cypher_stage2)
cypher_stage3, key_stage_3 = stage3(cypher_stage2)
display_fancy('STAGE 3 - CHAR DOUBLES STATISTICS', cypher_stage3)
