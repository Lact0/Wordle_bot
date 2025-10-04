words: set[str] = set()
with open("all_words.txt", "r") as rfile:
    for line in rfile:
        word = line.strip()

        if len(word) != 5: continue
        has_grammar: bool = False
        for letter in word:
            if not letter.isalpha():
                has_grammar = True
                break
        if has_grammar: continue
        words.add(word.lower())


with open("five_letter_words.txt", "w") as wfile:
    for word in words:
        wfile.write(word + '\n')