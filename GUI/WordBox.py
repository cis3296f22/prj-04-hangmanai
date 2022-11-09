from PyQt6 import QtWidgets, uic
import sys
from GUI.CharacterBox import CharacterBox

class TestWindow(QtWidgets.QMainWindow):

    def __init__(self, parent=None):

        super(TestWindow, self).__init__(parent)
        self.form_widget = WordBox()
        self.setCentralWidget(self.form_widget)
        self.setLayout(QtWidgets.QHBoxLayout())
        self.show()


class WordBox(QtWidgets.QWidget):
    def __init__(self, word="Sample", assets_dir="../assets"):
        super(WordBox, self).__init__()
        uic.loadUi(assets_dir + '/ui/wordBox.ui', self)
        self.assets_dir = assets_dir
        self.wordFrame.setLayout(QtWidgets.QHBoxLayout())
        # self.wordFrame.layout().setSpacing(30)
        self.word = word
        self.characterBoxList = []
        self.setWord(word)
        # self.blank()
        # self.setCharacterAt(0, "a")
        # self.setCharacterAt(len(self.word) - 1, "a")
        self.hideCharAt(2)

    def setWord(self, word, hide=False):
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


    def setCharacterAt(self, index, char):
        if index >= len(self.word):
            print("Character index should not be over the length of word set in word box")
            return
        self.word = self.word[:index] + char + self.word[index + 1:]
        self.setWord(self.word)


    def showWord(self):
        for charBox in self.characterBoxList:
            charBox.showChar()

    def showCharAt(self, index):
        self.characterBoxList[index].showChar()

    def hideWord(self):
        for charBox in self.characterBoxList:
            charBox.hideChar()

    def hideCharAt(self, index):
        self.characterBoxList[index].hideChar()

    def reset(self):
        self.setWord("")

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    widget = TestWindow()
    app.exec()