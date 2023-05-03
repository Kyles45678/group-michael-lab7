def main():
    n, l = map(int, input().split())
    guesses = [input().split() for _ in range(n)]

    print("GOING")

    def valid(word):
        for guess, feedback in guesses:
            if not valid_guess(word, guess, feedback):
                return False
        return True

    def valid_guess(word, guess, feedback):
        counts = {'G': 0, 'Y': 0, 'B': 0}
        for w, g in zip(word, guess):
            if w == g:
                counts['G'] += 1
            elif w in guess:
                counts['Y'] += 1
            else:
                counts['B'] += 1
        return all(counts[k] == feedback.count(k) for k in counts)

    def generate_words(l):
        if l == 1:
            return [c for c in 'abcdefghijklmnopqrstuvwxyz']
        else:
            words = []
            for prefix in generate_words(l - 1):
                for c in 'abcdefghijklmnopqrstuvwxyz':
                    words.append(prefix + c)
            return words

    for word in generate_words(l):
        if valid(word):
            print(word)
            break


main()
