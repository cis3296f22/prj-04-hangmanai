# Hangman Extra
This application can take an image of a handwritten document, recognize the letters in the image, and produce text from it. This will be used to play hangman, a game where a player thinks of a secret word and other players try to spell it out one letter at a time, knowing only the length of the word and whether previously guessed letters are in it. Each correct guess fills in a blank space with the letter, each incorrect guess gets you one step closer to losing. Players have 6 incorrect guesses before the game is ended and the word is revealed. Each letter will be guessed by using a handwritten photo of a letter that is scanned into text.

# Installation
```
pip install foobar
```

# How to run 
- Download the latest release file from the release section in GitHub and unzip it.
- Download the latest Python 3.9 from here (https://www.python.org/downloads/)
- Install needed python libraries for this project

```
pip install pyqt6
```
- Move to the project folder and on the command line run with
```
python main.pyw
```
- You will see GUI screen


## How to build
- Install PyCharm from here (https://www.jetbrains.com/pycharm/download/)
  - Select community version for free access.
- Install Python from here (https://www.python.org/downloads/)
  - Make sure to tick the term "Add Python 3.9 to PATH" to run Python from console.
- Install Pyqt6 GUI library for this application.
  - Go to Setting -> Project -> Project Interpreter -> Add mark -> search for pyqt6 -> Install
  - Or you can use command line to install
```
pip install pyqt6
```
