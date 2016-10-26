"""
Takes an encrypted string (character substitution) as a command line argument, and tries to decrypt it automatically.
"""
import random
import string
import sys
from collections import defaultdict, Counter

import itertools
from statistics import mean

VALID_CHARS = list(string.ascii_lowercase + ' .,-!?"')  # WARNING: DO NOT USE '_'


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
            if c == ' ':
                ret_val += '_'
            else:
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
        if a == b and a != ' ' and b != ' ':
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


def score_text(text):
    """
    Returns the number of word matches within a text
    :param text:
    :return: Number of word matches
    """
    hits = 0
    for word in text.split():
        if word in COMMON_WORDS:
            hits += 1
    return hits


def most_common_dict(dicts):
    """
    Calculates an average dictionary out of given dicts of the same dimensions and keys.
    Includes only items that occour as twice as much as the average.
    :param dicts: list with dicts
    :return: dict
    """
    retVal = {}
    keys = dicts[0].keys()
    for k in keys:
        values = []
        for d in dicts:
            values.append(d[k])
        most_common_item_for_k = sorted(Counter(values).items(), key=lambda x: x[1], reverse=True)[0]
        if most_common_item_for_k[1] > 2 * mean(Counter(values).values()):
            retVal[k] = most_common_item_for_k[0]
    return retVal


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

# https://github.com/first20hours/google-10000-english
COMMON_WORDS = ['that', 'this', 'with', 'from', 'your', 'have', 'more', 'will', 'home', 'page', 'free', 'time', 'they',
                'site', 'what', 'news', 'only', 'when', 'here', 'also', 'help', 'view', 'been', 'were', 'some', 'like',
                'than', 'find', 'date', 'back', 'list', 'name', 'just', 'over', 'year', 'into', 'next', 'used', 'work',
                'last', 'most', 'data', 'make', 'them', 'post', 'city', 'such', 'best', 'then', 'good', 'well', 'info',
                'high', 'each', 'very', 'book', 'read', 'need', 'many', 'user', 'said', 'does', 'mail', 'full', 'life',
                'know', 'days', 'part', 'real', 'item', 'ebay', 'must', 'made', 'line', 'send', 'type', 'take', 'area',
                'want', 'long', 'code', 'show', 'even', 'much', 'sign', 'file', 'link', 'open', 'case', 'same', 'both',
                'game', 'care', 'down', 'size', 'shop', 'text', 'rate', 'form', 'love', 'john', 'main', 'call', 'save',
                'york', 'card', 'jobs', 'food', 'sale', 'teen', 'room', 'join', 'west', 'look', 'left', 'team', 'week',
                'note', 'live', 'june', 'plan', 'cost', 'july', 'test', 'come', 'cart', 'play', 'less', 'blog', 'park',
                'side', 'give', 'sell', 'body', 'east', 'club', 'road', 'gift', 'hard', 'four', 'blue', 'easy', 'star',
                'hand', 'keep', 'baby', 'term', 'film', 'head', 'cell', 'self', 'away', 'once', 'sure', 'cars', 'tell',
                'able', 'gold', 'arts', 'past', 'five', 'upon', 'says', 'land', 'done', 'ever', 'word', 'bill', 'talk',
                'kids', 'true', 'else', 'mark', 'rock', 'tips', 'plus', 'auto', 'edit', 'fast', 'fact', 'unit', 'tech',
                'meet', 'feel', 'bank', 'risk', 'town', 'girl', 'toys', 'golf', 'loan', 'wide', 'sort', 'half', 'step',
                'none', 'paul', 'lake', 'sony', 'fire', 'chat', 'html', 'loss', 'face', 'base', 'near', 'stay', 'turn',
                'mean', 'king', 'copy', 'drug', 'pics', 'cash', 'seen', 'port', 'stop', 'soon', 'held', 'mind', 'lost',
                'tour', 'menu', 'hope', 'wish', 'role', 'came', 'fine', 'hour', 'bush', 'huge', 'kind', 'move', 'logo',
                'nice', 'sent', 'band', 'lead', 'went', 'mode', 'fund', 'male', 'took', 'song', 'cnet', 'late', 'fall',
                'idea', 'tool', 'hill', 'maps', 'deal', 'hold', 'safe', 'feed', 'hall', 'anti', 'ship', 'paid', 'hair',
                'tree', 'thus', 'wall', 'wine', 'vote', 'ways', 'rule', 'told', 'feet', 'door', 'cool', 'asia', 'uses',
                'java', 'pass', 'fees', 'skin', 'prev', 'mary', 'ring', 'iraq', 'boys', 'deep', 'rest', 'pool', 'mini',
                'fish', 'pack', 'born', 'race', 'debt', 'core', 'sets', 'wood', 'rent', 'dark', 'host', 'isbn', 'fair',
                'ohio', 'gets', 'dead', 'mike', 'trip', 'poor', 'eyes', 'farm', 'lord', 'hear', 'goes', 'wife', 'hits',
                'zone', 'jack', 'flat', 'flow', 'path', 'laws', 'skip', 'diet', 'army', 'gear', 'lots', 'firm', 'jump',
                'dvds', 'ball', 'goal', 'sold', 'wind', 'palm', 'pain', 'xbox', 'oral', 'ford', 'edge', 'root', 'pink',
                'shot', 'cold', 'foot', 'mass', 'heat', 'wild', 'miss', 'task', 'soft', 'fuel', 'walk', 'wait', 'rose',
                'pick', 'load', 'tags', 'guys', 'drop', 'rich', 'ipod', 'seem', 'hire', 'gave', 'ones', 'rank', 'kong',
                'died', 'inch', 'snow', 'camp', 'fill', 'gone', 'fort', 'gene', 'disc', 'boat', 'icon', 'ends', 'cast',
                'felt', 'soul', 'aids', 'flag', 'atom', 'iron', 'void', 'disk', 'desk', 'dave', 'hong', 'vice', 'duty',
                'bear', 'gain', 'lack', 'iowa', 'knew', 'zoom', 'blow', 'clip', 'wire', 'tape', 'spam', 'acid', 'cent',
                'null', 'zero', 'roll', 'bath', 'font', 'beta', 'fail', 'jazz', 'bags', 'wear', 'rare', 'bars', 'dual',
                'rise', 'bird', 'lady', 'fans', 'dell', 'seat', 'bids', 'toll', 'cape', 'mine', 'whom', 'math', 'dogs',
                'moon', 'fear', 'wars', 'kept', 'beat', 'arms', 'utah', 'hide', 'slow', 'faqs', 'nine', 'eric', 'spot',
                'grow', 'rain', 'onto', 'diff', 'bass', 'hole', 'pets', 'ride', 'pair', 'runs', 'yeah', 'evil', 'euro',
                'peak', 'salt', 'bell', 'jeff', 'lane', 'kill', 'ages', 'plug', 'cook', 'perl', 'bike', 'lose', 'seek',
                'tony', 'kits', 'soil', 'matt', 'exit', 'iran', 'keys', 'wave', 'holy', 'acts', 'mesh', 'dean', 'poll',
                'unix', 'bond', 'jean', 'visa', 'pure', 'lens', 'draw', 'warm', 'babe', 'crew', 'legs', 'rear', 'node',
                'lock', 'mile', 'mens', 'bowl', 'tank', 'navy', 'dish', 'adam', 'slot', 'gray', 'demo', 'hate', 'rice',
                'loop', 'gary', 'vary', 'rome', 'arab', 'milk', 'boot', 'push', 'misc', 'alan', 'dear', 'beer', 'jose',
                'jane', 'earn', 'twin', 'dont', 'bits', 'suit', 'chip', 'char', 'echo', 'grid', 'voip', 'pull', 'nasa',
                'nick', 'plot', 'pump', 'anne', 'exam', 'ryan', 'beds', 'grey', 'bold', 'scan', 'aged', 'bulk', 'pmid',
                'cute', 'para', 'seed', 'peer', 'meat', 'alex', 'bang', 'bone', 'bugs', 'gate', 'tone', 'busy', 'neck',
                'wing', 'tiny', 'rail', 'tube', 'belt', 'luck', 'dial', 'gang', 'cake', 'semi', 'andy', 'cafe', 'till',
                'shoe', 'sand', 'seal', 'lies', 'pipe', 'deck', 'thin', 'sick', 'dose', 'lets', 'cats', 'greg', 'folk',
                'okay', 'hist', 'lift', 'lisa', 'mall', 'fell', 'yard', 'sean', 'pour', 'tion', 'dust', 'wiki', 'kent',
                'adds', 'ward', 'roof', 'kiss', 'rush', 'mpeg', 'yoga', 'lamp', 'rico', 'phil', 'http', 'glad', 'wins',
                'rack', 'boss', 'ross', 'anna', 'solo', 'tall', 'pdas', 'nova', 'wake', 'drum', 'foto', 'ease', 'tabs',
                'pine', 'tend', 'gulf', 'rick', 'hunt', 'thai', 'fred', 'mill', 'burn', 'labs', 'sole', 'laid', 'clay',
                'weak', 'blvd', 'wise', 'odds', 'marc', 'sons', 'leaf', 'cuba', 'silk', 'kate', 'wolf', 'fits', 'kick',
                'meal', 'hurt', 'slip', 'cuts', 'mars', 'caps', 'pill', 'meta', 'mint', 'spin', 'wash', 'aims', 'ieee',
                'corp', 'soap', 'axis', 'guns', 'hero', 'punk', 'duke', 'pace', 'wage', 'dawn', 'carl', 'coat', 'rica',
                'doll', 'peru', 'nike', 'reed', 'mice', 'temp', 'vast', 'wrap', 'mood', 'quiz', 'beam', 'tops', 'shut',
                'ncaa', 'thou', 'mask', 'coal', 'lion', 'goto', 'neil', 'beef', 'hats', 'surf', 'hook', 'cord', 'crop',
                'lite', 'sing', 'tons', 'hang', 'hood', 'fame', 'eggs', 'ruby', 'mins', 'stem', 'drew', 'tune', 'corn',
                'puts', 'grew', 'trek', 'ties', 'brad', 'jury', 'tail', 'lawn', 'soup', 'byte', 'nose', 'oclc', 'juan',
                'thru', 'jews', 'trim', 'espn', 'quit', 'lung', 'todd', 'doug', 'sees', 'bull', 'cole', 'mart', 'tale',
                'lynn', 'docs', 'coin', 'fake', 'cure', 'arch', 'hdtv', 'asin', 'bomb', 'harm', 'deer', 'oven', 'noon',
                'cams', 'joel', 'proc', 'mate', 'chef', 'isle', 'slim', 'luke', 'comp', 'pete', 'spec', 'penn', 'midi',
                'tied', 'dale', 'oils', 'sept', 'unto', 'pays', 'lang', 'stud', 'fold', 'phys', 'pole', 'mega', 'bend',
                'moms', 'glen', 'lips', 'pond', 'tire', 'chad', 'josh', 'drag', 'ripe', 'rely', 'scsi', 'nuts', 'nail',
                'span', 'joke', 'univ', 'pads', 'inns', 'cups', 'foam', 'poem', 'asks', 'bean', 'bias', 'swim', 'nano',
                'loud', 'rats', 'stat', 'cruz', 'bios', 'thee', 'ruth', 'pray', 'pope', 'jeep', 'bare', 'hung', 'mono',
                'tile', 'apps', 'ciao', 'knee', 'prep', 'chem', 'pros', 'cant', 'sara', 'joan', 'duck', 'dive', 'fiji',
                'audi', 'raid', 'volt', 'dirt', 'acer', 'dist', 'geek', 'xnxx', 'sink', 'grip', 'watt', 'pins', 'reno',
                'polo', 'horn', 'prot', 'frog', 'logs', 'snap', 'jpeg', 'swap', 'flip', 'buzz', 'nuke', 'boom', 'calm',
                'fork', 'troy', 'zope', 'gmbh', 'sims', 'tray', 'sage', 'suse', 'cave', 'wool', 'eyed', 'grab', 'oops',
                'trap', 'fool', 'karl', 'dies', 'jail', 'ipaq', 'comm', 'lace', 'ugly', 'hart', 'ment', 'biol', 'rows',
                'treo', 'gods', 'poly', 'ears', 'fist', 'mere', 'cons', 'taxi', 'worn', 'shaw', 'expo', 'deny', 'bali',
                'judy', 'trio', 'cube', 'rugs', 'fate', 'gras', 'oval', 'soma', 'href', 'benz', 'wifi', 'tier', 'earl',
                'guam', 'cite', 'mess', 'rope', 'dump', 'hose', 'pubs', 'mild', 'clan', 'sync', 'mesa', 'hull', 'shed',
                'memo', 'tide', 'funk', 'reel', 'bind', 'rand', 'buck', 'usgs', 'acre', 'lows', 'aqua', 'chen', 'emma',
                'pest', 'reef', 'chan', 'beth', 'jill', 'sofa', 'dans', 'viii', 'tent', 'dept', 'hack', 'dare', 'hawk',
                'lamb', 'junk', 'lucy', 'hans', 'poet', 'epic', 'sake', 'sans', 'lean', 'dude', 'luis', 'alto', 'gore',
                'cult', 'dash', 'cage', 'divx', 'hugh', 'jake', 'eval', 'ping', 'flux', 'muze', 'oman', 'rage', 'adsl',
                'prix', 'avon', 'rays', 'walt', 'acne', 'libs', 'undo', 'dana', 'halo', 'gays', 'exec', 'maui', 'vids',
                'yale', 'doom', 'owen', 'bite', 'issn', 'myth', 'weed', 'oecd', 'dice', 'quad', 'dock', 'mods', 'hint',
                'msie', 'buys', 'pork', 'barn', 'fare', 'asus', 'bald', 'fuji', 'leon', 'mold', 'dame', 'herb', 'alot',
                'idle', 'cove', 'casa', 'eden', 'incl', 'reid', 'flex', 'rosa', 'hash', 'lazy', 'carb', 'pens', 'worm',
                'deaf', 'mats', 'blah', 'mime', 'feof', 'usda', 'keen', 'peas', 'urls', 'owns', 'zinc', 'guru', 'levy',
                'grad', 'bras', 'kyle', 'pale', 'gaps', 'tear', 'nest', 'nato', 'gale', 'stan', 'idol', 'moss', 'cork',
                'mali', 'dome', 'heel', 'yang', 'dumb', 'feat', 'ntsc', 'usps', 'conf', 'glow', 'oaks', 'erik', 'paso',
                'norm', 'ware', 'jade', 'foul', 'keno', 'seas', 'pose', 'mrna', 'goat', 'sail', 'sega', 'cdna', 'bolt',
                'gage', 'urge', 'smtp', 'kurt', 'neon', 'ours', 'lone', 'cope', 'lime', 'kirk', 'bool', 'spas', 'jets',
                'intl', 'yarn', 'knit', 'pike', 'hugo', 'gzip', 'ctrl', 'bent', 'laos', 'about', 'search', 'other',
                'which', 'their', 'there', 'contact', 'business', 'online', 'first', 'would', 'services', 'these',
                'click', 'service', 'price', 'people', 'state', 'email', 'health', 'world', 'products', 'music',
                'should', 'product', 'system', 'policy', 'number', 'please', 'support', 'message', 'after', 'software',
                'video', 'where', 'rights', 'public', 'books', 'school', 'through', 'links', 'review', 'years', 'order',
                'privacy', 'items', 'company', 'group', 'under', 'general', 'research', 'january', 'reviews', 'program',
                'games', 'could', 'great', 'united', 'hotel', 'center', 'store', 'travel', 'comments', 'report',
                'member', 'details', 'terms', 'before', 'hotels', 'right', 'because', 'local', 'those', 'using',
                'results', 'office', 'national', 'design', 'posted', 'internet', 'address', 'within', 'states', 'phone',
                'shipping', 'reserved', 'subject', 'between', 'forum', 'family', 'based', 'black', 'check', 'special',
                'prices', 'website', 'index', 'being', 'women', 'today', 'south', 'project', 'pages', 'version',
                'section', 'found', 'sports', 'house', 'related', 'security', 'county', 'american', 'photo', 'members',
                'power', 'while', 'network', 'computer', 'systems', 'three', 'total', 'place', 'download', 'without',
                'access', 'think', 'north', 'current', 'posts', 'media', 'control', 'water', 'history', 'pictures',
                'personal', 'since', 'guide', 'board', 'location', 'change', 'white', 'small', 'rating', 'children',
                'during', 'return', 'students', 'shopping', 'account', 'times', 'sites', 'level', 'digital', 'profile',
                'previous', 'events', 'hours', 'image', 'title', 'another', 'shall', 'property', 'class', 'still',
                'money', 'quality', 'every', 'listing', 'content', 'country', 'private', 'little', 'visit', 'tools',
                'reply', 'customer', 'december', 'compare', 'movies', 'include', 'college', 'value', 'article',
                'provide', 'source', 'author', 'press', 'learn', 'around', 'print', 'course', 'canada', 'process',
                'stock', 'training', 'credit', 'point', 'science', 'advanced', 'sales', 'english', 'estate', 'select',
                'windows', 'photos', 'thread', 'category', 'large', 'gallery', 'table', 'register', 'however',
                'october', 'november', 'market', 'library', 'really', 'action', 'start', 'series', 'model', 'features',
                'industry', 'human', 'provided', 'required', 'second', 'movie', 'forums', 'march', 'better', 'yahoo',
                'going', 'medical', 'friend', 'server', 'study', 'staff', 'articles', 'feedback', 'again', 'looking',
                'issues', 'april', 'never', 'users', 'complete', 'street', 'topic', 'comment', 'things', 'working',
                'against', 'standard', 'person', 'below', 'mobile', 'party', 'payment', 'login', 'student', 'programs',
                'offers', 'legal', 'above', 'recent', 'stores', 'problem', 'memory', 'social', 'august', 'quote',
                'language', 'story', 'options', 'rates', 'create', 'young', 'america', 'field', 'paper', 'single',
                'example', 'girls', 'password', 'latest', 'question', 'changes', 'night', 'texas', 'poker', 'status',
                'browse', 'issue', 'range', 'building', 'seller', 'court', 'february', 'always', 'result', 'audio',
                'light', 'write', 'offer', 'groups', 'given', 'files', 'event', 'release', 'analysis', 'request',
                'china', 'making', 'picture', 'needs', 'possible', 'might', 'month', 'major', 'areas', 'future',
                'space', 'cards', 'problems', 'london', 'meeting', 'become', 'interest', 'child', 'enter', 'share',
                'similar', 'garden', 'schools', 'million', 'added', 'listed', 'learning', 'energy', 'delivery',
                'popular', 'stories', 'journal', 'reports', 'welcome', 'central', 'images', 'notice', 'original',
                'radio', 'until', 'color', 'council', 'includes', 'track', 'archive', 'others', 'format', 'least',
                'society', 'months', 'safety', 'friends', 'trade', 'edition', 'messages', 'further', 'updated',
                'having', 'provides', 'david', 'already', 'green', 'studies', 'close', 'common', 'drive', 'specific',
                'several', 'living', 'called', 'short', 'display', 'limited', 'powered', 'means', 'director', 'daily',
                'beach', 'natural', 'whether', 'period', 'planning', 'database', 'official', 'weather', 'average',
                'window', 'france', 'region', 'island', 'record', 'direct', 'records', 'district', 'calendar', 'costs',
                'style', 'front', 'update', 'parts', 'early', 'miles', 'sound', 'resource', 'present', 'either',
                'document', 'works', 'material', 'written', 'federal', 'hosting', 'rules', 'final', 'adult', 'tickets',
                'thing', 'centre', 'cheap', 'finance', 'minutes', 'third', 'gifts', 'europe', 'reading', 'topics',
                'cover', 'usually', 'together', 'videos', 'percent', 'function', 'getting', 'global', 'economic',
                'player', 'projects', 'lyrics', 'often', 'submit', 'germany', 'amount', 'watch', 'included', 'though',
                'thanks', 'deals', 'various', 'words', 'linux', 'james', 'weight', 'heart', 'received', 'choose',
                'archives', 'points', 'magazine', 'error', 'camera', 'clear', 'receive', 'domain', 'methods', 'chapter',
                'makes', 'policies', 'beauty', 'manager', 'india', 'position', 'taken', 'listings', 'models', 'michael',
                'known', 'cases', 'florida', 'simple', 'quick', 'wireless', 'license', 'friday', 'whole', 'annual',
                'later', 'basic', 'shows', 'google', 'church', 'method', 'purchase', 'active', 'response', 'practice',
                'hardware', 'figure', 'holiday', 'enough', 'designed', 'along', 'among', 'death', 'writing', 'speed',
                'brand', 'discount', 'higher', 'effects', 'created', 'remember', 'yellow', 'increase', 'kingdom',
                'thought', 'stuff', 'french', 'storage', 'japan', 'doing', 'loans', 'shoes', 'entry', 'nature',
                'orders', 'africa', 'summary', 'growth', 'notes', 'agency', 'monday', 'european', 'activity',
                'although', 'western', 'income', 'force', 'overall', 'river', 'package', 'contents', 'players',
                'engine', 'album', 'regional', 'supplies', 'started', 'views', 'plans', 'double', 'build', 'screen',
                'exchange', 'types', 'lines', 'continue', 'across', 'benefits', 'needed', 'season', 'apply', 'someone',
                'anything', 'printer', 'believe', 'effect', 'asked', 'sunday', 'casino', 'volume', 'cross', 'anyone',
                'mortgage', 'silver', 'inside', 'solution', 'mature', 'rather', 'weeks', 'addition', 'supply',
                'nothing', 'certain', 'running', 'lower', 'union', 'jewelry', 'clothing', 'names', 'robert', 'homepage',
                'skills', 'islands', 'advice', 'career', 'military', 'rental', 'decision', 'leave', 'british', 'teens',
                'woman', 'sellers', 'middle', 'cable', 'taking', 'values', 'division', 'coming', 'tuesday', 'object',
                'lesbian', 'machine', 'length', 'actually', 'score', 'client', 'returns', 'capital', 'follow', 'sample',
                'shown', 'saturday', 'england', 'culture', 'flash', 'george', 'choice', 'starting', 'thursday',
                'courses', 'consumer', 'airport', 'foreign', 'artist', 'outside', 'levels', 'channel', 'letter',
                'phones', 'ideas', 'summer', 'allow', 'degree', 'contract', 'button', 'releases', 'homes', 'super',
                'matter', 'custom', 'virginia', 'almost', 'located', 'multiple', 'asian', 'editor', 'cause', 'focus',
                'featured', 'rooms', 'female', 'thomas', 'primary', 'cancer', 'numbers', 'reason', 'browser', 'spring',
                'answer', 'voice', 'friendly', 'schedule', 'purpose', 'feature', 'comes', 'police', 'everyone',
                'approach', 'cameras', 'brown', 'physical', 'medicine', 'ratings', 'chicago', 'forms', 'glass', 'happy',
                'smith', 'wanted', 'thank', 'unique', 'survey', 'prior', 'sport', 'ready', 'animal', 'sources',
                'mexico', 'regular', 'secure', 'simply', 'evidence', 'station', 'round', 'paypal', 'favorite', 'option',
                'master', 'valley', 'recently', 'probably', 'rentals', 'built', 'blood', 'improve', 'larger',
                'networks', 'earth', 'parents', 'nokia', 'impact', 'transfer', 'kitchen', 'strong', 'carolina',
                'wedding', 'hospital', 'ground', 'overview', 'owners', 'disease', 'italy', 'perfect', 'classic',
                'basis', 'command', 'cities', 'william', 'express', 'award', 'distance', 'peter', 'ensure', 'involved',
                'extra', 'partners', 'budget', 'rated', 'guides', 'success', 'maximum', 'existing', 'quite', 'selected',
                'amazon', 'patients', 'warning', 'horse', 'forward', 'flowers', 'stars', 'lists', 'owner', 'retail',
                'animals', 'useful', 'directly', 'housing', 'takes', 'bring', 'catalog', 'searches', 'trying', 'mother',
                'traffic', 'joined', 'input', 'strategy', 'agent', 'valid', 'modern', 'senior', 'ireland', 'teaching',
                'grand', 'testing', 'trial', 'charge', 'units', 'instead', 'canadian', 'normal', 'wrote', 'ships',
                'entire', 'leading', 'metal', 'positive', 'fitness', 'chinese', 'opinion', 'football', 'abstract',
                'output', 'funds', 'greater', 'likely', 'develop', 'artists', 'guest', 'seems', 'trust', 'contains',
                'session', 'multi', 'republic', 'vacation', 'century', 'academic', 'graphics', 'indian', 'expected',
                'grade', 'dating', 'pacific', 'mountain', 'filter', 'mailing', 'vehicle', 'longer', 'consider',
                'northern', 'behind', 'panel', 'floor', 'german', 'buying', 'match', 'proposed', 'default', 'require',
                'outdoor', 'morning', 'allows', 'protein', 'plant', 'reported', 'politics', 'partner', 'authors',
                'boards', 'faculty', 'parties', 'mission', 'string', 'sense', 'modified', 'released', 'stage',
                'internal', 'goods', 'unless', 'richard', 'detailed', 'japanese', 'approved', 'target', 'except',
                'ability', 'maybe', 'moving', 'brands', 'places', 'pretty', 'spain', 'southern', 'yourself', 'winter',
                'battery', 'youth', 'pressure', 'boston', 'keywords', 'medium', 'break', 'purposes', 'dance', 'itself',
                'defined', 'papers', 'playing', 'awards', 'studio', 'reader', 'virtual', 'device', 'answers', 'remote',
                'external', 'apple', 'offered', 'theory', 'enjoy', 'remove', 'surface', 'minimum', 'visual', 'variety',
                'teachers', 'martin', 'manual', 'block', 'subjects', 'agents', 'repair', 'civil', 'steel', 'songs',
                'fixed', 'wrong', 'hands', 'finally', 'updates', 'desktop', 'classes', 'paris', 'sector', 'capacity',
                'requires', 'jersey', 'fully', 'father', 'electric', 'quotes', 'officer', 'driver', 'respect',
                'unknown', 'worth', 'teacher', 'workers', 'georgia', 'peace', 'campus', 'showing', 'creative', 'coast',
                'benefit', 'progress', 'funding', 'devices', 'grant', 'agree', 'fiction', 'watches', 'careers',
                'beyond', 'families', 'museum', 'blogs', 'accepted', 'former', 'complex', 'agencies', 'parent',
                'spanish', 'michigan', 'columbia', 'setting', 'scale', 'stand', 'economy', 'highest', 'helpful',
                'monthly', 'critical', 'frame', 'musical', 'angeles', 'employee', 'chief', 'gives', 'bottom',
                'packages', 'detail', 'changed', 'heard', 'begin', 'colorado', 'royal', 'clean', 'switch', 'russian',
                'largest', 'african', 'titles', 'relevant', 'justice', 'connect', 'bible', 'basket', 'applied',
                'weekly', 'demand', 'suite', 'vegas', 'square', 'chris', 'advance', 'auction', 'allowed', 'correct',
                'charles', 'nation', 'selling', 'piece', 'sheet', 'seven', 'older', 'illinois', 'elements', 'species',
                'cells', 'module', 'resort', 'facility', 'random', 'pricing', 'minister', 'motion', 'looks', 'fashion',
                'visitors', 'monitor', 'trading', 'forest', 'calls', 'whose', 'coverage', 'couple', 'giving', 'chance',
                'vision', 'ending', 'clients', 'actions', 'listen', 'discuss', 'accept', 'naked', 'clinical',
                'sciences', 'markets', 'lowest', 'highly', 'appear', 'lives', 'currency', 'leather', 'patient',
                'actual', 'stone', 'commerce', 'perhaps', 'persons', 'tests', 'village', 'accounts', 'amateur',
                'factors', 'coffee', 'settings', 'buyer', 'cultural', 'steve', 'easily', 'poster', 'closed', 'holidays',
                'zealand', 'balance', 'graduate', 'replies', 'initial', 'label', 'thinking', 'scott', 'canon', 'league',
                'waste', 'minute', 'provider', 'optional', 'sections', 'chair', 'fishing', 'effort', 'phase', 'fields',
                'fantasy', 'letters', 'motor', 'context', 'install', 'shirt', 'apparel', 'crime', 'count', 'breast',
                'johnson', 'quickly', 'dollars', 'websites', 'religion', 'claim', 'driving', 'surgery', 'patch',
                'measures', 'kansas', 'chemical', 'doctor', 'reduce', 'brought', 'himself', 'enable', 'exercise',
                'santa', 'leader', 'diamond', 'israel', 'servers', 'alone', 'meetings', 'seconds', 'jones', 'arizona',
                'keyword', 'flight', 'congress', 'username', 'produced', 'italian', 'pocket', 'saint', 'freedom',
                'argument', 'creating', 'drugs', 'joint', 'premium', 'fresh', 'attorney', 'upgrade', 'factor',
                'growing', 'stream', 'hearing', 'eastern', 'auctions', 'therapy', 'entries', 'dates', 'signed', 'upper',
                'serious', 'prime', 'samsung', 'limit', 'began', 'louis', 'steps', 'errors', 'shops', 'efforts',
                'informed', 'thoughts', 'creek', 'worked', 'quantity', 'urban', 'sorted', 'myself', 'tours', 'platform',
                'labor', 'admin', 'nursing', 'defense', 'machines', 'heavy', 'covered', 'recovery', 'merchant',
                'expert', 'protect', 'solid', 'became', 'orange', 'vehicles', 'prevent', 'theme', 'campaign', 'marine',
                'guitar', 'finding', 'examples', 'saying', 'spirit', 'claims', 'motorola', 'affairs', 'touch',
                'intended', 'towards', 'goals', 'election', 'suggest', 'branch', 'charges', 'serve', 'reasons', 'magic',
                'mount', 'smart', 'talking', 'latin', 'avoid', 'manage', 'corner', 'oregon', 'element', 'birth',
                'virus', 'abuse', 'requests', 'separate', 'quarter', 'tables', 'define', 'racing', 'facts', 'column',
                'plants', 'faith', 'chain', 'identify', 'avenue', 'missing', 'domestic', 'sitemap', 'moved', 'houston',
                'reach', 'mental', 'viewed', 'moment', 'extended', 'sequence', 'attack', 'sorry', 'centers', 'opening',
                'damage', 'reserve', 'recipes', 'gamma', 'plastic', 'produce', 'placed', 'truth', 'counter', 'failure',
                'follows', 'weekend', 'dollar', 'ontario', 'films', 'bridge', 'native', 'williams', 'movement',
                'printing', 'baseball', 'owned', 'approval', 'draft', 'chart', 'played', 'contacts', 'jesus', 'readers',
                'clubs', 'jackson', 'equal', 'matching', 'offering', 'shirts', 'profit', 'leaders', 'posters',
                'variable', 'expect', 'parking', 'compared', 'workshop', 'russia', 'codes', 'kinds', 'seattle',
                'golden', 'teams', 'lighting', 'senate', 'forces', 'funny', 'brother', 'turned', 'portable', 'tried',
                'returned', 'pattern', 'named', 'theatre', 'laser', 'earlier', 'sponsor', 'warranty', 'indiana',
                'harry', 'objects', 'delete', 'evening', 'assembly', 'nuclear', 'taxes', 'mouse', 'signal', 'criminal',
                'issued', 'brain', 'sexual', 'powerful', 'dream', 'obtained', 'false', 'flower', 'passed', 'supplied',
                'falls', 'opinions', 'promote', 'stated', 'stats', 'hawaii', 'appears', 'carry', 'decided', 'covers',
                'hello', 'designs', 'maintain', 'tourism', 'priority', 'adults', 'clips', 'savings', 'graphic',
                'payments', 'binding', 'brief', 'ended', 'winning', 'eight', 'straight', 'script', 'served', 'wants',
                'prepared', 'dining', 'alert', 'atlanta', 'dakota', 'queen', 'credits', 'clearly', 'handle', 'sweet',
                'criteria', 'pubmed', 'diego', 'truck', 'behavior', 'enlarge', 'revenue', 'measure', 'changing',
                'votes', 'looked', 'festival', 'ocean', 'flights', 'experts', 'signs', 'depth', 'whatever', 'logged',
                'laptop', 'vintage', 'train', 'exactly', 'explore', 'maryland', 'concept', 'nearly', 'eligible',
                'checkout', 'reality', 'forgot', 'handling', 'origin', 'gaming', 'feeds', 'billion', 'scotland',
                'faster', 'dallas', 'bought', 'nations', 'route', 'followed', 'broken', 'frank', 'alaska', 'battle',
                'anime', 'speak', 'protocol', 'query', 'equity', 'speech', 'rural', 'shared', 'sounds', 'judge',
                'bytes', 'forced', 'fight', 'height', 'speaker', 'filed', 'obtain', 'offices', 'designer', 'remain',
                'managed', 'failed', 'marriage', 'korea', 'banks', 'secret', 'kelly', 'leads', 'negative', 'austin',
                'toronto', 'theater', 'springs', 'missouri', 'andrew', 'perform', 'healthy', 'assets', 'injury',
                'joseph', 'ministry', 'drivers', 'lawyer', 'figures', 'married', 'proposal', 'sharing', 'portal',
                'waiting', 'birthday', 'gratis', 'banking', 'brian', 'toward', 'slightly', 'assist', 'conduct',
                'lingerie', 'calling', 'serving', 'profiles', 'miami', 'comics', 'matters', 'houses', 'postal',
                'controls', 'breaking', 'combined', 'ultimate', 'wales', 'minor', 'finish', 'noted', 'reduced',
                'physics', 'spent', 'extreme', 'samples', 'davis', 'daniel', 'reviewed', 'forecast', 'removed', 'helps',
                'singles', 'cycle', 'amounts', 'contain', 'accuracy', 'sleep', 'pharmacy', 'brazil', 'creation',
                'static', 'scene', 'hunter', 'crystal', 'famous', 'writer', 'chairman', 'violence', 'oklahoma',
                'speakers', 'drink', 'academy', 'dynamic', 'gender', 'cleaning', 'concerns', 'vendor', 'intel',
                'officers', 'referred', 'supports', 'regions', 'junior', 'rings', 'meaning', 'ladies', 'henry',
                'ticket', 'guess', 'agreed', 'soccer', 'import', 'posting', 'presence', 'instant', 'viewing',
                'majority', 'christ', 'aspects', 'austria', 'ahead', 'scheme', 'utility', 'preview', 'manner', 'matrix',
                'devel', 'despite', 'strength', 'turkey', 'proper', 'degrees', 'delta', 'seeking', 'inches', 'phoenix',
                'shares', 'daughter', 'standing', 'comfort', 'colors', 'cisco', 'ordering', 'alpha', 'appeal', 'cruise',
                'bonus', 'bookmark', 'specials', 'disney', 'adobe', 'smoking', 'becomes', 'drives', 'alabama',
                'improved', 'trees', 'achieve', 'dress', 'dealer', 'nearby', 'carried', 'happen', 'exposure',
                'gambling', 'refer', 'miller', 'outdoors', 'clothes', 'caused', 'luxury', 'babes', 'frames', 'indeed',
                'circuit', 'layer', 'printed', 'removal', 'easier', 'printers', 'adding', 'kentucky', 'mostly',
                'taylor', 'prints', 'spend', 'factory', 'interior', 'revised', 'optical', 'relative', 'amazing',
                'clock', 'identity', 'suites', 'feeling', 'hidden', 'victoria', 'serial', 'relief', 'revision', 'ratio',
                'planet', 'copies', 'recipe', 'permit', 'seeing', 'proof', 'tennis', 'bedroom', 'empty', 'instance',
                'licensed', 'orlando', 'bureau', 'maine', 'ideal', 'specs', 'recorded', 'pieces', 'finished', 'parks',
                'dinner', 'lawyers', 'sydney', 'stress', 'cream', 'trends', 'discover', 'patterns', 'boxes', 'hills',
                'fourth', 'advisor', 'aware', 'wilson', 'shape', 'irish', 'stations', 'remains', 'greatest', 'firms',
                'operator', 'generic', 'usage', 'charts', 'mixed', 'census', 'exist', 'wheel', 'transit', 'compact',
                'poetry', 'lights', 'tracking', 'angel', 'keeping', 'attempt', 'matches', 'width', 'noise', 'engines',
                'forget', 'array', 'accurate', 'stephen', 'climate', 'alcohol', 'greek', 'managing', 'sister',
                'walking', 'explain', 'smaller', 'newest', 'happened', 'extent', 'sharp', 'lesbians', 'export',
                'managers', 'aircraft', 'modules', 'sweden', 'conflict', 'versions', 'employer', 'occur', 'knows',
                'describe', 'concern', 'backup', 'citizens', 'heritage', 'holding', 'trouble', 'spread', 'coach',
                'kevin', 'expand', 'audience', 'assigned', 'jordan', 'affect', 'virgin', 'raised', 'directed',
                'dealers', 'sporting', 'helping', 'affected', 'totally', 'plate', 'expenses', 'indicate', 'blonde',
                'anderson', 'organic', 'albums', 'cheats', 'guests', 'hosted', 'diseases', 'nevada', 'thailand',
                'agenda', 'anyway', 'tracks', 'advisory', 'logic', 'template', 'prince', 'circle', 'grants', 'anywhere',
                'atlantic', 'edward', 'investor', 'leaving', 'wildlife', 'cooking', 'speaking', 'sponsors', 'respond',
                'sizes', 'plain', 'entered', 'launch', 'checking', 'costa', 'belgium', 'guidance', 'trail', 'symbol',
                'crafts', 'highway', 'buddy', 'observed', 'setup', 'booking', 'glossary', 'fiscal', 'styles', 'denver',
                'filled', 'channels', 'ericsson', 'appendix', 'notify', 'blues', 'portion', 'scope', 'supplier',
                'cables', 'cotton', 'biology', 'dental', 'killed', 'border', 'ancient', 'debate', 'starts', 'causes',
                'arkansas', 'leisure', 'learned', 'notebook', 'explorer', 'historic', 'attached', 'opened', 'husband',
                'disabled', 'crazy', 'upcoming', 'britain', 'concert', 'scores', 'comedy', 'adopted', 'weblog',
                'linear', 'bears', 'carrier', 'edited', 'constant', 'mouth', 'jewish', 'meter', 'linked', 'portland',
                'concepts', 'reflect', 'deliver', 'wonder', 'lessons', 'fruit', 'begins', 'reform', 'alerts', 'treated',
                'mysql', 'relating', 'assume', 'alliance', 'confirm', 'neither', 'lewis', 'howard', 'offline', 'leaves',
                'engineer', 'replace', 'checks', 'reached', 'becoming', 'safari', 'sugar', 'stick', 'allen', 'relation',
                'enabled', 'genre', 'slide', 'montana', 'tested', 'enhance', 'exact', 'bound', 'adapter', 'formal',
                'hockey', 'storm', 'micro', 'colleges', 'laptops', 'showed', 'editors', 'threads', 'supreme',
                'brothers', 'presents', 'dolls', 'estimate', 'cancel', 'limits', 'weapons', 'paint', 'delay', 'pilot',
                'outlet', 'czech', 'novel', 'ultra', 'winner', 'idaho', 'episode', 'potter', 'plays', 'bulletin',
                'modify', 'oxford', 'truly', 'epinions', 'painting', 'universe', 'patent', 'eating', 'planned',
                'watching', 'lodge', 'mirror', 'sterling', 'sessions', 'kernel', 'stocks', 'buyers', 'journals',
                'jennifer', 'antonio', 'charged', 'broad', 'taiwan', 'chosen', 'greece', 'swiss', 'sarah', 'clark',
                'terminal', 'nights', 'behalf', 'liquid', 'nebraska', 'salary', 'foods', 'gourmet', 'guard', 'properly',
                'orleans', 'saving', 'empire', 'resume', 'twenty', 'newly', 'raise', 'prepare', 'avatar', 'illegal',
                'hundreds', 'lincoln', 'helped', 'premier', 'tomorrow', 'decide', 'consent', 'drama', 'visiting',
                'downtown', 'keyboard', 'contest', 'bands', 'suitable', 'millions', 'lunch', 'audit', 'chamber',
                'guinea', 'findings', 'muscle', 'clicking', 'polls', 'typical', 'tower', 'yours', 'chicken', 'attend',
                'shower', 'sending', 'jason', 'tonight', 'holdem', 'shell', 'province', 'catholic', 'governor',
                'seemed', 'swimming', 'spyware', 'formula', 'solar', 'catch', 'pakistan', 'reliable', 'doubt', 'finder',
                'unable', 'periods', 'tasks', 'attacks', 'const', 'doors', 'symptoms', 'resorts', 'biggest', 'memorial',
                'visitor', 'forth', 'insert', 'gateway', 'alumni', 'drawing', 'ordered', 'fighting', 'happens',
                'romance', 'bruce', 'split', 'themes', 'powers', 'heaven', 'pregnant', 'twice', 'focused', 'egypt',
                'bargain', 'cellular', 'norway', 'vermont', 'asking', 'blocks', 'normally', 'hunting', 'diabetes',
                'shift', 'bodies', 'cutting', 'simon', 'writers', 'marks', 'flexible', 'loved', 'mapping', 'numerous',
                'birds', 'indexed', 'superior', 'saved', 'paying', 'cartoon', 'shots', 'moore', 'granted', 'choices',
                'carbon', 'spending', 'magnetic', 'registry', 'crisis', 'outlook', 'massive', 'denmark', 'employed',
                'bright', 'treat', 'header', 'poverty', 'formed', 'piano', 'sheets', 'patrick', 'puerto', 'displays',
                'plasma', 'allowing', 'earnings', 'mystery', 'journey', 'delaware', 'bidding', 'risks', 'banner',
                'charter', 'barbara', 'counties', 'ports', 'dreams', 'blogger', 'stands', 'teach', 'occurred', 'rapid',
                'hairy', 'reverse', 'deposit', 'seminar', 'latina', 'wheels', 'sexcam', 'specify', 'dutch', 'formats',
                'depends', 'boots', 'holds', 'router', 'concrete', 'editing', 'poland', 'folder', 'womens', 'upload',
                'pulse', 'voting', 'courts', 'notices', 'detroit', 'metro', 'toshiba', 'strip', 'pearl', 'accident',
                'resident', 'possibly', 'airline', 'regard', 'exists', 'smooth', 'strike', 'flashing', 'narrow',
                'threat', 'surveys', 'sitting', 'putting', 'vietnam', 'trailer', 'castle', 'gardens', 'missed',
                'malaysia', 'antique', 'labels', 'willing', 'acting', 'heads', 'stored', 'logos', 'milfs', 'antiques',
                'density', 'hundred', 'strange', 'mention', 'parallel', 'honda', 'amended', 'operate', 'bills',
                'bathroom', 'stable', 'opera', 'doctors', 'lesson', 'cinema', 'asset', 'drinking', 'reaction', 'blank',
                'enhanced', 'entitled', 'severe', 'generate', 'deluxe', 'humor', 'monitors', 'lived', 'duration',
                'pursuant', 'fabric', 'visits', 'tight', 'domains', 'contrast', 'flying', 'berlin', 'siemens',
                'adoption', 'meant', 'capture', 'pounds', 'buffalo', 'plane', 'desire', 'camping', 'meets', 'welfare',
                'caught', 'marked', 'driven', 'measured', 'medline', 'bottle', 'marshall', 'massage', 'rubber',
                'closing', 'tampa', 'thousand', 'legend', 'grace', 'susan', 'adams', 'python', 'monster', 'villa',
                'columns', 'hamilton', 'cookies', 'inner', 'tutorial', 'entity', 'cruises', 'holder', 'portugal',
                'lawrence', 'roman', 'duties', 'valuable', 'ethics', 'forever', 'dragon', 'captain', 'imagine',
                'brings', 'heating', 'scripts', 'stereo', 'taste', 'dealing', 'commit', 'airlines', 'liberal',
                'livecam', 'trips', 'sides', 'turns', 'cache', 'jacket', 'oracle', 'matthew', 'lease', 'aviation',
                'hobbies', 'proud', 'excess', 'disaster', 'console', 'commands', 'giant', 'achieved', 'injuries',
                'shipped', 'seats', 'alarm', 'voltage', 'anthony', 'nintendo', 'usual', 'loading', 'stamps', 'appeared',
                'franklin', 'angle', 'vinyl', 'mining', 'ongoing', 'worst', 'imaging', 'betting', 'liberty', 'wyoming',
                'convert', 'analyst', 'garage', 'exciting', 'thongs', 'ringtone', 'finland', 'morgan', 'derived',
                'pleasure', 'honor', 'oriented', 'eagle', 'desktops', 'pants', 'columbus', 'nurse', 'prayer', 'quiet',
                'postage', 'producer', 'cheese', 'comic', 'crown', 'maker', 'crack', 'picks', 'semester', 'fetish',
                'applies', 'casinos', 'smoke', 'apache', 'filters', 'craft', 'apart', 'fellow', 'blind', 'lounge',
                'coins', 'gross', 'strongly', 'hilton', 'proteins', 'horror', 'familiar', 'capable', 'douglas',
                'debian', 'epson', 'elected', 'carrying', 'victory', 'madison', 'editions', 'mainly', 'ethnic', 'actor',
                'finds', 'fifth', 'citizen', 'vertical', 'prize', 'occurs', 'absolute', 'consists', 'anytime',
                'soldiers', 'guardian', 'lecture', 'layout', 'classics', 'horses', 'dirty', 'wayne', 'donate', 'taught',
                'worker', 'alive', 'temple', 'prove', 'wings', 'breaks', 'genetic', 'waters', 'promise', 'prefer',
                'ridge', 'cabinet', 'modem', 'harris', 'bringing', 'evaluate', 'tiffany', 'tropical', 'collect',
                'toyota', 'streets', 'vector', 'shaved', 'turning', 'buffer', 'purple', 'larry', 'mutual', 'pipeline',
                'syntax', 'prison', 'skill', 'chairs', 'everyday', 'moves', 'inquiry', 'ethernet', 'checked', 'exhibit',
                'throw', 'trend', 'sierra', 'visible', 'desert', 'oldest', 'rhode', 'mercury', 'steven', 'handbook',
                'navigate', 'worse', 'summit', 'victims', 'spaces', 'burning', 'escape', 'coupons', 'somewhat',
                'receiver', 'cialis', 'boats', 'glance', 'scottish', 'arcade', 'richmond', 'russell', 'tells',
                'obvious', 'fiber', 'graph', 'covering', 'platinum', 'judgment', 'bedrooms', 'talks', 'filing',
                'foster', 'modeling', 'passing', 'awarded', 'trials', 'tissue', 'clinton', 'masters', 'bonds',
                'alberta', 'commons', 'fraud', 'spectrum', 'arrival', 'pottery', 'emphasis', 'roger', 'aspect',
                'awesome', 'mexican', 'counts', 'priced', 'crash', 'desired', 'inter', 'closer', 'assumes', 'heights',
                'shadow', 'riding', 'firefox', 'expense', 'grove', 'venture', 'clinic', 'korean', 'healing', 'princess',
                'entering', 'packet', 'spray', 'studios', 'buttons', 'funded', 'thompson', 'winners', 'extend', 'roads',
                'dublin', 'rolling', 'memories', 'nelson', 'arrived', 'creates', 'faces', 'tourist', 'mayor', 'murder',
                'adequate', 'senator', 'yield', 'grades', 'cartoons', 'digest', 'lodging', 'hence', 'entirely',
                'replaced', 'radar', 'rescue', 'losses', 'combat', 'reducing', 'stopped', 'lakes', 'closely', 'diary',
                'kings', 'shooting', 'flags', 'baker', 'launched', 'shock', 'walls', 'abroad', 'ebony', 'drawn',
                'arthur', 'visited', 'walker', 'suggests', 'beast', 'operated', 'targets', 'overseas', 'dodge',
                'counsel', 'pizza', 'invited', 'yards', 'gordon', 'farmers', 'queries', 'ukraine', 'absence', 'nearest',
                'cluster', 'vendors', 'whereas', 'serves', 'woods', 'surprise', 'partial', 'shoppers', 'couples',
                'ranking', 'jokes', 'simpson', 'twiki', 'sublime', 'palace', 'verify', 'globe', 'trusted', 'copper',
                'dicke', 'kerry', 'receipt', 'supposed', 'ordinary', 'nobody', 'ghost', 'applying', 'pride', 'knowing',
                'reporter', 'keith', 'champion', 'cloudy', 'linda', 'chile', 'plenty', 'sentence', 'throat', 'ignore',
                'maria', 'uniform', 'wealth', 'vacuum', 'dancing', 'brass', 'writes', 'plaza', 'outcomes', 'survival',
                'quest', 'publish', 'trans', 'jonathan', 'whenever', 'lifetime', 'pioneer', 'booty', 'acrobat',
                'plates', 'acres', 'venue', 'athletic', 'thermal', 'essays', 'vital', 'telling', 'fairly', 'coastal',
                'config', 'charity', 'excel', 'modes', 'campbell', 'stupid', 'harbor', 'hungary', 'traveler', 'segment',
                'realize', 'enemy', 'puzzle', 'rising', 'aluminum', 'wells', 'wishlist', 'opens', 'insight', 'secrets',
                'lucky', 'latter', 'thick', 'trailers', 'repeat', 'syndrome', 'philips', 'penalty', 'glasses',
                'enables', 'iraqi', 'builder', 'vista', 'jessica', 'chips', 'terry', 'flood', 'arena', 'pupils',
                'stewart', 'outcome', 'expanded', 'casual', 'grown', 'polish', 'lovely', 'extras', 'centres', 'jerry',
                'clause', 'smile', 'lands', 'troops', 'indoor', 'bulgaria', 'armed', 'broker', 'charger', 'believed',
                'cooling', 'trucks', 'divorce', 'laura', 'shopper', 'tokyo', 'partly', 'nikon', 'candy', 'pills',
                'tiger', 'donald', 'folks', 'sensor', 'exposed', 'telecom', 'angels', 'deputy', 'sealed', 'loaded',
                'scenes', 'boost', 'spanking', 'founded', 'chronic', 'icons', 'moral', 'catering', 'finger', 'keeps',
                'pound', 'locate', 'trained', 'roses', 'bread', 'tobacco', 'wooden', 'motors', 'tough', 'roberts',
                'incident', 'gonna', 'dynamics', 'decrease', 'cumshots', 'chest', 'pension', 'billy', 'revenues',
                'emerging', 'worship', 'craig', 'herself', 'churches', 'damages', 'reserves', 'solve', 'shorts',
                'minority', 'diverse', 'johnny', 'recorder', 'facing', 'nancy', 'tones', 'passion', 'sight', 'defence',
                'patches', 'refund', 'towns', 'trembl', 'divided', 'emails', 'cyprus', 'insider', 'seminars', 'makers',
                'hearts', 'worry', 'carter', 'legacy', 'pleased', 'danger', 'vitamin', 'widely', 'phrase', 'genuine',
                'raising', 'paradise', 'hybrid', 'reads', 'roles', 'glory', 'bigger', 'billing', 'diesel', 'versus',
                'combine', 'exceed', 'saudi', 'fault', 'babies', 'karen', 'compiled', 'romantic', 'revealed', 'albert',
                'examine', 'jimmy', 'graham', 'bristol', 'margaret', 'compaq', 'slowly', 'rugby', 'portions', 'infant',
                'sectors', 'samuel', 'fluid', 'grounds', 'regards', 'unlike', 'equation', 'baskets', 'wright', 'barry',
                'proven', 'cached', 'warren', 'studied', 'reviewer', 'involves', 'profits', 'devil', 'grass', 'comply',
                'marie', 'florist', 'cherry', 'deutsch', 'kenya', 'webcam', 'funeral', 'nutten', 'earrings', 'enjoyed',
                'chapters', 'charlie', 'quebec', 'dennis', 'francis', 'sized', 'manga', 'noticed', 'socket', 'silent',
                'literary', 'signals', 'theft', 'swing', 'symbols', 'humans', 'analog', 'facial', 'choosing', 'talent',
                'dated', 'seeker', 'wisdom', 'shoot', 'boundary', 'packard', 'offset', 'payday', 'philip', 'elite',
                'holders', 'believes', 'swedish', 'poems', 'deadline', 'robot', 'witness', 'collins', 'equipped',
                'stages', 'winds', 'powder', 'broadway', 'acquired', 'assess', 'stones', 'entrance', 'gnome', 'roots',
                'losing', 'attempts', 'gadgets', 'noble', 'glasgow', 'impacts', 'gospel', 'shore', 'loves', 'induced',
                'knight', 'loose', 'linking', 'appeals', 'earned', 'illness', 'islamic', 'pending', 'parker', 'lebanon',
                'kennedy', 'teenage', 'triple', 'cooper', 'vincent', 'secured', 'unusual', 'answered', 'slots',
                'disorder', 'routine', 'toolbar', 'rocks', 'titans', 'wearing', 'sought', 'genes', 'mounted', 'habitat',
                'firewall', 'median', 'scanner', 'herein', 'animated', 'judicial', 'integer', 'bachelor', 'attitude',
                'engaged', 'falling', 'basics', 'montreal', 'carpet', 'struct', 'lenses', 'binary', 'genetics',
                'attended', 'dropped', 'walter', 'besides', 'hosts', 'moments', 'atlas', 'strings', 'feels', 'torture',
                'deleted', 'mitchell', 'ralph', 'warner', 'embedded', 'inkjet', 'wizard', 'corps', 'actors', 'liver',
                'liable', 'brochure', 'morris', 'petition', 'eminem', 'recall', 'antenna', 'picked', 'assumed',
                'belief', 'killing', 'bikini', 'memphis', 'shoulder', 'decor', 'lookup', 'texts', 'harvard', 'brokers',
                'diameter', 'ottawa', 'podcast', 'seasons', 'refine', 'bidder', 'singer', 'evans', 'herald', 'literacy',
                'fails', 'aging', 'plugin', 'diving', 'invite', 'alice', 'latinas', 'suppose', 'involve', 'moderate',
                'terror', 'younger', 'thirty', 'opposite', 'rapidly', 'dealtime', 'intro', 'mercedes', 'clerk', 'mills',
                'outline', 'tramadol', 'holland', 'receives', 'jeans', 'fonts', 'refers', 'favor', 'veterans', 'sigma',
                'xhtml', 'occasion', 'victim', 'demands', 'sleeping', 'careful', 'arrive', 'sunset', 'tracked',
                'moreover', 'minimal', 'lottery', 'framed', 'aside', 'licence', 'michelle', 'essay', 'dialogue',
                'camps', 'declared', 'aaron', 'handheld', 'trace', 'disposal', 'florists', 'packs', 'switches',
                'romania', 'consult', 'greatly', 'blogging', 'cycling', 'midnight', 'commonly', 'inform', 'turkish',
                'pentium', 'quantum', 'murray', 'intent', 'largely', 'pleasant', 'announce', 'spoke', 'arrow',
                'sampling', 'rough', 'weird', 'inspired', 'holes', 'weddings', 'blade', 'suddenly', 'oxygen', 'cookie',
                'meals', 'canyon', 'meters', 'merely', 'passes', 'pointer', 'stretch', 'durham', 'permits', 'muslim',
                'sleeve', 'netscape', 'cleaner', 'cricket', 'feeding', 'stroke', 'township', 'rankings', 'robin',
                'robinson', 'strap', 'sharon', 'crowd', 'olympic', 'remained', 'entities', 'customs', 'rainbow',
                'roulette', 'decline', 'gloves', 'israeli', 'medicare', 'skiing', 'cloud', 'valve', 'hewlett',
                'explains', 'proceed', 'flickr', 'feelings', 'knife', 'jamaica', 'shelf', 'timing', 'liked', 'adopt',
                'denied', 'fotos', 'britney', 'freeware', 'donation', 'outer', 'deaths', 'rivers', 'tales', 'katrina',
                'islam', 'nodes', 'thumbs', 'seeds', 'cited', 'targeted', 'skype', 'realized', 'twelve', 'founder',
                'decade', 'gamecube', 'dispute', 'tired', 'titten', 'adverse', 'excerpt', 'steam', 'drinks', 'voices',
                'acute', 'climbing', 'stood', 'perfume', 'carol', 'honest', 'albany', 'restore', 'stack', 'somebody',
                'curve', 'creator', 'amber', 'museums', 'coding', 'tracker', 'passage', 'trunk', 'hiking', 'pierre',
                'jelsoft', 'headset', 'oakland', 'colombia', 'waves', 'camel', 'lamps', 'suicide', 'archived', 'arabia',
                'juice', 'chase', 'logical', 'sauce', 'extract', 'panama', 'payable', 'courtesy', 'athens', 'judges',
                'retired', 'remarks', 'detected', 'decades', 'walked', 'arising', 'nissan', 'bracelet', 'juvenile',
                'afraid', 'acoustic', 'railway', 'cassette', 'pointed', 'causing', 'mistake', 'norton', 'locked',
                'fusion', 'mineral', 'steering', 'beads', 'fortune', 'canvas', 'parish', 'claimed', 'screens',
                'cemetery', 'planner', 'croatia', 'flows', 'stadium', 'fewer', 'coupon', 'nurses', 'proxy', 'lanka',
                'edwards', 'contests', 'costume', 'tagged', 'berkeley', 'voted', 'killer', 'bikes', 'gates', 'adjusted',
                'bishop', 'pulled', 'shaped', 'seasonal', 'farmer', 'counters', 'slave', 'cultures', 'norfolk',
                'coaching', 'examined', 'encoding', 'heroes', 'painted', 'lycos', 'zdnet', 'artwork', 'cosmetic',
                'resulted', 'portrait', 'ethical', 'carriers', 'mobility', 'floral', 'builders', 'struggle', 'schemes',
                'neutral', 'fisher', 'spears', 'bedding', 'joining', 'heading', 'equally', 'bearing', 'combo',
                'seniors', 'worlds', 'guilty', 'haven', 'tablet', 'charm', 'violent', 'basin', 'ranch', 'crossing',
                'cottage', 'drunk', 'crimes', 'resolved', 'mozilla', 'toner', 'latex', 'branches', 'anymore', 'delhi',
                'holdings', 'alien', 'locator', 'broke', 'nepal', 'zimbabwe', 'browsing', 'resolve', 'melissa',
                'moscow', 'thesis', 'nylon', 'discs', 'rocky', 'bargains', 'frequent', 'nigeria', 'ceiling', 'pixels',
                'ensuring', 'hispanic', 'anybody', 'diamonds', 'fleet', 'untitled', 'bunch', 'totals', 'marriott',
                'singing', 'afford', 'starring', 'referral', 'optimal', 'distinct', 'turner', 'sucking', 'cents',
                'reuters', 'spoken', 'omega', 'stayed', 'civic', 'manuals', 'watched', 'saver', 'thereof', 'grill',
                'redeem', 'rogers', 'grain', 'regime', 'wanna', 'wishes', 'depend', 'differ', 'ranging', 'monica',
                'repairs', 'breath', 'candle', 'hanging', 'colored', 'verified', 'formerly', 'situated', 'seeks',
                'herbal', 'loving', 'strictly', 'routing', 'stanley', 'retailer', 'vitamins', 'elegant', 'gains',
                'renewal', 'opposed', 'deemed', 'scoring', 'brooklyn', 'sisters', 'critics', 'spots', 'hacker',
                'madrid', 'margin', 'solely', 'salon', 'norman', 'turbo', 'headed', 'voters', 'madonna', 'murphy',
                'thinks', 'thats', 'soldier', 'phillips', 'aimed', 'justin', 'interval', 'mirrors', 'tricks', 'reset',
                'brush', 'expansys', 'panels', 'repeated', 'assault', 'spare', 'kodak', 'tongue', 'bowling', 'danish',
                'monkey', 'filename', 'skirt', 'florence', 'invest', 'honey', 'analyzes', 'drawings', 'scenario',
                'lovers', 'atomic', 'approx', 'arabic', 'gauge', 'junction', 'faced', 'rachel', 'solving', 'weekends',
                'produces', 'chains', 'kingston', 'sixth', 'engage', 'deviant', 'quoted', 'adapters', 'farms',
                'imports', 'cheat', 'bronze', 'sandy', 'suspect', 'macro', 'sender', 'crucial', 'adjacent', 'tuition',
                'spouse', 'exotic', 'viewer', 'signup', 'threats', 'puzzles', 'reaching', 'damaged', 'receptor',
                'laugh', 'surgical', 'destroy', 'citation', 'pitch', 'autos', 'premises', 'perry', 'proved', 'imperial',
                'dozen', 'benjamin', 'teeth', 'cloth', 'studying', 'stamp', 'lotus', 'salmon', 'olympus', 'cargo',
                'salem', 'starter', 'upgrades', 'likes', 'butter', 'pepper', 'weapon', 'luggage', 'burden', 'tapes',
                'zones', 'races', 'stylish', 'maple', 'grocery', 'offshore', 'depot', 'kenneth', 'blend', 'harrison',
                'julie', 'emission', 'finest', 'realty', 'janet', 'apparent', 'phpbb', 'autumn', 'probe', 'toilet',
                'ranked', 'jackets', 'routes', 'packed', 'excited', 'outreach', 'helen', 'mounting', 'recover', 'lopez',
                'balanced', 'timely', 'talked', 'upskirts', 'debug', 'delayed', 'chuck', 'explicit', 'villas', 'ebook',
                'exclude', 'peeing', 'brooks', 'newton', 'anxiety', 'bingo', 'whilst', 'spatial', 'ceramic', 'prompt',
                'precious', 'minds', 'annually', 'scanners', 'xanax', 'fingers', 'sunny', 'ebooks', 'delivers',
                'necklace', 'leeds', 'cedar', 'arranged', 'theaters', 'advocacy', 'raleigh', 'threaded', 'qualify',
                'blair', 'hopes', 'mason', 'diagram', 'burns', 'pumps', 'footwear', 'beijing', 'peoples', 'victor',
                'mario', 'attach', 'licenses', 'utils', 'removing', 'advised', 'spider', 'ranges', 'pairs', 'trails',
                'hudson', 'isolated', 'calgary', 'interim', 'assisted', 'divine', 'approve', 'chose', 'compound',
                'abortion', 'dialog', 'venues', 'blast', 'wellness', 'calcium', 'newport', 'indians', 'shield',
                'harvest', 'membrane', 'prague', 'previews', 'locally', 'pickup', 'mothers', 'nascar', 'iceland',
                'candles', 'sailing', 'sacred', 'morocco', 'chrome', 'tommy', 'refused', 'brake', 'exterior',
                'greeting', 'ecology', 'oliver', 'congo', 'botswana', 'delays', 'olive', 'cyber', 'verizon', 'scored',
                'clone', 'dicks', 'velocity', 'lambda', 'relay', 'composed', 'tears', 'oasis', 'baseline', 'angry',
                'silicon', 'compete', 'lover', 'belong', 'honolulu', 'beatles', 'rolls', 'thomson', 'barnes', 'malta',
                'daddy', 'ferry', 'rabbit', 'seating', 'exports', 'omaha', 'electron', 'loads', 'heather', 'passport',
                'motel', 'unions', 'treasury', 'warrant', 'solaris', 'frozen', 'occupied', 'royalty', 'scales', 'rally',
                'observer', 'sunshine', 'strain', 'ceremony', 'somehow', 'arrested', 'yamaha', 'hebrew', 'gained',
                'dying', 'laundry', 'stuck', 'solomon', 'placing', 'stops', 'homework', 'adjust', 'assessed',
                'enabling', 'filling', 'imposed', 'silence', 'focuses', 'soviet', 'treaty', 'vocal', 'trainer', 'organ',
                'stronger', 'volumes', 'advances', 'lemon', 'toxic', 'darkness', 'bizrate', 'vienna', 'implied',
                'stanford', 'packing', 'statute', 'rejected', 'satisfy', 'shelter', 'chapel', 'gamespot', 'layers',
                'guided', 'bahamas', 'powell', 'mixture', 'bench', 'rider', 'radius', 'logging', 'hampton', 'borders',
                'butts', 'bobby', 'sheep', 'railroad', 'lectures', 'wines', 'nursery', 'harder', 'cheapest', 'travesti',
                'stuart', 'salvador', 'salad', 'monroe', 'tender', 'paste', 'clouds', 'tanzania', 'preserve',
                'unsigned', 'staying', 'easter', 'theories', 'praise', 'jeremy', 'venice', 'estonia', 'veteran',
                'streams', 'landing', 'signing', 'executed', 'katie', 'showcase', 'integral', 'relax', 'namibia',
                'synopsis', 'hardly', 'prairie', 'reunion', 'composer', 'sword', 'absent', 'sells', 'ecuador', 'hoping',
                'accessed', 'spirits', 'coral', 'pixel', 'float', 'colin', 'imported', 'paths', 'bubble', 'acquire',
                'contrary', 'tribune', 'vessel', 'acids', 'focusing', 'viruses', 'cheaper', 'admitted', 'dairy',
                'admit', 'fancy', 'equality', 'samoa', 'stickers', 'leasing', 'lauren', 'beliefs', 'squad', 'analyze',
                'ashley', 'scroll', 'relate', 'wages', 'suffer', 'forests', 'invalid', 'concerts', 'martial', 'males',
                'retain', 'execute', 'tunnel', 'genres', 'cambodia', 'patents', 'chaos', 'wheat', 'beaver', 'updating',
                'readings', 'kijiji', 'confused', 'compiler', 'eagles', 'bases', 'accused', 'unity', 'bride', 'defines',
                'airports', 'begun', 'brunette', 'packets', 'anchor', 'socks', 'parade', 'trigger', 'gathered', 'essex',
                'slovenia', 'notified', 'beaches', 'folders', 'dramatic', 'surfaces', 'terrible', 'routers', 'pendant',
                'dresses', 'baptist', 'hiring', 'clocks', 'females', 'wallace', 'reflects', 'taxation', 'fever',
                'cuisine', 'surely', 'myspace', 'theorem', 'stylus', 'drums', 'arnold', 'chicks', 'cattle', 'radical',
                'rover', 'treasure', 'reload', 'flame', 'levitra', 'tanks', 'assuming', 'monetary', 'elderly',
                'floating', 'bolivia', 'spell', 'hottest', 'stevens', 'kuwait', 'emily', 'alleged', 'compile',
                'webster', 'struck', 'plymouth', 'warnings', 'bridal', 'annex', 'tribal', 'curious', 'freight',
                'rebate', 'meetup', 'eclipse', 'sudan', 'shuttle', 'stunning', 'cycles', 'affects', 'detect',
                'actively', 'ampland', 'fastest', 'butler', 'injured', 'payroll', 'cookbook', 'courier', 'uploaded',
                'hints', 'collapse', 'americas', 'twinks', 'unlikely', 'techno', 'beverage', 'tribute', 'wired',
                'elvis', 'immune', 'latvia', 'forestry', 'barriers', 'rarely', 'infected', 'martha', 'genesis',
                'barrier', 'argue', 'trains', 'metals', 'bicycle', 'letting', 'arise', 'celtic', 'thereby', 'jamie',
                'particle', 'minerals', 'advise', 'humidity', 'bottles', 'boxing', 'bangkok', 'hughes', 'jeffrey',
                'chess', 'operates', 'brisbane', 'survive', 'oscar', 'menus', 'reveal', 'canal', 'amino', 'herbs',
                'clinics', 'manitoba', 'missions', 'watson', 'lying', 'costumes', 'strict', 'saddam', 'drill',
                'offense', 'bryan', 'protest', 'hobby', 'tries', 'nickname', 'inline', 'washing', 'staffing', 'trick',
                'enquiry', 'closure', 'timber', 'intense', 'playlist', 'showers', 'ruling', 'steady', 'statutes',
                'myers', 'drops', 'wider', 'plugins', 'enrolled', 'sensors', 'screw', 'publicly', 'hourly', 'blame',
                'geneva', 'freebsd', 'reseller', 'handed', 'suffered', 'intake', 'informal', 'tucson', 'heavily',
                'swingers', 'fifty', 'headers', 'mistakes', 'uncle', 'defining', 'counting', 'assure', 'devoted',
                'jacob', 'sodium', 'randy', 'hormone', 'timothy', 'brick', 'naval', 'medieval', 'bridges', 'captured',
                'thehun', 'decent', 'casting', 'dayton', 'shortly', 'cameron', 'carlos', 'donna', 'andreas', 'warrior',
                'diploma', 'cabin', 'innocent', 'scanning', 'valium', 'copying', 'cordless', 'patricia', 'eddie',
                'uganda', 'fired', 'trivia', 'adidas', 'perth', 'grammar', 'syria', 'disagree', 'klein', 'harvey',
                'tires', 'hazard', 'retro', 'livesex', 'gregory', 'episodes', 'boolean', 'circular', 'anger',
                'mainland', 'suits', 'chances', 'interact', 'bizarre', 'glenn', 'auckland', 'olympics', 'fruits',
                'worldsex', 'ribbon', 'startup', 'suzuki', 'trinidad', 'kissing', 'handy', 'exempt', 'crops', 'reduces',
                'geometry', 'slovakia', 'guild', 'gorgeous', 'capitol', 'dishes', 'barbados', 'chrysler', 'nervous',
                'refuse', 'extends', 'mcdonald', 'replica', 'plumbing', 'brussels', 'tribe', 'trades', 'superb',
                'trinity', 'handled', 'legends', 'floors', 'exhaust', 'shanghai', 'speaks', 'burton', 'davidson',
                'copied', 'scotia', 'farming', 'gibson', 'roller', 'batch', 'organize', 'alter', 'nicole', 'latino',
                'ghana', 'edges', 'mixing', 'handles', 'skilled', 'fitted', 'harmony', 'asthma', 'twins', 'triangle',
                'amend', 'oriental', 'reward', 'windsor', 'zambia', 'hydrogen', 'webshots', 'sprint', 'chick',
                'advocate', 'inputs', 'genome', 'escorts', 'thong', 'medal', 'coaches', 'vessels', 'walks', 'knives',
                'arrange', 'artistic', 'honors', 'booth', 'indie', 'unified', 'bones', 'breed', 'detector', 'ignored',
                'polar', 'fallen', 'precise', 'sussex', 'msgid', 'invoice', 'gather', 'backed', 'alfred', 'colonial',
                'carey', 'motels', 'forming', 'embassy', 'danny', 'rebecca', 'slight', 'proceeds', 'indirect',
                'amongst', 'msgstr', 'arrest', 'adipex', 'horizon', 'deeply', 'toolbox', 'marina', 'prizes', 'bosnia',
                'browsers', 'patio', 'surfing', 'lloyd', 'optics', 'pursue', 'overcome', 'attract', 'brighton', 'beans',
                'ellis', 'disable', 'snake', 'succeed', 'leonard', 'lending', 'reminder', 'searched', 'plains',
                'raymond', 'insights', 'sullivan', 'midwest', 'karaoke', 'lonely', 'hereby', 'observe', 'julia',
                'berry', 'collar', 'racial', 'bermuda', 'amanda', 'mobiles', 'kelkoo', 'exhibits', 'terrace',
                'bacteria', 'replied', 'seafood', 'novels', 'ought', 'safely', 'finite', 'kidney', 'fixes', 'sends',
                'durable', 'mazda', 'allied', 'throws', 'moisture', 'roster', 'symantec', 'spencer', 'wichita',
                'nasdaq', 'uruguay', 'timer', 'tablets', 'tuning', 'gotten', 'tyler', 'futures', 'verse', 'highs',
                'wanting', 'custody', 'scratch', 'launches', 'ellen', 'rocket', 'bullet', 'towers', 'racks', 'nasty',
                'latitude', 'tumor', 'deposits', 'beverly', 'mistress', 'trustees', 'watts', 'duncan', 'reprints',
                'bernard', 'forty', 'tubes', 'midlands', 'priest', 'floyd', 'ronald', 'analysts', 'queue', 'trance',
                'locale', 'nicholas', 'bundle', 'hammer', 'invasion', 'runner', 'notion', 'skins', 'mailed', 'fujitsu',
                'spelling', 'arctic', 'exams', 'rewards', 'beneath', 'defend', 'medicaid', 'infrared', 'seventh',
                'welsh', 'belly', 'quarters', 'stolen', 'soonest', 'haiti', 'naturals', 'lenders', 'fitting',
                'fixtures', 'bloggers', 'agrees', 'surplus', 'elder', 'sonic', 'cheers', 'belarus', 'zoning', 'gravity',
                'thumb', 'guitars', 'essence', 'flooring', 'ethiopia', 'mighty', 'athletes', 'humanity', 'holmes',
                'scholars', 'galaxy', 'chester', 'snapshot', 'caring', 'segments', 'dominant', 'twist', 'itunes',
                'stomach', 'buried', 'newbie', 'minimize', 'darwin', 'ranks', 'debut', 'bradley', 'anatomy', 'fraction',
                'defects', 'milton', 'marker', 'clarity', 'sandra', 'adelaide', 'monaco', 'settled', 'folding',
                'emirates', 'airfare', 'vaccine', 'belize', 'promised', 'volvo', 'penny', 'robust', 'bookings',
                'minolta', 'porter', 'jungle', 'ivory', 'alpine', 'andale', 'fabulous', 'remix', 'alias', 'newer',
                'spice', 'implies', 'cooler', 'maritime', 'periodic', 'overhead', 'ascii', 'prospect', 'shipment',
                'breeding', 'donor', 'tension', 'trash', 'shapes', 'manor', 'envelope', 'diane', 'homeland', 'excluded',
                'andrea', 'breeds', 'rapids', 'disco', 'bailey', 'endif', 'emotions', 'incoming', 'lexmark', 'cleaners',
                'eternal', 'cashiers', 'rotation', 'eugene', 'metric', 'minus', 'bennett', 'hotmail', 'joshua',
                'armenia', 'varied', 'grande', 'closest', 'actress', 'assign', 'tigers', 'aurora', 'slides', 'milan',
                'premiere', 'lender', 'villages', 'shade', 'chorus', 'rhythm', 'digit', 'argued', 'dietary', 'symphony',
                'clarke', 'sudden', 'marilyn', 'lions', 'findlaw', 'pools', 'lyric', 'claire', 'speeds', 'matched',
                'carroll', 'rational', 'fighters', 'chambers', 'warming', 'vocals', 'fountain', 'chubby', 'grave',
                'burner', 'finnish', 'gentle', 'deeper', 'muslims', 'footage', 'howto', 'worthy', 'reveals', 'saints',
                'carries', 'devon', 'helena', 'saves', 'regarded', 'marion', 'lobby', 'egyptian', 'tunisia', 'outlined',
                'headline', 'treating', 'punch', 'gotta', 'cowboy', 'bahrain', 'enormous', 'karma', 'consist', 'betty',
                'queens', 'shemales', 'lucas', 'tribes', 'defeat', 'clicks', 'honduras', 'naughty', 'hazards',
                'insured', 'harper', 'mardi', 'tenant', 'cabinets', 'tattoo', 'shake', 'algebra', 'shadows', 'holly',
                'silly', 'mercy', 'hartford', 'freely', 'marcus', 'sunrise', 'wrapping', 'weblogs', 'timeline',
                'belongs', 'readily', 'fence', 'nudist', 'infinite', 'diana', 'ensures', 'lindsay', 'legally', 'shame',
                'civilian', 'fatal', 'remedy', 'realtors', 'briefly', 'genius', 'fighter', 'flesh', 'retreat',
                'adapted', 'barely', 'wherever', 'estates', 'democrat', 'borough', 'failing', 'retained', 'pamela',
                'andrews', 'marble', 'jesse', 'logitech', 'surrey', 'briefing', 'belkin', 'highland', 'modular',
                'brandon', 'giants', 'balloon', 'winston', 'solved', 'hawaiian', 'gratuit', 'consoles', 'qatar',
                'magnet', 'porsche', 'cayman', 'jaguar', 'sheer', 'posing', 'hopkins', 'urgent', 'infants', 'gothic',
                'cylinder', 'witch', 'cohen', 'puppy', 'kathy', 'graphs', 'surround', 'revenge', 'expires', 'enemies',
                'finances', 'accepts', 'enjoying', 'patrol', 'smell', 'italiano', 'carnival', 'roughly', 'sticker',
                'promises', 'divide', 'cornell', 'satin', 'deserve', 'mailto', 'promo', 'worried', 'tunes', 'garbage',
                'combines', 'bradford', 'phrases', 'chelsea', 'boring', 'reynolds', 'speeches', 'reaches', 'schema',
                'catalogs', 'quizzes', 'prefix', 'lucia', 'savannah', 'barrel', 'typing', 'nerve', 'planets', 'deficit',
                'boulder', 'pointing', 'renew', 'coupled', 'myanmar', 'metadata', 'harold', 'circuits', 'floppy',
                'texture', 'handbags', 'somerset', 'incurred', 'antigua', 'thunder', 'caution', 'locks', 'namely',
                'euros', 'pirates', 'aerial', 'rebel', 'origins', 'hired', 'makeup', 'textile', 'nathan', 'tobago',
                'indexes', 'hindu', 'licking', 'markers', 'weights', 'albania', 'lasting', 'wicked', 'kills',
                'roommate', 'webcams', 'pushed', 'slope', 'reggae', 'failures', 'surname', 'theology', 'nails',
                'evident', 'whats', 'rides', 'rehab', 'saturn', 'allergy', 'twisted', 'merit', 'enzyme', 'zshops',
                'planes', 'edmonton', 'tackle', 'disks', 'condo', 'pokemon', 'ambien', 'retrieve', 'vernon', 'worldcat',
                'titanium', 'fairy', 'builds', 'shaft', 'leslie', 'casio', 'deutsche', 'postings', 'kitty', 'drain',
                'monte', 'fires', 'algeria', 'blessed', 'cardiff', 'cornwall', 'favors', 'potato', 'panic', 'sticks',
                'leone', 'excuse', 'reforms', 'basement', 'onion', 'strand', 'sandwich', 'lawsuit', 'cheque', 'banners',
                'reject', 'circles', 'italic', 'beats', 'merry', 'scuba', 'passive', 'valued', 'bangbus', 'courage',
                'verde', 'gazette', 'hitachi', 'batman', 'hearings', 'coleman', 'anaheim', 'textbook', 'dried',
                'luther', 'frontier', 'settle', 'stopping', 'refugees', 'knights', 'palmer', 'derby', 'peaceful',
                'altered', 'pontiac', 'doctrine', 'scenic', 'trainers', 'sewing', 'conclude', 'munich', 'celebs',
                'propose', 'lighter', 'advisors', 'pavilion', 'tactics', 'trusts', 'talented', 'annie', 'pillow',
                'derek', 'shorter', 'harley', 'relying', 'finals', 'paraguay', 'steal', 'parcel', 'refined', 'fifteen',
                'fears', 'predict', 'boutique', 'acrylic', 'rolled', 'tuner', 'peterson', 'shannon', 'toddler',
                'flavor', 'alike', 'homeless', 'horrible', 'hungry', 'metallic', 'blocked', 'warriors', 'cadillac',
                'malawi', 'sagem', 'curtis', 'parental', 'strikes', 'lesser', 'marathon', 'pressing', 'gasoline',
                'dressed', 'scout', 'belfast', 'dealt', 'niagara', 'warcraft', 'charms', 'catalyst', 'trader', 'bucks',
                'denial', 'thrown', 'prepaid', 'raises', 'electro', 'badge', 'wrist', 'analyzed', 'heath', 'ballot',
                'lexus', 'varying', 'remedies', 'validity', 'trustee', 'handjobs', 'weighted', 'angola', 'squirt',
                'performs', 'plastics', 'realm', 'jenny', 'helmet', 'salaries', 'postcard', 'elephant', 'yemen',
                'tsunami', 'scholar', 'nickel', 'buses', 'expedia', 'geology', 'coating', 'wallet', 'cleared',
                'smilies', 'boating', 'drainage', 'shakira', 'corners', 'broader', 'rouge', 'yeast', 'clearing',
                'coated', 'intend', 'louise', 'kenny', 'routines', 'hitting', 'yukon', 'beings', 'aquatic', 'reliance',
                'habits', 'striking', 'podcasts', 'singh', 'gilbert', 'ferrari', 'brook', 'outputs', 'ensemble',
                'insulin', 'assured', 'biblical', 'accent', 'mysimon', 'eleven', 'wives', 'ambient', 'utilize',
                'mileage', 'prostate', 'adaptor', 'auburn', 'unlock', 'hyundai', 'pledge', 'vampire', 'angela',
                'relates', 'nitrogen', 'xerox', 'merger', 'softball', 'firewire', 'nextel', 'framing', 'musician',
                'blocking', 'rwanda', 'sorts', 'vsnet', 'limiting', 'dispatch', 'papua', 'restored', 'armor', 'riders',
                'chargers', 'remark', 'dozens', 'varies', 'rendered', 'picking', 'guards', 'openings', 'councils',
                'kruger', 'pockets', 'granny', 'viral', 'inquire', 'pipes', 'laden', 'aruba', 'cottages', 'realtor',
                'merge', 'edgar', 'develops', 'chassis', 'dubai', 'pushing', 'fleece', 'pierce', 'allan', 'dressing',
                'sperm', 'filme', 'craps', 'frost', 'sally', 'yacht', 'tracy', 'prefers', 'drilling', 'breach', 'whale',
                'tomatoes', 'bedford', 'mustang', 'clusters', 'antibody', 'momentum', 'wiring', 'pastor', 'calvin',
                'shark', 'phases', 'grateful', 'emerald', 'laughing', 'grows', 'cliff', 'tract', 'ballet', 'abraham',
                'bumper', 'webpage', 'garlic', 'hostels', 'shine', 'senegal', 'banned', 'wendy', 'briefs', 'diffs',
                'mumbai', 'ozone', 'radios', 'tariff', 'nvidia', 'opponent', 'pasta', 'muscles', 'serum', 'wrapped',
                'swift', 'runtime', 'inbox', 'focal', 'distant', 'decimal', 'propecia', 'samba', 'hostel', 'employ',
                'mongolia', 'penguin', 'magical', 'miracle', 'manually', 'reprint', 'centered', 'yearly', 'wound',
                'belle', 'writings', 'hamburg', 'cindy', 'fathers', 'charging', 'marvel', 'lined', 'petite', 'terrain',
                'strips', 'gossip', 'rangers', 'rotary', 'discrete', 'beginner', 'boxed', 'cubic', 'sapphire', 'kinase',
                'skirts', 'crawford', 'labeled', 'marking', 'serbia', 'sheriff', 'griffin', 'declined', 'guyana',
                'spies', 'neighbor', 'elect', 'highways', 'thinkpad', 'intimate', 'preston', 'deadly', 'bunny', 'chevy',
                'rounds', 'longest', 'tions', 'dentists', 'flyer', 'dosage', 'variance', 'cameroon', 'baking',
                'adaptive', 'computed', 'needle', 'baths', 'brakes', 'nirvana', 'invision', 'sticky', 'destiny',
                'generous', 'madness', 'emacs', 'climb', 'blowing', 'heated', 'jackie', 'sparc', 'cardiac', 'dover',
                'adrian', 'vatican', 'brutal', 'learners', 'token', 'seekers', 'yields', 'suited', 'numeric', 'skating',
                'kinda', 'aberdeen', 'emperor', 'dylan', 'belts', 'blacks', 'educated', 'rebates', 'burke', 'proudly',
                'inserted', 'pulling', 'basename', 'obesity', 'curves', 'suburban', 'touring', 'clara', 'vertex',
                'tomato', 'andorra', 'expired', 'travels', 'flush', 'waiver', 'hayes', 'delight', 'survivor', 'garcia',
                'cingular', 'moses', 'counted', 'declare', 'johns', 'valves', 'impaired', 'donors', 'jewel', 'teddy',
                'teaches', 'ventures', 'bufing', 'stranger', 'tragedy', 'julian', 'dryer', 'painful', 'velvet',
                'tribunal', 'ruled', 'pensions', 'prayers', 'funky', 'nowhere', 'joins', 'wesley', 'lately', 'scary',
                'mattress', 'mpegs', 'brunei', 'likewise', 'banana', 'slovak', 'cakes', 'mixer', 'remind', 'sbjct',
                'charming', 'tooth', 'annoying', 'stays', 'disclose', 'affair', 'drove', 'washer', 'upset', 'restrict',
                'springer', 'beside', 'mines', 'rebound', 'logan', 'mentor', 'fought', 'baghdad', 'metres', 'pencil',
                'freeze', 'titled', 'sphere', 'ratios', 'concord', 'endorsed', 'walnut', 'lance', 'ladder', 'italia',
                'liberia', 'sherman', 'maximize', 'hansen', 'senators', 'workout', 'bleeding', 'colon', 'lanes',
                'purse', 'optimize', 'stating', 'caroline', 'align', 'bless', 'engaging', 'crest', 'triumph', 'welding',
                'deferred', 'alloy', 'condos', 'plots', 'polished', 'gently', 'tulsa', 'locking', 'casey', 'draws',
                'fridge', 'blanket', 'bloom', 'simpsons', 'elliott', 'fraser', 'justify', 'blades', 'loops', 'surge',
                'trauma', 'tahoe', 'advert', 'possess', 'flashers', 'subaru', 'vanilla', 'picnic', 'souls', 'arrivals',
                'spank', 'hollow', 'vault', 'securely', 'fioricet', 'groove', 'pursuit', 'wires', 'mails', 'backing',
                'sleeps', 'blake', 'travis', 'endless', 'figured', 'orbit', 'niger', 'bacon', 'heater', 'colony',
                'cannon', 'circus', 'promoted', 'forbes', 'moldova', 'paxil', 'spine', 'trout', 'enclosed', 'cooked',
                'thriller', 'transmit', 'apnic', 'fatty', 'gerald', 'pressed', 'scanned', 'hunger', 'mariah', 'joyce',
                'surgeon', 'cement', 'planners', 'disputes', 'textiles', 'missile', 'intranet', 'closes', 'deborah',
                'marco', 'assists', 'gabriel', 'auditor', 'aquarium', 'violin', 'prophet', 'bracket', 'isaac', 'oxide',
                'naples', 'promptly', 'modems', 'harmful', 'prozac', 'sexually', 'dividend', 'newark', 'glucose',
                'phantom', 'playback', 'turtle', 'warned', 'neural', 'fossil', 'hometown', 'badly', 'apollo', 'persian',
                'handmade', 'greene', 'robots', 'grenada', 'scoop', 'earning', 'mailman', 'sanyo', 'nested', 'somalia',
                'movers', 'verbal', 'blink', 'carlo', 'workflow', 'novelty', 'bryant', 'tiles', 'voyuer', 'switched',
                'tamil', 'garmin', 'fuzzy', 'grams', 'richards', 'budgets', 'toolkit', 'render', 'carmen', 'hardwood',
                'erotica', 'temporal', 'forge', 'dense', 'brave', 'awful', 'airplane', 'istanbul', 'impose', 'viewers',
                'asbestos', 'meyer', 'enters', 'savage', 'willow', 'resumes', 'throwing', 'existed', 'wagon', 'barbie',
                'knock', 'potatoes', 'thorough', 'peers', 'roland', 'optimum', 'quilt', 'creature', 'mounts',
                'syracuse', 'refresh', 'webcast', 'michel', 'subtle', 'notre', 'maldives', 'stripes', 'firmware',
                'shepherd', 'canberra', 'cradle', 'mambo', 'flour', 'sympathy', 'choir', 'avoiding', 'blond', 'expects',
                'jumping', 'fabrics', 'polymer', 'hygiene', 'poultry', 'virtue', 'burst', 'surgeons', 'bouquet',
                'promotes', 'mandate', 'wiley', 'corpus', 'johnston', 'fibre', 'shades', 'indices', 'adware', 'zoloft',
                'prisoner', 'daisy', 'halifax', 'ultram', 'cursor', 'earliest', 'donated', 'stuffed', 'insects',
                'crude', 'morrison', 'maiden', 'examines', 'viking', 'myrtle', 'bored', 'cleanup', 'bother', 'budapest',
                'knitting', 'attacked', 'bhutan', 'mating', 'compute', 'redhead', 'arrives', 'tractor', 'allah',
                'unwrap', 'fares', 'resist', 'hoped', 'safer', 'wagner', 'touched', 'cologne', 'wishing', 'ranger',
                'smallest', 'newman', 'marsh', 'ricky', 'scared', 'theta', 'monsters', 'asylum', 'lightbox', 'robbie',
                'stake', 'cocktail', 'outlets', 'arbor', 'poison']

ENGLISH_WORDS = FREQ_words_one_char + FREQ_words_two_char + FREQ_words_three_char + FREQ_words_four_char + COMMON_WORDS
##################################################################################

cyphertext = clean_text(get_text_from_file(get_first_commandline_argument()))
KEY = {}
display_fancy('INPUT', cyphertext)

# try to find word separator
sep = get_top_chars(cyphertext, 1)[0]
KEY[sep] = ' '
cyphertext = apply_substitution_dictionary(cyphertext, KEY)
# print(KEY)
display_fancy('SPACE DETECTION', cyphertext)

# find one char words
for doc, eng in zip(get_top_short_words(cyphertext, 1), FREQ_words_one_char):
    if doc not in KEY.keys() and eng not in KEY.values():
        KEY[doc] = eng

# find most common characters
for doc, eng in zip(get_top_chars(cyphertext, n=6)[1:], FREQ_char_unigrams):
    if doc not in KEY.keys() and eng not in KEY.values():
        KEY[doc] = eng

# take the top 2 (seems good) most frequent three-char words
for doc, eng in zip(get_top_short_words(cyphertext, length=3, n=2), FREQ_words_three_char):
    if word_pattern(doc) == word_pattern(eng):
        for x, Y in zip(doc, eng):
            if x not in KEY.keys() and Y not in KEY.values():
                KEY[x] = Y

print(KEY)
display_fancy('FREQUENCY STAGE 1', apply_substitution_dictionary(cyphertext, KEY))

###############################

# key_candidates = defaultdict(list)
#
# # add possible double char permutations
# double_chars = []
# for c in get_top_double_chars(cyphertext, n=10):
#     c = c[:-1]  # get one char
#     if c not in KEY.keys():
#         double_chars.append(c)
# for i in itertools.permutations(double_chars):
#     for doc, eng in zip(i, [x[:-1] for x in FREQ_char_doubles]):
#         # print(doc, eng)
#         if doc not in KEY.keys() and eng not in KEY.values():
#             key_candidates[doc].append(eng)
#
# # add possible short word char permutations
# for i in itertools.permutations(get_top_short_words(cyphertext, length=2, n=4)):
#     for doc, eng in zip(i, FREQ_words_two_char):
#         for x, Y in zip(doc, eng):
#             if x not in KEY.keys() and Y not in KEY.values():
#                 key_candidates[x].append(Y)
# for i in itertools.permutations(get_top_short_words(cyphertext, length=3, n=6)[2:]):
#     # first 2 three char words have already been processed
#     for doc, eng in zip(i, FREQ_words_three_char):
#         if word_pattern(doc) == word_pattern(eng):
#             for x, Y in zip(doc, eng):
#                 if x not in KEY.keys() and Y not in KEY.values():
#                     key_candidates[x].append(Y)
# for i in itertools.permutations(get_top_short_words(cyphertext, length=4, n=4)):
#     for doc, eng in zip(i, FREQ_words_four_char):
#         if word_pattern(doc) == word_pattern(eng):
#             for x, Y in zip(doc, eng):
#                 if x not in KEY.keys() and Y not in KEY.values():
#                     key_candidates[x].append(Y)
#
# # GENERATE ALL KEY CANDIDATE PERMUTATIONS #
#
# for k, v in key_candidates.items():
#     print(k, Counter(v))

#####################################################
print('RAGE-QUIT-BRUTE-FORCING THE SHIT OUT OF THIS...')

best_score = score_text(cyphertext)
key_store = []
LEARNED_PART = {}
while True:
    leftover_doc_chars = list(set(VALID_CHARS).difference(set(KEY.keys())).difference(LEARNED_PART.keys()))
    leftover_doc_chars.remove(' ')
    leftover_eng_chars = list(set(VALID_CHARS).difference(set(KEY.items())).difference(LEARNED_PART.items()))
    leftover_eng_chars.remove(' ')
    # doc chars complexity must be less or equal than eng chars (due to import restrictions)
    map_range = list(range(0, len(leftover_eng_chars)))
    random.shuffle(map_range)
    random_part = {}
    for doc_n, eng_n in zip(range(0, len(leftover_doc_chars)), map_range):
        random_part[leftover_doc_chars[doc_n]] = leftover_eng_chars[eng_n]
    random_key = KEY.copy()
    random_key.update(random_part)
    random_key.update(LEARNED_PART)
    text = apply_substitution_dictionary(cyphertext, random_key)
    score = score_text(text)
    if score > best_score:
        best_score = score
        display_fancy('BRUTE FORCE SCORE {}'.format(score), text)
        key_store.append(random_key)
        LEARNED_PART = most_common_dict(key_store)
        print('LEARNED PART')
        print(LEARNED_PART)