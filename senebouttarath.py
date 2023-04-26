alphabet = ['a', 'b', 'c', 'd', 'e', 'f', 'g',
            'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p',
            'q', 'r', 's', 't', 'u', 'v',
            'w', 'x', 'y', 'z']


def filter_out_occurences_with_known(occurs, knowns):
    for c in knowns:
        if c in occurs:
            occurs[c] -= 1;


def filter_out_possibilities(possibles, knowns, occurs):
    for i in range(len(knowns)):
        if knowns[i] != "":  # this index is used, remove index from all possibles
            for l in possibles:
                if i in possibles[l]:
                    possibles[l].remove(i)

    to_pop_from_occurs = []
    for let in occurs:
        if occurs[let] <= 0 and let in possibles:
            possibles.pop(let)
            to_pop_from_occurs.append(let)

    for let in to_pop_from_occurs:
        occurs.pop(let)


def add_nums_to_set(s, end_range, ignores):
    for i in range(end_range):
        if i not in ignores:
            s.add(i)


def main():
    (num_guesses, word_length) = map(int, input().split(" "))

    known_characters = [""] * word_length
    guesses_list = []

    possibilities = {}
    occurs = {}

    for g in range(num_guesses - 1):
        (word, correctness) = input().split(" ")
        guesses_list.append((word, correctness))

        cur_occurs = {}
        for i in range(word_length):
            char = word[i]

            if correctness[i] == "G":
                known_characters[i] = char

            if correctness[i] == "Y":
                if char not in possibilities:
                    possibilities[char] = set()
                add_nums_to_set(possibilities[char], word_length, [i])

            if correctness[i] == "G" or correctness[i] == "Y":
                if char not in cur_occurs:
                    cur_occurs[char] = 0;
                cur_occurs[char] += 1

        for let in cur_occurs:
            if let not in occurs or occurs[let] < cur_occurs[let]:
                occurs[let] = cur_occurs[let]

    print(known_characters)
    print("occurences:", occurs)
    print(possibilities)

    filter_out_occurences_with_known(occurs, known_characters)
    filter_out_possibilities(possibilities, known_characters, occurs)

    print("-----------------------------------------------------------------")
    print("occurences:", occurs)
    print(possibilities)


main()
