
words: list[str] = []
with open('words', 'r') as file:
    for line in file:
        words.append(line.strip())

Color = int
Coloring = tuple[Color, Color, Color, Color, Color]
GREY:   Color = -1
YELLOW: Color = 0
GREEN:  Color = 1

class Feedback:
    def __init__(self, guess: str, colors: Coloring):
        self.guess = guess
        self.coloring = colors

    def isWin(self) -> bool:
        return self.coloring == (GREEN, GREEN, GREEN, GREEN, GREEN)

def score_guess(guess: str, answer: str) -> Feedback:
    guess = guess.lower()
    answer = answer.lower()
    ret = [GREY, GREY, GREY, GREY, GREY]

    # first we add greens (to avoid weird edge cases)
    yellow_count: dict[str, int] = {}
    for i in range(5):
        if guess[i] == answer[i]: 
            ret[i] = GREEN
            continue
        if answer[i] in yellow_count: yellow_count[answer[i]] += 1
        else: yellow_count[answer[i]] = 1

    for i in range(5):
        if ret[i] == GREEN: continue
        if (guess[i] in yellow_count) and (yellow_count[guess[i]] > 0):
            ret[i] = YELLOW
            yellow_count[guess[i]] -= 1

    # I know this is ugly, I don't care
    return Feedback(guess, (ret[0], ret[1], ret[2], ret[3], ret[4]))


# some tests for score_guess
assert score_guess("crane", "crane").coloring == (GREEN, GREEN, GREEN, GREEN, GREEN)
assert score_guess("Crane", "crAne").coloring == (GREEN, GREEN, GREEN, GREEN, GREEN)
assert score_guess("misty", "crane").coloring == (GREY, GREY, GREY, GREY, GREY)
assert score_guess("cloud", "crane").coloring == (GREEN, GREY, GREY, GREY, GREY)
assert score_guess("trace", "crane").coloring == (GREY, GREEN, GREEN, YELLOW, GREEN)
assert score_guess("beefy", "crane").coloring == (GREY, YELLOW, GREY, GREY, GREY)
assert score_guess("roast", "rotor").coloring == (GREEN, GREEN, GREY, GREY, YELLOW)
assert score_guess("puppy", "apple").coloring == (YELLOW, GREY, GREEN, GREY, GREY)
assert score_guess("canal", "banal").coloring == (GREY, GREEN, GREEN, GREEN, GREEN)


def is_possible_given_info(word: str, result: Feedback) -> bool:
    return score_guess(result.guess, word).coloring == result.coloring

def cull_possibilities(result: Feedback, words: list[str]) -> list[str]:
    return list(filter(lambda w: is_possible_given_info(w, result), words))