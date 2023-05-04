# Kyle Senebouttarath

import random

alphabet = set(['a', 'b', 'c', 'd', 'e', 'f', 'g',
                'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p',
                'q', 'r', 's', 't', 'u', 'v',
                'w', 'x', 'y', 'z'])


# reads through the dictionary of impossible letter positions and
#   returns the letters that are impossible at a given position index
def get_impossible_letters_at_pos(pos_index, impossible_letter_positions):
    impossible_letters = []
    for l in impossible_letter_positions:
        if pos_index in impossible_letter_positions[l]:
            impossible_letters.append(l)
    return impossible_letters


# fills the empty cells in our final known characters array with random, possibles
def fill_empties_with_randoms(knowns, impossible_letters, impossible_letter_positions):
    # ignore letters that we know NEVER appear
    possible_letters = alphabet.copy()
    for l in impossible_letters:
        if l in possible_letters:
            possible_letters.remove(l)

    # loop through known letters, if there's an empty space, place a possible letter at that position
    for i in range(len(knowns)):
        if knowns[i] == '':
            imps = get_impossible_letters_at_pos(i, impossible_letter_positions)
            new_posses = possible_letters.copy()
            for il in imps:
                if il in new_posses:
                    new_posses.remove(il)
            knowns[i] = random.choice(list(new_posses))


# loop through our remaining letters (per letter amount too), place them in their
# first valid spots
def place_remaining_occurs(knowns, poss, occurs):
    to_remove = []

    for letter in occurs:
        while occurs[letter] > 0:
            first_pos = next(iter(poss[letter]))
            knowns[first_pos] = letter
            occurs[letter] -= 1;
            for l in poss:
                if first_pos in poss[l]:
                    poss[l].remove(first_pos)
        to_remove.append(letter)

    for l in to_remove:
        if l in poss:
            poss.pop(l)
        if l in occurs:
            occurs.pop(l)


# Uses set intersection to get a set of positions shared across all yellow letters.
# then, for each yellow, compute the difference of this set from our shared common set to get
# unique positions
def get_unique_possibilities(possibles, word_length):
    most_shared_set = set(range(word_length))
    for c in possibles:
        most_shared_set = most_shared_set.intersection(possibles[c])
    c = possibles.copy()
    for k in c:
        c[k] = c[k].difference(most_shared_set)
    return c


# determines if a provided dictionary of differentiating letter positions has moves to place
# it has a move to place if it has 1 unique position
def has_moves(diffed_possibles):
    for letter in diffed_possibles:
        if len(diffed_possibles[letter]) == 1:
            return True
    return False


# place the yellow letters that have a single unique position on the last guess
# update the final answer, the number of occurrences per evaluated letter, and possible placements
# of other letters
def place_single_differed_possibiles(knowns, poss, occurs, diffed_possibles):
    keys_to_remove = []
    poses_to_remove = []

    for letter in diffed_possibles:
        if len(diffed_possibles[letter]) == 1:
            index_to_place = diffed_possibles[letter].pop()
            poss[letter].pop()
            poses_to_remove.append(index_to_place)
            if letter in occurs:
                occurs[letter] -= 1
            knowns[index_to_place] = letter
            if occurs[letter] <= 0:
                keys_to_remove.append(letter)

    for key in keys_to_remove:
        if key in occurs and occurs[key] <= 0:
            occurs.pop(key)
        if key in poss:
            poss.pop(key)
        if key in diffed_possibles:
            diffed_possibles.pop(key)

    for pos in poses_to_remove:
        for letter in poss:
            if pos in poss[letter]:
                poss[letter].remove(pos)
        for letter in diffed_possibles:
            if pos in diffed_possibles[letter]:
                diffed_possibles[letter].remove(pos)

    diffed_letters_to_remove = []
    for letter in poss:
        if len(diffed_possibles[letter]) <= 0:
            diffed_letters_to_remove.append(letter)

    for letter in diffed_letters_to_remove:
        if letter in diffed_possibles:
            diffed_possibles.pop(letter)


# loop through the possible letter positions. if there is only one position, place it
# and then update the known list and occurrences
def place_single_possibles(knowns, possibles, occurs):
    keys_to_remove = []

    for letter in possibles:
        if len(possibles[letter]) == 1:
            index_to_place = possibles[letter].pop()
            keys_to_remove.append(letter)
            if letter in occurs:
                occurs[letter] -= 1
            knowns[index_to_place] = letter

    for k in occurs:
        if occurs[k] <= 0:
            keys_to_remove.append(k)

    for key in keys_to_remove:
        if key in occurs and occurs[key] <= 0:
            occurs.pop(key)
        if key in possibles:
            possibles.pop(key)


# loops through the known letters, and removes their counts from the occurrences
def filter_out_occurences_with_known(occurs, knowns):
    to_remove = []
    for c in knowns:
        if c in occurs:
            occurs[c] -= 1;
            if occurs[c] <= 0:
                to_remove.append(c)
    for c in to_remove:
        occurs.pop(c)


# remove the known letter positions from the list of possible letter positions per letter
def filter_out_possibilities(possibles, knowns, occurs):
    for i in range(len(knowns)):
        if knowns[i] != "":  # this index is used, remove index from all possibles
            for l in possibles:
                if i in possibles[l]:
                    possibles[l].remove(i)
    to_pop_from_occurs = []
    for let in occurs:  # if our occurrences dropped to zero for a letter, remove it
        if occurs[let] <= 0 and let in possibles:
            possibles.pop(let)
            to_pop_from_occurs.append(let)
    for let in to_pop_from_occurs:
        occurs.pop(let)


# filter out the possible placements for letters based on what we deemed as impossible placement locations
def filter_out_possibilities_with_impossible_positions(occurs, possibles, impossible_poses):
    for c in occurs:
        if occurs[c] > 0:
            if c in impossible_poses:
                for i in impossible_poses[c]:
                    if c in possibles and i in possibles[c]:
                        possibles[c].remove(i)


# adds a given range of numbers to a set, but ignore a list of given numbers
def add_nums_to_set(s, end_range, ignores):
    for i in range(end_range):
        if i not in ignores:
            s.add(i)


# main
def main():
    # first line input
    (num_guesses, word_length) = map(int, input().split(" "))

    # memory allocations
    known_characters = [""] * word_length
    guesses_list = []
    possibilities = {}
    occurs = {}
    pure_impossibles = set()
    impossible_positions = {}

    # gather remaining guesses, store them in allocations
    for g in range(num_guesses - 1):
        (word, correctness) = input().split(" ")
        guesses_list.append((word, correctness))
        cur_occurs = {}
        for i in range(word_length):
            char = word[i]
            if correctness[i] == "G":           # if green slot, we know this character
                known_characters[i] = char
            if correctness[i] == "Y":           # if yellow, track that it cannot be in the current position and all
                if char not in possibilities:    # other positions as possible
                    possibilities[char] = set()
                if char not in impossible_positions:
                    impossible_positions[char] = set()
                impossible_positions[char].add(i)
                add_nums_to_set(possibilities[char], word_length, list(impossible_positions[char]))
            if correctness[i] == "B":           # if black, track tile as impossible
                if char not in cur_occurs:
                    pure_impossibles.add(char)
                if char not in impossible_positions:
                    impossible_positions[char] = set()
                impossible_positions[char].add(i)
            if correctness[i] == "G" or correctness[i] == "Y":  # track letter tally (occurrences)
                if char not in cur_occurs:
                    cur_occurs[char] = 0;
                cur_occurs[char] += 1
                if char in pure_impossibles:
                    pure_impossibles.remove(char)
        for let in cur_occurs:
            if let not in occurs or occurs[let] < cur_occurs[let]:
                occurs[let] = cur_occurs[let]

    # filter out letter positions for the
    filter_out_occurences_with_known(occurs, known_characters)
    filter_out_possibilities(possibilities, known_characters, occurs)
    filter_out_possibilities_with_impossible_positions(occurs, possibilities, impossible_positions)

    # place the yellow characters that have 1 possible placement
    place_single_possibles(known_characters, possibilities, occurs)

    # if we solved our word by then, print it
    cur_word = "".join(known_characters)
    if len(cur_word) == word_length:
        print(cur_word)
        return

    # get unique, unshared possible positions, then place single possible locations
    differenced_possibilities = get_unique_possibilities(possibilities, word_length)
    while has_moves(differenced_possibilities):
        place_single_differed_possibiles(known_characters, possibilities, occurs, differenced_possibilities)

    # if we solved our word by then, print it
    cur_word = "".join(known_characters)
    if len(cur_word) == word_length:
        print(cur_word)
        return

    # place any remaining letters that we know occur in the string in their first valid positions
    place_remaining_occurs(known_characters, possibilities, occurs)

    # if we solved our word by then, print it
    cur_word = "".join(known_characters)
    if len(cur_word) == word_length:
        print(cur_word)
        return

    # place random spaces
    fill_empties_with_randoms(known_characters, pure_impossibles, impossible_positions)

    # we solved our word by then, print it
    cur_word = "".join(known_characters)
    print(cur_word)


main()
