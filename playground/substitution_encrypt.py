import string, random

VALID_CHARS = list(string.ascii_lowercase + ' .,-!?"')
RANDOM_CHARS = list(VALID_CHARS)
random.shuffle(RANDOM_CHARS)
KEY = {c: k for c, k in zip(VALID_CHARS, RANDOM_CHARS)}

with open('../texts/crypto_long.txt',  mode='w', encoding='utf8', newline='') as outfile:
    for line in open('../texts/plain_long.txt'):
        line = line.lower()
        for char in line:
            if char in VALID_CHARS:
                outfile.write(KEY[char])
        outfile.write('\n')