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
        Simple Button Class for the Hangman game UI.

        This can add the flexible button to the hangman UI with text, button function, custom colors (background, foreground, border)

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

    def getWord(self):
        return "".join([x.text() for x in self.characterBoxList])

    def setWord(self, word: str, hide: bool = False) -> None:
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
        if index >= len(self.word):
            print("Character index should not be over the length of word set in word box")
            return
        self.word = self.word[:index] + char + self.word[index + 1:]
        self.setWord(self.word)


    def showWord(self) -> None:
        for charBox in self.characterBoxList:
            charBox.showChar()

    def showCharAt(self, index: int) -> None:
        self.characterBoxList[index].showChar()

    def hideWord(self) -> None:
        for charBox in self.characterBoxList:
            charBox.hideChar()

    def hideCharAt(self, index: int) -> None:
        self.characterBoxList[index].hideChar()

    def wrongChars(self) -> None:
        for charBox in self.characterBoxList:
            if not charBox.isShown():
                charBox.wrongChar()

    def wrongCharAt(self, index: int) -> None:
        self.characterBoxList[index].wrongChar()

    def reset(self) -> None:
        self.hideWord()



if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    widget = TestWindow()
    app.exec()