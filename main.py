from wordle import *
from bots import *
from cache.crane import *

# would be cool to simplify to not remembering guess history, but just having a 
# single representation of all knowledge gained. 

def calc_openings():
    with open("cache/temp_opening_ev.txt", "w") as file:
        bot = PartitionedEVBot()
        # bot.verbose = True

        file.write("opening_evs: dict[str, float] = {\n")
        best_score: float = 0
        best_guess = nyt_words[0]

        i = 0
        print("CALCULATING BEST OPENER...")
        for guess in nyt_words:
            score = bot.guess_ev(guess)
            if score > best_score:
                best_score = score
                best_guess = guess
            file.write(f"   '{guess}': {score},\n")

            i += 1
            if i % 5 == 0: 
                file.flush()
                print(f'\r{i}/{len(nyt_words)} ({int(i / len(nyt_words) * 1000)/10}%)', end='')
        
        print(f"BEST OPENER: {best_guess} WITH SCORE {best_score}")

        file.write('}')

def calc_seconds(opening: str, hard: bool = False) -> dict[Coloring, tuple[str, float]]:
    bot = PartitionedEVBot()
    bot.verbose = True
    bot.hard = hard
    
    response_counts:  dict[Coloring, int] = {}
    response_guesses: dict[Coloring, str] = {}
    response_scores:  dict[Coloring, float] = {}
    i = 0
    for possible_answer in nyt_words:

        print(i)
        i += 1

        bot.reset()
        result = score_guess(opening, possible_answer)

        # we've already handled this response
        if result.coloring in response_counts:
            response_counts[result.coloring] += 1
            continue

        bot.read_result(result)
       
        response_counts[result.coloring] = 1
        best_guess = bot.guess()
        response_guesses[result.coloring] = best_guess
        response_scores[result.coloring] = bot.guess_ev(best_guess)

    # package guesses & counts into one 
    ret: dict[Coloring, tuple[str, float]] = {}
    for response in response_counts:
        ret[response] = (response_guesses[response], response_scores[response])
    return ret



# second_response = calc_seconds("lares")
# print(second_response)
# with open("cache/lares.py", "a") as file:
#     file.write("\nlares_response = {\n")
#     for result in second_response:
#         guess, score = second_response[result]
#         file.write(f"   {result}: ('{guess}', {score}),\n")
#     file.write("}")
print("SCORE:", test_bot(LaresOpParEVBot()))