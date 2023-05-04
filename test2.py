from collections import defaultdict

# read input
G, L = map(int, input().split())
guesses = [input().split() for _ in range(G-1)]

# create a list of possible words based on the first guess
possible_words = ["".join(sorted(guesses[0][0]))]
for i in range(1, L):
    possible_words = [word + letter for letter in guesses[0][0] for word in possible_words if letter not in word]

# iterate through each subsequent guess and eliminate words that do not match
for guess, feedback in guesses[1:]:
    # group the possible words by the feedback for the current guess
    groups = defaultdict(list)
    for word in possible_words:
        key = tuple(get_feedback(word, guess))
        groups[key].append(word)
    # eliminate words that do not match the feedback for the current guess
    possible_words = []
    for key in groups:
        if key == tuple(feedback):
            possible_words.extend(groups[key])

# choose any word from the remaining possible words as the final guess
print(possible_words[0])
