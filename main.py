from wordle import *
from random import randint

# would be cool to simplify to not remembering guess history, but just having a 
# single representation of all knowledge gained. 

nWins = 0
nTests = len(words)
for j in range(nTests):

    answer = words[j]#words[randint(0, len(words) - 1)]
    temp_words = words
    for i in range(6):
        guess = temp_words[randint(0, len(temp_words) - 1)]
        result: Feedback = score_guess(guess, answer)
        # print(f'GUESS {i+1}: {guess}, FEEDBACK: {result.coloring}')

        if result.isWin(): 
            # print("WON!!!")
            nWins += 1
            break

        temp_words = cull_possibilities(result, temp_words)
    print(f"{j}/{nTests}, Answer was {answer}")

print(f"WINRATE: {nWins / nTests}")