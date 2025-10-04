from wordle import *
from random import randint

class WordleBot:

    guesses: list[str] = []
    results: list[Feedback] = []
    words: list[str] = []
    possibles: list[str] = []

    def __init__(self, words: list[str] = nyt_words):
        self.words = words
        self.possibles = words

    def guess(self) -> str:
        self.guesses.append("")
        return ""
    
    def read_result(self, result: Feedback):
        # print("BEFORE CULLING: ", result.guess, result.coloring, self.possibles)
        self.results.append(result)
        self.possibles = cull_possibilities(result, self.possibles)
        # print("AFTER CULLING:")
        # print(result.guess, result.coloring, self.possibles)

    def reset(self):
        self.possibles = self.words
        self.guesses = []
        self.results = []



def test_bot(bot: WordleBot) -> float:
    nWins = 0
    for i in range(len(nyt_words)):
        answer = nyt_words[i]
        bot.reset()
        # if i % 100 == 0: 
        print(f"\r{i}/{len(nyt_words)}", end="")

        for g in range(6):
            guess = bot.guess()
            result: Feedback = score_guess(guess, answer)
            bot.read_result(result)

            if result.isWin(): 
                nWins += 1
                break
            elif g == 5:
                print(f"\nFAILED ON '{answer}'")
    print()
    return nWins / len(nyt_words)

def play_game(bot: WordleBot, ans: str, verbose: bool = False):
    for i in range(6):
        guess = bot.guess()
        res = score_guess(guess, ans)
        bot.read_result(res)
        if verbose: print(f"BOT GUESSED: {guess}, RESULT: {res.coloring}")
        if res.isWin():
            if verbose: print(f"BOT WON AFTER GUESS {i+1}!")
            break
    




class RandomBot(WordleBot):
    def guess(self) -> str:
        self.guesses.append(self.possibles[randint(0, len(self.possibles) - 1)])
        return self.guesses[-1]

class OpRandomBot(RandomBot):
    def guess(self) -> str:
        if len(self.guesses) == 0: 
            self.guesses.append("crane")
            return "crane"
        if len(self.guesses) == 1: 
            self.guesses.append(second_guess[self.results[-1].coloring][0])
            return self.guesses[-1]
        super().guess()
        return self.guesses[-1]

class HardEVBot(WordleBot):

    verbose: bool = False

    def guess(self) -> str:
        best_score: float = 0
        best_guess = self.possibles[0]
        for guess in self.possibles:
            score = self.guess_ev(guess)
            if score > best_score:
                best_score = score
                best_guess = guess
        self.guesses.append(best_guess)
        return best_guess

    def guess_ev(self, guess: str) -> float:
        total = 0
        i = 0
        for ans in self.possibles:
            if self.verbose and i % 100 == 0:
                l = len(self.possibles)
                percent = int(i / l * 100)
                cur = int((total) / (1 if i == 0 else i))
                print(f"\rEval '{guess}': {i}/{l} ({percent}%) (score: {cur})", end='')
            nLeft = len(cull_possibilities(score_guess(guess, ans), self.possibles))
            total += len(self.possibles) - nLeft
            i += 1
        if self.verbose: print()
        return total / len(self.possibles)


from cache.crane import second_guess
class CraneEVBot(HardEVBot):
    def guess(self) -> str:
        if len(self.guesses) == 0: 
            self.guesses.append("crane")
            return "crane"
        if len(self.guesses) == 1: 
            self.guesses.append(second_guess[self.results[-1].coloring][0])
            return self.guesses[-1]
        super().guess()
        return self.guesses[-1]



class PartitionedEVBot(WordleBot):

    verbose: bool = False
    hard: bool = False

    def guess(self) -> str:
        best_score: float = 0
        best_guess = self.possibles[0]

        i = 0
        prefix = ""
        guess_pool = self.possibles if self.hard else self.words
        for guess in guess_pool:#self.possibles:
            if self.verbose: 
                prefix = f"Eval ({i}/{len(guess_pool)}): "
            i += 1

            score = self.guess_ev(guess, prefix)
            if score > best_score:
                best_score = score
                best_guess = guess

        self.guesses.append(best_guess)
        if self.verbose: print()
        return best_guess

    def guess_ev(self, guess: str, prefix: str = "") -> float:
        total = 0
        i = 0
        memo: dict[Coloring, int] = {}
        for ans in self.possibles:
            if self.verbose and i % 100 == 0:
                l = len(self.possibles)
                percent = int(i / l * 100)
                cur = int((total) / (1 if i == 0 else i))
                print(f"\r{prefix}Eval '{guess}': {i}/{l} ({percent}%) (score: {cur})", end='')
            i += 1
            
            result = score_guess(guess, ans)
            if result.coloring in memo:
                total += memo[result.coloring]
                continue

            nLeft = len(cull_possibilities(result, self.possibles))
            total += len(self.possibles) - nLeft
            memo[result.coloring] = len(self.possibles) - nLeft

        if self.verbose and prefix == "": print()
        return total / len(self.possibles)

from cache.lares import hard_lares_response, lares_response
class LaresOpParEVBot(PartitionedEVBot):
    def guess(self) -> str:
        if len(self.guesses) == 0: 
            self.guesses.append("lares")
            return "lares"
        if len(self.guesses) == 1: 
            coloring = self.results[-1].coloring
            if self.hard: self.guesses.append(hard_lares_response[coloring][0])
            else:         self.guesses.append(lares_response[coloring][0])
            return self.guesses[-1]
        super().guess()
        return self.guesses[-1]


