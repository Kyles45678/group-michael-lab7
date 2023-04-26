class InputGuess:
    def __init__(self, word, result):
        self.word = word
        self.result = result
    
    def __str__(self):
        return "Word: {}, Result: {}".format(self.word, self.result)

    
class Guesser:
    def __init__(self, length_of_words):
        self.length_of_words = length_of_words
        self.counts = []
        self.output = ['_'] * length_of_words


    def compile_guess(self, guess):
        current_counts = {}
        # for i in range(self.length_of_words):
        for i, (letter, result) in enumerate(zip(guess.word, guess.result)):
            if letter not in current_counts:
                    current_counts[letter] = 0

            if letter in guess.word[:i] + guess.word[i + 1:]:
                if result in ['G', 'Y']:
                    current_counts[letter] += 1
        
            elif result in ['G', 'Y']:
                current_counts[letter] += 1

            if result == 'G':
                self.output[i] = letter
        self.counts.append(current_counts)
        # print(json.dumps(current_counts, indent=4))
                # print(letter, result)
        # for i in range(self.length_of_words):
        #     current_letter = guess.word[i]
        #     current_result = guess.result[i]
        #     if current_letter not in current_counts:
        #         current_counts[current_letter] = 0
        #     if current_result == 'G':
        #         self.output[i] = current_letter
                
        #         self.greens[current_letter].append(i)

        #     elif current_result == 'Y':
        #         self.yellows[current_letter].append(i)
        #         pass
        #     elif current_result == 'B':
        #         pass

    def combine(self):
        out = {}
        for count_dict in self.counts:
            for key, value in count_dict.items():
                if key not in out:
                    out[key] = 0
                out[key] = max(value, out[key])

        unadded_letters = []
        for key, value in out.items():
            if key in self.output:
                out[key] -= 1
        
        print(out)
        


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
    guesser.combine()
    # print(json.dumps(guesser.greens))
    # print(json.dumps(guesser.yellows))
    # print(guesser.letters_needed)

main()
