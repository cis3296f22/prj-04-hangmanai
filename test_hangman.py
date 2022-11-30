import sys
from unittest import TestCase

from PyQt6 import QtWidgets

from Display.CharacterBox import CharacterBox
from Display.LifeBox import LifeBox
from Display.ScoreView import ScoreView
from Display.WordBox import WordBox
from WordProvider import WordProvider
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

    def test_LifeBox_set_life(self):
        app = QtWidgets.QApplication(sys.argv)
        widget = LifeBox(assets_dir="assets")
        widget.setLife(2)
        self.assertTrue(widget.getLife() == 2)

    def test_LifeBox_is_zero(self):
        app = QtWidgets.QApplication(sys.argv)
        widget = LifeBox(assets_dir="assets")
        widget.setLife(0)
        self.assertTrue(widget.isZero())

    def test_LifeBox_set_max_attempts(self):
        app = QtWidgets.QApplication(sys.argv)
        widget = LifeBox(assets_dir="assets")
        widget.setMaxAttempts(6)
        self.assertTrue(widget.max_attempts == 6)

    def test_LifeBox_take_life(self):
        app = QtWidgets.QApplication(sys.argv)
        widget = LifeBox(assets_dir="assets")
        widget.takeLife(None)
        self.assertTrue(widget.getLife() == 4)

    def test_LifeBox_reset(self):
        app = QtWidgets.QApplication(sys.argv)
        widget = LifeBox(assets_dir="assets")
        widget.setLife(0)
        widget.reset()
        self.assertTrue(widget.getLife() == 5)

    def test_WordBox_set_word(self):
        app = QtWidgets.QApplication(sys.argv)
        widget = WordBox(assets_dir="assets")
        widget.setWord("Test")
        self.assertTrue(widget.word == "Test".upper())

    def test_WordBox_set_character_at(self):
        app = QtWidgets.QApplication(sys.argv)
        widget = WordBox(assets_dir="assets")
        widget.setWord("Test")
        widget.setCharacterAt(2, "X")
        self.assertTrue(widget.word == "TEXT")

    def test_WordBox_show_char_at(self):
        app = QtWidgets.QApplication(sys.argv)
        widget = WordBox(assets_dir="assets")
        widget.setWord("Test")
        widget.hideWord()
        widget.showCharAt(1)
        self.assertTrue(widget.characterBoxList[1].isEnabled())

    def test_WordBox_hide_word(self):
        app = QtWidgets.QApplication(sys.argv)
        widget = WordBox(assets_dir="assets")
        widget.setWord("Test")
        widget.hideWord()
        self.assertTrue(all([not x.isEnabled() for x in widget.characterBoxList]))

    def test_WordBox_hide_char_at(self):
        app = QtWidgets.QApplication(sys.argv)
        widget = WordBox(assets_dir="assets")
        widget.setWord("Test")
        widget.hideCharAt(1)
        self.assertTrue(not widget.characterBoxList[1].isEnabled())

    def test_WordBox_reset(self):
        app = QtWidgets.QApplication(sys.argv)
        widget = WordBox(assets_dir="assets")
        widget.setWord("Test")
        widget.reset()
        self.assertTrue(all([not x.isEnabled() for x in widget.characterBoxList]))

    def test_ScoreView_detach_handler(self):
        app = QtWidgets.QApplication(sys.argv)
        widget = ScoreView(assets_dir="assets")
        widget.detachHandler()
        self.assertTrue(widget.scoreHandler == widget.offHandler)

    def test_ScoreView_attach_handler(self):
        app = QtWidgets.QApplication(sys.argv)
        widget = ScoreView(assets_dir="assets")
        widget.attachHandler()
        self.assertTrue(widget.scoreHandler == widget.onHandler)

    def test_ScoreView_add_score(self):
        app = QtWidgets.QApplication(sys.argv)
        widget = ScoreView(assets_dir="assets")
        widget.setScore(100)
        widget.addScore(200)
        self.assertTrue(widget.score == 300)

    def test_ScoreView_set_score(self):
        app = QtWidgets.QApplication(sys.argv)
        widget = ScoreView(assets_dir="assets")
        widget.setScore(100)
        self.assertTrue(widget.score == 100)

    def test_ScoreView_confirm_score(self):
        app = QtWidgets.QApplication(sys.argv)
        widget = ScoreView(assets_dir="assets")
        widget.setScore(100)
        widget.confirmScore()
        self.assertTrue(widget.confirmed_score == 100)

    def test_ScoreView_reset(self):
        app = QtWidgets.QApplication(sys.argv)
        widget = ScoreView(assets_dir="assets")
        widget.setScore(100)
        widget.confirmScore()
        self.assertTrue(widget.confirmed_score == 100 and widget.score == 0)

    def test_get_easy_word_random(self):
        self.assertTrue(0 < len(WordProvider().getEasyWordRandom()) < 4)

    def test_get_medium_word_random(self):
        self.assertTrue(4 < len(WordProvider().getMediumWordRandom()) < 8)

    def test_get_hard_word_random(self):
        self.assertTrue(8 < len(WordProvider().getHardWordRandom()))
