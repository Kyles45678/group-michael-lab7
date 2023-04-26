import string
import json

class InputGuess:
    def __init__(self, word, result):
        self.word = word
        self.result = result
    
    def __str__(self):
        return "Word: {}, Result: {}".format(self.word, self.result)

    
class Guesser:
    def __init__(self, length_of_words):
        self.length_of_words = length_of_words
        self.output = [None] * length_of_words
        self.yellow = []
        self.black = []
        self.counts = {letter: 0 for letter in string.ascii_lowercase}
        self.total_letters = []

    def compile_guess(self, guess):
        temp_counts = {letter: 0 for letter in string.ascii_lowercase}
        for i, (letter, result) in enumerate(zip(guess.word, guess.result)):
            self.total_letters.append(letter)
            if result == 'G':
                self.output[i] = letter
            elif result == "Y":
                self.yellow.append((letter, i))
            elif result == 'B':
                self.black.append((letter, i))

            if letter in guess.word[:i] + guess.word[i + 1:]:
                if result in ['G', 'Y']:
                    temp_counts[letter] += 1
                    
            elif result in ['G', 'Y']:
                temp_counts[letter] += 1

        for key, value in temp_counts.items():
            self.counts[key] = max(self.counts[key], value)

    def compile_results(self):
        indices = [None] * self.length_of_words
        for i, element in enumerate(self.output):
            if not element:
                indices[i] = i
        
        for key in self.counts:
            if key in self.output:
                self.counts[key] -= self.output.count(key)
        invalid_pos = {letter: [] for letter in string.ascii_lowercase}
        for letter, index in self.yellow:
            if self.counts[letter] == 0:
                continue
            invalid_pos[letter].append(index)
        
        for i, found in enumerate(self.output):
            if found:
                continue
            for key, value in invalid_pos.items():
                if not value:
                    continue
                if i in value:
                    continue
                if self.counts[key] == 0:
                    continue
                self.output[i] = key
                self.counts[key] -= 1
                break

            if not self.output[i]:
                for letter in string.ascii_lowercase:
                    if letter not in self.total_letters:
                        self.output[i] = letter
                        self.total_letters.append(letter)
                        break

        print(''.join(letter for letter in self.output))
"""
4 5
reply YYGBB
refer BBBGG
puppy YYGBB

2 12
aabbccddeeff GGGYGBYYYBBB


"""


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
    
    guesser.compile_results()

main()
