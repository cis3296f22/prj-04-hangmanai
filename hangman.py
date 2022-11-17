# from medianwords_list import medianlist
# from hardwords_list import hardlist

import sys

from PyQt6 import QtWidgets

from Display.MainFrame import MainFrame


class Hangman():
    def __init__(self, main_frame: MainFrame, word: str = "Dichlorodifluoromethane", max_attempts: int = 6):

        self.word: str = word
        self.attempts: int = 0
        self.max_attempts: int = max_attempts
        self.display: MainFrame = main_frame

        self.already_guessed = []

        self.name = "Unknown"
        self.setUpDisplay()
        self.updateUI()

    def setUpDisplay(self):
        self.display.setKeyboardListner(lambda x, y: self.guess(x, y))
        self.display.setMaxAttempts(self.max_attempts)
        self.display.setWord(self.word, True)
        self.display.setReplayHandler(self.reset)
        self.display.setHomeHandler(self.reset)
        self.display.attachScoreHandler()

    def reset(self):
        self.setUpDisplay()
        self.attempts: int = 0
        self.already_guessed = []
        self.updateUI()

    def updateUI(self):
        self.display.setLife(self.max_attempts - self.attempts)

        for i in range(len(self.word)):
            if self.word.upper()[i] in self.already_guessed:
                self.display.showCharAt(i)
            else:
                self.display.hideCharAt(i)

    def guess(self, char: str, used_chars: list[str]):
        if char.upper() in self.already_guessed:
            print("You cannot guess the same letter twice")
        self.already_guessed = used_chars

        if char.upper() not in self.word.upper():
            self.attempts = self.attempts + 1

        self.updateUI()
        self.display.updateScore(char, used_chars, self.word)

        self.finishGameCondition()

    def finishGameCondition(self):
        all_match = all([(x in self.already_guessed) for x in self.word.upper()])
        if self.max_attempts - self.attempts > 0 and all_match:
            self.display.win()
            self.display.setKeyboardListner(lambda x, y: print("[" + x + "] -> " + str(y)))
            self.display.detachScoreHandler()
        elif self.attempts >= self.max_attempts:
            self.display.lose()
            self.display.setKeyboardListner(lambda x, y: print("[" + x + "] -> " + str(y)))
            self.display.detachScoreHandler()
        else:
            return


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    main_frame = MainFrame(assets_dir="assets")
    game = Hangman(main_frame)

    app.exec()
