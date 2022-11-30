# from medianwords_list import medianlist
# from hardwords_list import hardlist

import sys

from PyQt6 import QtWidgets

from Display.MainFrame import MainFrame
from WordProvider import WordProvider


class Hangman():

    """
        Hangman class is the main executable for the whole program

        GUI display and words

    """

    def __init__(self, main_frame: MainFrame, word: str = "Dichlorodifluoromethane", max_attempts: int = 6):

        self.word: str = word.upper()
        self.attempts: int = 0
        self.max_attempts: int = max_attempts
        self.display: MainFrame = main_frame
        self.wordProvider: WordProvider = WordProvider()

        self.already_guessed = []

        self.name = "Unknown"
        self.setUpDisplay()
        self.updateUI()

    def setUpDisplay(self):

        """
            Set up the display for the GUI

            Parameters:
            self

            Returns:
            None

        """

        self.display.setKeyboardListner(lambda x, y: self.guess(x, y))
        self.display.setDifficultyHandler(lambda x: [self.wordProvider.setDifficulty(x), print(str(x), self.setWord(self.wordProvider.getRandomWord()))])
        self.setWord(self.wordProvider.getRandomWord())
        self.display.setMaxAttempts(self.max_attempts)
        self.display.setReplayHandler(lambda : [self.reset(), print("Reply Handler"), self.display.reset()], False)
        self.display.setHomeHandler(lambda : [self.reset(), print("Home Handler"), self.display.transitHome(), self.display.reset()], False)

    def reset(self):

        """
            reset the game

            Parameters:
            self

            Returns:
            None

        """

        self.setUpDisplay()
        self.attempts: int = 0
        self.already_guessed = []
        self.updateUI()

    def updateUI(self):

        """
            update the UI

            Parameters:
            self

            Returns:
            None

        """

        self.display.setLife(self.max_attempts - self.attempts)

        for i in range(len(self.word)):
            if self.word.upper()[i] in self.already_guessed:
                self.display.showCharAt(i)
            else:
                self.display.hideCharAt(i)


    def guess(self, char: str, used_chars):

        """
            display the letters and used letter in the GUI

            Parameters:
            char: letter
            uesd_chars: show the already guessed letters

            Returns:
            None

        """

        if char.upper() in self.already_guessed:
            print("You cannot guess the same letter twice")
        self.already_guessed = used_chars

        if char.upper() not in self.word.upper():
            self.attempts = self.attempts + 1

        if char in self.word.upper():
            self.display.correctGuess(sum([char == x for x in self.word.upper()]))
        else:
            self.display.wrongGuess()

        self.display.repaint()
        self.updateUI()
        # self.display.updateScore(char, used_chars, self.word)


        self.finishGameCondition()

    def finishGameCondition(self):

        """
            display all the condition for finish game

            Parameters:
            self

            Returns:
            None

        """

        all_match = all([(x in self.already_guessed) for x in self.word.upper()])
        if self.max_attempts - self.attempts > 0 and all_match:
            self.display.win()
            self.display.setKeyboardListner(lambda x, y: print("[" + x + "] -> " + str(y)))
            self.display.repaint()
        elif self.attempts >= self.max_attempts:
            self.display.lose()
            self.display.wrongChars()
            self.display.setKeyboardListner(lambda x, y: print("[" + x + "] -> " + str(y)))
            self.display.repaint()
        else:
            return

    def setWord(self, word: str):

        """
            set word function

            Parameters:
            word: set the word for the GUI display

            Returns:
            None

        """

        self.word = word.upper()
        self.display.setWord(self.word, True)

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    main_frame = MainFrame(assets_dir="assets")
    game = Hangman(main_frame)

    app.exec()
