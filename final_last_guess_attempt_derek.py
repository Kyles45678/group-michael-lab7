import string

guesses = []
results = []
total_letters = []
letter_counts = {}

# Parse the guesses and results
def parse_guesses():
    for guess, result in zip(guesses, results):
        temp_counts = {}
        # Iterate through each letter of the results
        for i, result_letter in enumerate(result):
            total_letters.append(guess[i])
            # If the letter is G, then set the output index for that letter
            # And add 1 to the count
            if result_letter == "G":
                output[i] = guess[i]
                add_count_to_dict(temp_counts, guess[i])
            # If the letter is Y, then add one to that letter's count
            elif result_letter == "Y":
                add_count_to_dict(temp_counts, guess[i])

        # Get the maximum number of letters from each of the guesses.
        for key, value in temp_counts.items():
            if letter_counts.get(key) is None:
                letter_counts[key] = 0
            letter_counts[key] = max(letter_counts[key], value)

# Method for adding a count to the dict, if in the dict, just add one.
# If not in the dict, instantiate it, then add it.
def add_count_to_dict(dictionary, key):
    if dictionary.get(key) is None:
        dictionary[key] = 0
    dictionary[key] += 1

# Check how many letters of a certain type are in the output, then subtract it from the total letter counts
def finalize_counts():
    for key in letter_counts:
        if key in output:
            letter_counts[key] -= output.count(key)

# Get which locations in the output don't have letters
def get_possible_letter_locations():
    indices = []
    for i, letter in enumerate(output):
        if letter is None:
            indices.append(i)
    return indices

# Find a valid place for the yellows and add extra letters at the end when all yellows are used if needed
def place_yellows_and_extras():
    # Get possible new letter indices
    indices = get_possible_letter_locations()
    # Iterate through each letter in letter counts
    for letter in letter_counts:
        # While the letter count is greator than zero
        while (letter_counts[letter] > 0):
            # iterate through each of the possible letter locations
            for index in indices:
                # If that index is not None, continue because letter is found
                if output[index] is not None:
                    continue
                # If the position is valid (Y is allowed to go there)
                is_valid = check_position(letter, index)
                if is_valid:
                    # Set that output to the letter and subtract one from the count
                    output[index] = letter
                    letter_counts[letter] -= 1
                    # Move onto the next letter
                    break

    # Iterate through each possible letter location index
    for index in indices:
        # If the letter is not found
        if output[index] is None:
            # Iterate through all lowercase letters
            for letter in string.ascii_lowercase:
                # If that letter is not found in the total letters
                if letter not in total_letters:
                    # Set the index in output to that new letter
                    output[index] = letter
                    total_letters.append(letter)
                    # move onto the next index
                    break
    # Print the output
    print(''.join(output))

# Checks if a yellow letter can go in that index 
# (If any of the guesses have that letter at the position, it cannot go there)
def check_position(lookup_letter, index):
    for guess in guesses:
        letter = guess[index]
        if letter == lookup_letter:
            return False
    return True


# Read first line
number_of_guesses, length_of_words = input().split(" ")
number_of_guesses = int(number_of_guesses) # Parse number of guesses from line
length_of_words = int(length_of_words) # Parse length of words from line
# Read N - 1 lines for all guesses
for i in range(number_of_guesses - 1):
    # Read the current guess
    word, result = input().split(" ")
    guesses.append(word)
    results.append(result)

# Instantiate output
output = [None] * length_of_words

parse_guesses()
finalize_counts()
place_yellows_and_extras()
