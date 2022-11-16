import sys
from unittest import TestCase

from PyQt6 import QtWidgets

from Display.CharacterBox import CharacterBox
from hangman import Hangman
from Display.MainFrame import MainFrame


class TestHangman(TestCase):

    def test_set_up_display(self):
        app = QtWidgets.QApplication(sys.argv)
        main_frame = MainFrame(assets_dir="assets")
        game = Hangman(main_frame)
        game.setUpDisplay()
        self.assertTrue(True)

    def test_reset(self):
        app = QtWidgets.QApplication(sys.argv)
        main_frame = MainFrame(assets_dir="assets")
        game = Hangman(main_frame)
        game.reset()
        self.assertTrue(True)

    def test_update_ui(self):
        app = QtWidgets.QApplication(sys.argv)
        main_frame = MainFrame(assets_dir="assets")
        game = Hangman(main_frame)
        game.updateUI()
        self.assertTrue(True)

    def test_guess(self):
        app = QtWidgets.QApplication(sys.argv)
        main_frame = MainFrame(assets_dir="assets")
        game = Hangman(main_frame)
        game.guess("A", ["A", "B"])
        self.assertTrue(True)

    def test_finish_game_condition(self):
        app = QtWidgets.QApplication(sys.argv)
        main_frame = MainFrame(assets_dir="assets")
        game = Hangman(main_frame)
        game.finishGameCondition()
        self.assertTrue(True)

    def test_CharacterBox_text(self):
        app = QtWidgets.QApplication(sys.argv)
        charBox = CharacterBox(text="B", assets_dir="assets")
        self.assertTrue(charBox.text() == "B")

    def test_CharacterBox_set_text(self):
        app = QtWidgets.QApplication(sys.argv)
        charBox = CharacterBox(text="B", assets_dir="assets")
        charBox.setText("C")
        self.assertTrue(charBox.text() == "C")

    def test_CharacterBox_show_char(self):
        app = QtWidgets.QApplication(sys.argv)
        charBox = CharacterBox(assets_dir="assets")
        charBox.hideChar()
        charBox.showChar()
        self.assertTrue(charBox.isShown() == True)

    def test_CharacterBox_hide_char(self):
        app = QtWidgets.QApplication(sys.argv)
        charBox = CharacterBox(assets_dir="assets")
        charBox.hideChar()
        self.assertTrue(charBox.isShown() == False)

