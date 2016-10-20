from collections import defaultdict
import re

charCounter = defaultdict(int)
wordCounter = defaultdict(int)
char_re = re.compile(r'[a-z]')

# for line in open('textfiles/alice.txt'):
for line in open('../texts/crypto.txt'):
    line = line.lower()
    for word in line.split():
        word = ''.join(char_re.findall(word))
        wordCounter[word] += 1
    for char in line.lower():
        charCounter[char] += 1

print('CHARS')
print(sorted(charCounter.items(), key=lambda x: x[1], reverse=True))
print('WORDS')
print(sorted(wordCounter.items(), key=lambda x: x[1], reverse=True))