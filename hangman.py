import random
import time

from PyQt6.QtMultimedia import QSoundEffect

from easywords_list import easylist
# from medianwords_list import medianlist
# from hardwords_list import hardlist
from PyQt6 import QtWidgets, uic, QtCore
from PyQt6.QtCore import Qt

from PyQt6 import QtCore, QtGui, QtWidgets
from PyQt6.QtCore import (QCoreApplication, QPropertyAnimation, QDate, QDateTime, QMetaObject, QObject, QPoint, QRect,
                          QSize, QTime, QTimer, QUrl, Qt, QEvent)

import sys

from GUI.MainFrame import MainFrame


# TODO Create new class which generates the list of words
# TODO Separate word generate and select from the actual game.
class Hangman():
    def __init__(self, main_frame: MainFrame, word: int = "Electrocardiographic", max_attempts: int = 6):
        # test of the words, later will be placed
        # self.word_list = ["one", "two", "three", "four", "five", "six", "sevent", "eight", "nine", "ten", "zero"]
        self.word: str = word
        self.attempts: int = 0
        self.max_attempts: int = max_attempts
        self.display: MainFrame = main_frame
        self.already_guessed = []
        # self.play_game = True
        self.name = "Unknown"

        # self.welcome()
        # self.initialize()

        self.updateUI()
        # FIXME CHECK Mainframe callback set here
        self.setUpDisplay()

    def setUpDisplay(self):
        self.display.setKeyboardListner(lambda x, y: self.guess(x, y))
        self.display.setMaxAttempts(self.max_attempts)
        self.display.setWord(self.word, True)
        self.display.setReplayHandler(self.reset)
        self.display.setHomeHandler(self.reset)

    def reset(self):
        self.setUpDisplay()
        self.attempts: int = 0
        self.already_guessed = []
        self.updateUI()

    def updateUI(self):
        print(self.max_attempts - self.attempts)
        self.display.setLife(self.max_attempts - self.attempts)
        self.display.setWord(self.word.upper(), True)

        for i in range(len(self.word)):
            if self.word.upper()[i] in self.already_guessed:
                self.display.showCharAt(i)
            else:
                self.display.hideCharAt(i)

        # self.welcome()
        # self.initialize()
    # FIXME Call back function for processing key pressing
    # NOTE Done coding, needs check
    def guess(self, char: str, used_chars: list[str]):
        if char.upper() in self.already_guessed:
            print("You cannot guess the same letter twice")
        self.already_guessed = used_chars

        if char.upper() not in self.word.upper():
            self.attempts = self.attempts + 1

        self.updateUI()

        self.finishGameCondition()

    # FIXME See if game ends 1) Attempts reaches 0 with incompleted word or 2) Guessed word correctly
    # NOTE Done coding, needs check
    def finishGameCondition(self):
        all_match = all([(x in self.already_guessed) for x in self.word.upper()])
        if self.max_attempts - self.attempts > 0 and all_match:
            self.display.win()
            self.display.setKeyboardListner( lambda x, y: print("[" + x + "] -> " + str(y)))
        elif self.attempts >= self.max_attempts:
            self.display.lose()
            self.display.setKeyboardListner(lambda x, y: print("[" + x + "] -> " + str(y)))
        else:
            return

    # TODO Deprecate this method
    # TODO Need GUI form system to accept name input
    # TODO Separate name input form from the actual game system

    def welcome(self):
        # welcome user the game
        print("\nWelcome to Hangman game\n")
        # ask player for their name
        self.name = input("Enter your name: ")
        # wait for the game to start
        print("Hello " + self.name + ", welcome to Hangman Extra!")
        # time.sleep(2)
        print("The game is about to start!\n Let's play Hangman!")
        # time.sleep(3)

    # promot for input for difficulty level
    def get_difficulty_input(self):

        difficulty = input('Before the game starts please pick a level! E for easy, M for median, H for hard!\n')
        return difficulty.upper()

    def initialize(self):
        difficulty = self.get_difficulty_input()

        # if difficulty == 'H':
        #     self.word = self.words_to_guess[hardlist]
        # elif difficulty == 'M':
        #     self.word = self.words_to_guess[medianlist]
        # else:
        #     self.word = self.words_to_guess[easylist]

        # self.word = random.choice(self.words_to_guess)
        self.length = len(self.word)
        self.count = 0
        self.display = '_' * self.length
        self.already_guessed = []
        self.play_game = ''

        # self.word_list = ["one", "two", "three", "four", "five", "six", "sevent", "eight", "nine", "ten", "zero"]
        # # variable word to set a randomly picked word as the word to guess
        # self.word = random.choice(self.word_list)
        # initialize attempts as 0
        # self.attempts = 0

        # display the word the underline will show how many letter are in the word.
        # self.display = '_' * self.length
        self.display.setWord(self.word)
        self.display.blank()
        # self.play_game = True

    def play(self):
        self.main_loop()

    def main_loop(self):
        self.game()
        while self.repeat():
            self.game()
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

    # TODO Deprecate this method
    # hangman method with each stage of the hangman
    def game(self):
        self.initialize()
        # set lives
        limit = 5

        while True:
            guess = input("This is the Hangman Word: " + self.display + " Enter your guess: \n")
            guess = guess.strip()
            # invalid input
            if len(guess.strip()) == 0 or len(guess.strip()) >= 2 or guess <= "9":
                print("Please enter a letter\n")
                continue

            # if guessed letter is correct
            elif guess in self.word:
                # add an index when letter correctly guessed
                self.already_guessed.extend([guess])
                index = self.word.find(guess)
                self.word = self.word[:index] + "_" + self.word[index + 1:]
                self.display = self.display[:index] + guess + self.display[index + 1:]
                print(self.display + "\n")

            # ask user to guess another guess
            elif guess in self.already_guessed:
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
                    print("The word was:", self.already_guessed, self.word)
                    break

            # when guessed word equal to length
            if self.word == '_' * self.length:
                print("You won the game.")
                return

            elif self.count != limit:
                continue


if __name__ == "__main__":
    # game = Hangman()
    # game.play()

    app = QtWidgets.QApplication(sys.argv)
    main_frame = MainFrame(assets_dir="assets")
    game = Hangman(main_frame)

    app.exec()
