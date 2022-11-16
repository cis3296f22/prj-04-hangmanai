import sys
from unittest import TestCase

import cv2
from PyQt6 import QtWidgets

from Display.CharacterBox import CharacterBox
from Display.HangmanView import HangmanView
from Display.Keyboard import Keyboard
from hangman import Hangman
from Display.MainFrame import MainFrame
from Camera.webcam_access import Webcam_Access

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

    def test_HangmanView_show_replay_button(self):
        app = QtWidgets.QApplication(sys.argv)
        hangmanView = HangmanView(assets_dir="assets")
        hangmanView.showReplayButton()
        self.assertTrue(True)

    def test_HangmanView_hide_replay_button(self):
        app = QtWidgets.QApplication(sys.argv)
        hangmanView = HangmanView(assets_dir="assets")
        hangmanView.hideReplayButton()
        self.assertTrue(True)

    def test_HangmanView_take_damage(self):
        app = QtWidgets.QApplication(sys.argv)
        hangmanView = HangmanView(assets_dir="assets")
        print(hangmanView.attempts)
        hangmanView.attempts = 5
        hangmanView.takeDamage()
        self.assertTrue(hangmanView.attempts == 4)

    def test_HangmanView_set_replay_handler(self):
        app = QtWidgets.QApplication(sys.argv)
        hangmanView = HangmanView(assets_dir="assets")
        hangmanView.setReplayHandler(lambda: print("Reply Handler"))
        self.assertTrue(True)

    def test_HangmanView_set_home_handler(self):
        app = QtWidgets.QApplication(sys.argv)
        hangmanView = HangmanView(assets_dir="assets")
        hangmanView.setHomeHandler(lambda: print("Home Handler"))
        self.assertTrue(True)

    def test_HangmanView_set_stage_progress(self):
        app = QtWidgets.QApplication(sys.argv)
        hangmanView = HangmanView(assets_dir="assets")
        hangmanView.setStageProgress(0.5)
        self.assertTrue(hangmanView.progress_percentage == 0.5)

    def test_HangmanView_set_max_attempts(self):
        app = QtWidgets.QApplication(sys.argv)
        hangmanView = HangmanView(assets_dir="assets")
        hangmanView.setMaxAttempts(5)
        self.assertTrue(hangmanView.max_attempts == 5)

    def test_HangmanView_reset(self):
        app = QtWidgets.QApplication(sys.argv)
        hangmanView = HangmanView(assets_dir="assets")
        hangmanView.setMaxAttempts(5)
        hangmanView.attempts = 0
        hangmanView.reset()
        self.assertTrue(hangmanView.max_attempts == 5)

    def test_HangmanView_drawings(self):
        app = QtWidgets.QApplication(sys.argv)
        hangmanView = HangmanView(assets_dir="assets")
        hangmanView.setStageProgress(1)
        hangmanView.repaint()
        self.assertTrue(True)

    def test_Keyboard_HangmanView_get_toggle_keys(self):
        app = QtWidgets.QApplication(sys.argv)
        keyboard = Keyboard(assets_dir="assets")
        keyboard.disableAll()
        disabledKeys = keyboard.getToggleKeys()
        keyboard.enableAll()
        enabledKeys = keyboard.getToggleKeys()
        b = len(disabledKeys)
        self.assertTrue("".join(disabledKeys) == "QWERTYUIOPASDFGHJKLZXCVBNM" and len(enabledKeys) == 0)

    def test_Keyboard_set_keyboard_listner(self):
        app = QtWidgets.QApplication(sys.argv)
        keyboard = Keyboard(assets_dir="assets")
        keyboard.disableAll()
        keyboard.setKeyboardListner(lambda: print("Keyboard listener"))

    def test_determine_camera(self):
        webcam = Webcam_Access()
        cam_found = webcam.determine_camera()
        if cam_found > -1:
            assert True
        else:
            assert False

    def test_take_pic(self):
        webcam = Webcam_Access()
        cam_id = webcam.determine_camera()
        print(cam_id)
        cap = cv2.VideoCapture(cam_id)
        ret, frame = cap.read()
        if ret == False:
            assert False
        result = Webcam_Access.take_pic(frame)
        if result == True:
            assert True

    def test_start_capture(self):
        webcam = Webcam_Access()
        webcam.start_capture(0)
        assert True


