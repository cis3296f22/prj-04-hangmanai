import sys

from PyQt6.QtCore import QUrl
from PyQt6.QtMultimedia import QSoundEffect

from GUI.MainFrame import MainFrame
from hangman import Hangman
import PyQt6


def main():
    app = PyQt6.QtWidgets.QApplication(sys.argv)
    main_frame = MainFrame(assets_dir="assets")
    game = Hangman(main_frame)
    filename = "assets/sound/sound.wav"
    effect = QSoundEffect()
    effect.setSource(QUrl.fromLocalFile(filename))
    # possible bug: QSoundEffect::Infinite cannot be used in setLoopCount
    effect.setLoopCount(-2)
    effect.play()
    app.exec()


if __name__ == "__main__":
    main()