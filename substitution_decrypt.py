"""
Takes an encrypted string (character substitution) as a command line argument, and tries to decrypt it automatically.
"""

import string
import sys

VALID_CHARS = list(string.ascii_lowercase + ' .,-!?"')
KEY = {c: c for c in VALID_CHARS}  # initialise "no"-key


def get_text_from_file(path):
    """
    Gets text from text file.
    :param path: path to text file
    :return: text as string
    """
    retVal = ""
    with open(path) as file:
        for line in file:
            retVal += line
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
        ret_val += key[c]
    return ret_val


cyphertext = clean_text(get_text_from_file(get_first_commandline_argument()))
print('\nCYPHERTEXT:', cyphertext)
print(apply_substitution_dictionary(cyphertext, KEY))
