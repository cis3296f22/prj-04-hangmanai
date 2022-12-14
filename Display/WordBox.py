import sys

from PyQt6 import QtWidgets, uic

from Display.CharacterBox import CharacterBox


class TestWindow(QtWidgets.QMainWindow):

    def __init__(self, parent=None):
        super(TestWindow, self).__init__(parent)
        self.form_widget = WordBox()
        self.setCentralWidget(self.form_widget)
        self.setLayout(QtWidgets.QHBoxLayout())
        self.show()

        # self.form_widget.blank()
        # self.form_widget.setCharacterAt(0, "a")
        # self.form_widget.setCharacterAt(len(self.word) - 1, "a")
        self.form_widget.hideCharAt(2)


class WordBox(QtWidgets.QWidget):
    """
        Word box of the word that is used for the hangman guess.

        Characters in the word box can be show and hidden with a command

    """

    def __init__(self, word: str = "Sample", assets_dir: str = "../assets"):
        super(WordBox, self).__init__()
        uic.loadUi(assets_dir + '/ui/wordBox.ui', self)
        self.assets_dir: str = assets_dir
        """ Path to asset directory"""
        self.word: str = word
        """ Word that is displayed in the WordBox"""
        self.characterBoxList: list[CharacterBox] = []
        """ List of CharacterBox that contains the each characters of word"""

        self.wordFrame.setLayout(QtWidgets.QHBoxLayout())
        self.setWord(word)

    def setWord(self, word: str, hide: bool = False) -> None:
        """
            Setter for the word in the word box

            Parameters:
            text (str): New word in word box

            Returns:
            None

        """
        self.word = word.upper()
        for char_box in self.characterBoxList:
            self.wordFrame.layout().removeWidget(char_box)

        self.characterBoxList.clear()

        # width = self.minimumWidth() * 0.8

        for char in self.word:
            char_box = CharacterBox(char, assets_dir=self.assets_dir)
            # char_box.label.setMinimumWidth(int(width / len(self.word)))
            self.characterBoxList.append(char_box)
            self.wordFrame.layout().addWidget(char_box)

        if hide:
            self.hideWord()
        else:
            self.showWord()

    def setCharacterAt(self, index: int, char: str) -> None:
        """
            Set the character of the letter at the specific index of the word

            Parameters:
            index (int): Index of char to be updated
            char (str): New char

            Returns:
            None

        """
        if index >= len(self.word):
            print("Character index should not be over the length of word set in word box")
            return
        self.word = self.word[:index] + char + self.word[index + 1:]
        self.setWord(self.word)

    def showWord(self) -> None:
        """
            Show all characters

            Returns:
            None

        """

        for charBox in self.characterBoxList:
            charBox.showChar()

    def showCharAt(self, index: int) -> None:
        """
            Show character at an index

            Parameters:
            index (int): Index of character in a word that you want to show

            Returns:
            None

        """
        self.characterBoxList[index].showChar()

    def hideWord(self) -> None:
        """
            Hide all of characters

            Returns:
            None

        """
        for charBox in self.characterBoxList:
            charBox.hideChar()

    def hideCharAt(self, index: int) -> None:
        """
            Hide character at an index

            Parameters:
            index (int): Index of character in a word that you want to hide

            Returns:
            None

        """
        self.characterBoxList[index].hideChar()

    def wrongChars(self) -> None:
        """
            Show the hidden characters as wrong guessed chars

            Returns:
            None

        """
        for charBox in self.characterBoxList:
            if not charBox.isShown():
                charBox.wrongChar()

    def reset(self) -> None:
        """
            Resets the word box by hiding all of letters

            Returns:
            None

        """
        self.hideWord()


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    widget = TestWindow()
    app.exec()
