import random
import time
from PyQt6 import QtWidgets, uic, QtCore
from PyQt6.QtCore import Qt

from PyQt6 import QtCore, QtGui, QtWidgets
from PyQt6.QtCore import (QCoreApplication, QPropertyAnimation, QDate, QDateTime, QMetaObject, QObject, QPoint, QRect,
                          QSize, QTime, QTimer, QUrl, Qt, QEvent)

import sys

from GUI.MainFrame import MainFrame


# main function
class Hangman():
    def __init__(self, main_frame, word="sample", max_attempts=6):
        # test of the words, later will be placed
        # self.word_list = ["one", "two", "three", "four", "five", "six", "sevent", "eight", "nine", "ten", "zero"]
        self.word = word
        self.attempts = 0
        self.max_attempts = max_attempts
        self.display = main_frame
        self.already_guessed = []
        # self.play_game = True
        self.name = "Unknown"

        # self.welcome()
        # self.initialize()
        self.updateUI()

    def updateUI(self):
        for i in range(len(self.word)):
            character = self.word[i] if self.word[i] in self.already_guessed else " "
            self.display.setCharacterAt(i, character)

    # FIXME Call back function for processing key pressing
    def guess(self, char):
        if char in self.already_guessed:
            print("You cannot guess the same letter twice")

        self.already_guessed.append(char)
        self.attempts = self.attempts - 1

        self.updateUI()

        self.finishGameCondition()

    # FIXME See if game ends 1) Attempts reaches 0 with incompleted word or 2) Guessed word correctly
    def finishGameCondition(self):
        all_match = all([(x in self.already_guessed) for x in self.word])
        if self.attempts == 0 and all_match:
            self.display.win()
        elif self.attempts != 0:
            return
        else:
            self.display.lose()

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

    def initialize(self):
        self.word_list = ["one", "two", "three", "four", "five", "six", "sevent", "eight", "nine", "ten", "zero"]
        # variable word to set a randomly picked word as the word to guess
        self.word = random.choice(self.word_list)
        # initialize attempts as 0
        # self.attempts = 0

        # display the word the underline will show how many letter are in the word.
        # self.display = '_' * self.length
        self.display.setWord(self.word)
        self.display.blank()
        # self.play_game = True

    # def play(self):
    #     self.main_loop()

    # def main_loop(self):
    #     self.game()
    #     while self.repeat():
    #         self.game()
    #     self.end()

    # TODO callback event for yes/no button action to inquire user for the next match
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

            # lost 1 live attempts +1
            else:
                self.attempts += 1

                if self.attempts == 1:
                    time.sleep(1)
                    print("   _____ \n"
                          "  |      \n"
                          "  |      \n"
                          "  |      \n"
                          "  |      \n"
                          "  |      \n"
                          "  |      \n"
                          "__|__\n")
                    print("Wrong guess. " + str(limit - self.attempts) + " guesses remaining\n")

                # lost 2 lives attempts +2
                elif self.attempts == 2:
                    time.sleep(1)
                    print("   _____ \n"
                          "  |     | \n"
                          "  |     |\n"
                          "  |      \n"
                          "  |      \n"
                          "  |      \n"
                          "  |      \n"
                          "__|__\n")
                    print("Wrong guess. " + str(limit - self.attempts) + " guesses remaining\n")

                # lost 3 lives attempts +3
                elif self.attempts == 3:
                    time.sleep(1)
                    print("   _____ \n"
                          "  |     | \n"
                          "  |     |\n"
                          "  |     | \n"
                          "  |      \n"
                          "  |      \n"
                          "  |      \n"
                          "__|__\n")
                    print("Wrong guess. " + str(limit - self.attempts) + " guesses remaining\n")

                # lost 4 lives attempts +4
                elif self.attempts == 4:
                    time.sleep(1)
                    print("   _____ \n"
                          "  |     | \n"
                          "  |     |\n"
                          "  |     | \n"
                          "  |     O \n"
                          "  |      \n"
                          "  |      \n"
                          "__|__\n")
                    print("Wrong guess. " + str(limit - self.attempts) + " last guess remaining\n")

                # lost 5 lives attempts +5
                elif self.attempts == 5:
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

            elif self.attempts != limit:
                continue


if __name__ == "__main__":
    # game = Hangman()
    # game.play()

    app = QtWidgets.QApplication(sys.argv)
    main_frame = MainFrame(assets_dir="assets")
    game = Hangman(main_frame)

    app.exec()
