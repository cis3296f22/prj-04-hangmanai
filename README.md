# Hangman Extra
This application can take an image of a handwritten document, recognize the letters in the image, and produce text from it. This will be used to play hangman, a game where a player thinks of a secret word and other players try to spell it out one letter at a time, knowing only the length of the word and whether previously guessed letters are in it. Each correct guess fills in a blank space with the letter, each incorrect guess gets you one step closer to losing. Players have 6 incorrect guesses before the game is ended and the word is revealed. Each letter will be guessed by using a handwritten photo of a letter that is scanned into text.

# Before we run
- Download the latest release file from the release section in GitHub and unzip it.
- Download the latest Python 3.9 from here (https://www.python.org/downloads/)
- Download Tesseract from here ([https://www.python.org/downloads/](https://tesseract-ocr.github.io/tessdoc/Installation.html))
- Install needed python libraries for this project

```
pip install pyqt6
```
```
pip install bs4
```
```
pip install requests
```
```
pip install Enum
```
```
pip install urllib
```
```
pip install requests
```
```
pip install qt6-tools
```
```
pip install opencv-python
```
```
pip install numpy
```
```
pip install pip install pytesseract
```

- Move to the project folder and on the command line run with
```
python main.pyw
```
- You will see GUI screen

## How to build
1. Install PyCharm from here (https://www.jetbrains.com/pycharm/download/)
  - Select community version for free access.
1. Install Python from here (https://www.python.org/downloads/)
  - Make sure to tick the term "Add Python 3.9 to PATH" to run Python from console.
1. Do a git clone command to download our project from our repository  
```
https://github.com/cis3296f22/prj-04-hangmanai.git
```
1. To run our project you will first need to check that your python version is at least 3.9
1. Before you run the project make sure you installed all the Python libraries listed above in installation 
1. When installing pytesseract onto your computer you need to use the link provided. Locate where the executable is located. Get the full path to the executable and copy it into the CameraThread.py file. Specifically look for pytesseract.pytesseract.tesseract_cmd = ‘Paste full path here’ also in the virtual environment install pytesseract
1. Default_word_list contains words for offline play, you can add more to it if you like, other words are generated from an online dictionary by word scrape.
1. Right click hangman.py to run our game, make sure you have your camera on.
1. Enjoy!

```
pip install pyqt6
```
