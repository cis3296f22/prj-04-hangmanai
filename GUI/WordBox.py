from PyQt6 import QtWidgets, uic
import sys
from GUI.CharactorBox import CharacterBox

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
        self.wordFrame.layout().setSpacing(20)
        self.word = word
        self.characterBoxList = []
        self.setWord(word)
        # self.blank()
        # self.setCharactorAt(0, "a")
        # self.setCharactorAt(len(self.word) - 1, "a")
        self.blankAt(2)

    def setWord(self, word):
        self.word = word.upper()
        for char_box in self.characterBoxList:
            self.wordFrame.layout().removeWidget(char_box)

        self.characterBoxList.clear()

        for char in self.word:
            char_box = CharacterBox(char, assets_dir=self.assets_dir)
            self.characterBoxList.append(char_box)
            self.wordFrame.layout().addWidget(char_box)

    def setCharactorAt(self, index, char):
        if index >= len(self.word):
            print("Character index should not be over the length of word set in word box")
            return
        self.word = self.word[:index] + char + self.word[index + 1:]
        self.setWord(self.word)

    def blankAt(self, index):
        self.setCharactorAt(index, " ")

    def blank(self):
        self.setWord(" " * len(self.word))

    def reset(self):
        self.setWord("")

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    widget = TestWindow()
    app.exec()