words = []

for word in open('textfiles/short_words.txt'):
    word = word.rstrip()
    if len(word) >= 3:
        words.append(word.rstrip())

for word in open('textfiles/medium_words.txt'):
    words.append(word.rstrip())


print(words)