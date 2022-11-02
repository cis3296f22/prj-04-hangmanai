import random
import time

# welcome user the game
print("\nWelcome to Hangman game\n")
# ask player for their name
name = input("Enter your name: ")
# wait for the game to start
print("Hello " + name + ", welcome to Hangman Extra!")
time.sleep(2)
print("The game is about to start!\n Let's play Hangman!")
time.sleep(3)


# main function
class Hangman():
    def __init__(self):
        # test of the words, later will be placed
        self.words_to_guess = None
        self.word = None
        self.length = None
        self.count = None
        self.display = None
        self.already_guessed = None
        self.play_game = None

        self.initialize()

    def initialize(self):
        self.words_to_guess = ["one", "two", "three", "four", "five", "six", "sevent", "eight", "nine", "ten", "zero"]
        # variable word to set a randomly picked word as the word to guess
        self.word = random.choice(words_to_guess)
        # set the length of the guessing word to the length of the picked word
        self.length = len(word)
        # initialize count as 0
        self.count = 0
        # display the word the underline will show how many letter are in the word.
        self.display = '_' * length
        self.already_guessed = []
        self.play_game = ""

    def play(self):
        main_loop()

    def main_loop(self):
        self.game()

        while self.repeat():
            self.game()
            self.play()

        self.end()

    # loop the game, as user if he or she wants to restart the game
    def repeat(self):
        # prompt user if he or she wants to play the game again
        play_game = input("Do You want to play again? y = yes, n = no \n")
        # accepted inputs are y,Y,n,N
        while play_game not in ["y", "n", "Y", "N"]:
            # if not them prompt the user again
            play_game = input("Please use valid input? y = yes, n = no \n")
        # if yes execute the main method again
        if play_game == "y":
            return True
        # if no then exit the game
        elif play_game == "n":
            print("Thanks For Playing! We expect you back again!")
            return False


    # hangman method with each stage of the hangman
    def game(self):
        self.initialize()
        # set lives
        limit = 5
        guess = input("This is the Hangman Word: " + self.display + " Enter your guess: \n")
        guess = guess.strip()
        # invalid input
        if len(guess.strip()) == 0 or len(guess.strip()) >= 2 or guess <= "9":
            print("Please enter a letter\n")
            hangman()

        # if guessed letter is correct
        elif guess in self.word:
            # add an index when letter correctly guessed
            already_guessed.extend([guess])
            index = self.word.find(guess)
            word = self.word[:index] + "_" + self.word[index + 1:]
            display = self.display[:index] + guess + self.display[index + 1:]
            print(display + "\n")

        # ask user to guess another guess
        elif guess in already_guessed:
            print("Try another letter.\n")

        # lost 1 live count +1
        else:
            self.count += 1

            if self.count == 1:
                time.sleep(1)
                print("   _____ \n"
                      "  |      \n"
                      "  |      \n"
                      "  |      \n"
                      "  |      \n"
                      "  |      \n"
                      "  |      \n"
                      "__|__\n")
                print("Wrong guess. " + str(limit - self.count) + " guesses remaining\n")

            # lost 2 lives count +2
            elif self.count == 2:
                time.sleep(1)
                print("   _____ \n"
                      "  |     | \n"
                      "  |     |\n"
                      "  |      \n"
                      "  |      \n"
                      "  |      \n"
                      "  |      \n"
                      "__|__\n")
                print("Wrong guess. " + str(limit - self.count) + " guesses remaining\n")

            # lost 3 lives count +3
            elif self.count == 3:
                time.sleep(1)
                print("   _____ \n"
                      "  |     | \n"
                      "  |     |\n"
                      "  |     | \n"
                      "  |      \n"
                      "  |      \n"
                      "  |      \n"
                      "__|__\n")
                print("Wrong guess. " + str(limit - self.count) + " guesses remaining\n")

            # lost 4 lives count +4
            elif self.count == 4:
                time.sleep(1)
                print("   _____ \n"
                      "  |     | \n"
                      "  |     |\n"
                      "  |     | \n"
                      "  |     O \n"
                      "  |      \n"
                      "  |      \n"
                      "__|__\n")
                print("Wrong guess. " + str(limit - self.count) + " last guess remaining\n")

            # lost 5 lives count +5
            elif self.count == 5:
                time.sleep(1)
                print("   _____ \n"
                      "  |     | \n"
                      "  |     |\n"
                      "  |     | \n"
                      "  |     O \n"
                      "  |    /|\ \n"
                      "  |    / \ \n"
                      "__|__\n")
                # show the word if the user failed to guess the word and lost all lives.
                print("Wrong guess. You are hanged!!!\n")
                print("The word was:", already_guessed, self.word)
                play_loop()

        # when guessed word equal to length
        if self.word == '_' * self.length:
            print("You won the game.")
            play_loop()

        elif self.count != limit:
            hangman()

if __name__ == "__main__":

