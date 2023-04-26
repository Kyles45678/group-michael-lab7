class InputGuess:
    def __init__(self, word, result):
        self.word = word
        self.result = result
    
    def __str__(self):
        return "Word: {}, Result: {}".format(self.word, self.result)

    
class Guesser:
    def __init__(self, length_of_words):
        self.length_of_words = length_of_words
        self.letter_counts = {}
        self.output = ['_'] * length_of_words


    def compile_guess(self, guess):
        for i in range(self.length_of_words):
            current_letter = guess.word[i]
            current_result = guess.result[i]
            if current_letter not in self.letter_counts:
                self.letter_counts[current_letter] = 0

            if current_result == 'G':
                self.output[i] = current_letter
                
            elif current_result == 'Y':
                self.letter_counts[current_letter] += 1
                pass
            elif current_result == 'B':
                pass

"""
4 5
reply YYGBB
refer BBBGG
puppy YYGBB

"""

import json

def main():
    guesses = []
    number_of_guesses, length_of_words = input().split(" ")
    number_of_guesses = int(number_of_guesses)
    length_of_words = int(length_of_words)
    guesser = Guesser(length_of_words)
    for i in range(number_of_guesses - 1):
        word, result = input().split(" ")
        new_guess = InputGuess(word, result)
        guesses.append(new_guess)
        guesser.compile_guess(new_guess)
    
    print(guesser.output)
    print(json.dumps(guesser.letter_counts))
    # print(guesser.letters_needed)

main()
