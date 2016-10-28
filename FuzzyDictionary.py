from collections import defaultdict
import editdistance


class Dictionary:

    __words_by_pattern__ = defaultdict(set)

    def __init__(self, path_to_wordlist):
        with open(path_to_wordlist) as dict_file:
            for line in dict_file:
                for word in line.split('_'):
                    self.__add_word_to_dictionary__(word.strip().lower())

    def __add_word_to_dictionary__(self, word):
        self.__words_by_pattern__[self.word_pattern_of(word)].add(word)

    def check(self, query):
        words_matching_query_pattern = self.__words_by_pattern__[self.word_pattern_of(query)]
        return query in words_matching_query_pattern

    def suggest(self, query):
        """
        Word suggestions.
        :param query: word
        :return: list with suggestions, best word first
        """
        candidates = self.__words_by_pattern__[self.word_pattern_of(query)]
        candidates_weighted = []
        for i in candidates:
            candidates_weighted.append((i, editdistance.eval(query, i)))
        candidates_sorted = sorted(candidates_weighted, key=lambda x: x[1])
        return [x[0] for x in candidates_sorted]

    def word_pattern_of(self, word):
        chars = []
        ret_val = []
        for c in word:
            if c not in chars:
                chars.append(c)
            ret_val.append(chars.index(c))
        return tuple(ret_val)