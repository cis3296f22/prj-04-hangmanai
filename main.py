import random
from hangman_art import stages, logo
from hangman_words import word_list

def hangman_game(chosen_word):
    end_of_game = False

    lives = len(stages) - 1

    guessed_letters = []
    for _ in range(len(chosen_word)):
        guessed_letters += "_"

    while not end_of_game:
        guess = input("Guess a letter: ").lower()

        if guess in guessed_letters:
            print(f"You've already guessed {guess}")

        for position in range(len(chosen_word)):
            letter = chosen_word[position]
            if letter == guess:
                guessed_letters[position] = letter
        print(f"{' '.join(guessed_letters)}")

        if guess not in chosen_word:
            print(f"You guessed {guess}, that's not in the word. You lose a life.")
            lives -= 1
            if lives == 0:
                end_of_game = True
                print("You lose.")
                print(f"The word was {chosen_word}.")

        if not "_" in guessed_letters:
            end_of_game = True
            print("You win.")

        print(stages[lives])

if __name__ == " __main__":
    print(logo)
    chosen_word = random.choice(word_list)
    print(f"It is a {len(chosen_word)}-letters word.")
    hangman_game(chosen_word)
