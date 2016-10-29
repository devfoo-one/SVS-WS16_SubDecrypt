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
        """
        Returns true if word is found within dictionary
        :param query: word
        :return: True/False if found or not
        """
        query = query.lower()
        words_matching_query_pattern = self.__words_by_pattern__[self.word_pattern_of(query)]
        return query in words_matching_query_pattern

    def suggest(self, query):
        """
        Word suggestions.
        :param query: String, word
        :return: list with suggestions, best word first
        """
        query = query.lower()
        candidates = self.__words_by_pattern__[self.word_pattern_of(query)]
        candidates_weighted = []
        for i in candidates:
            candidates_weighted.append((i, editdistance.eval(query, i)))
        candidates_weighted.sort(key=lambda x: x[1])
        return [x[0] for x in candidates_weighted]

    def best_edit_distance(self, query):
        """
        Returns the edit distance of the nearest word match.
        Best case would be that the word has been found, and edit-distance = 0
        :param query: String, word
        :return: Integer
        """
        query = query.lower()
        best_matches = self.suggest(query)
        if len(best_matches) != 0:
            return editdistance.eval(query.lower(), best_matches[0])
        else:
            return len(query) * 10


    def word_pattern_of(self, word):
        """
        Calculates word-pattern, like 'abba', 'xyyx' = (0,1,1,0)
        :param word: String, word
        :return: word pattern tuple
        """
        word = word.lower()
        chars = []
        ret_val = []
        for c in word:
            if c not in chars:
                chars.append(c)
            ret_val.append(chars.index(c))
        return tuple(ret_val)
