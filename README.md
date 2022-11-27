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


# UMLs Diagram
## Class Diagram
![image](https://user-images.githubusercontent.com/71058334/204118142-93484e20-5783-496f-8baa-1788ae630331.png)
The MainFrame sets up the GUI for the user to interact with. The MainFrame creates the user interface for the hidden word that is needed to guess, a virtual keyboard, a view of what the webcam (webcam_access) sees, the hangman’s gallow, and life circles on the top to indicate the remaining guesses. The main creates the actual game for the user to play. When the game is instantiated, users will be directed to the Home (home.py) page of the game with difficulties buttons of 3 types of modes, easy, normal and hard game modes. The word of each difficulty is provided by WordProvider class and WordProvider class will web scrape the dictionary website, acquire a list of words and pass them to the game while the home page is shown. The click of the difficulty button will direct the user to the main game page (HangmanUi). The user will interact with the game through the virtual keyboard (Keyboard) and camera (Camera) to control the hangman game and select letters from them. The correct guess of the letter in a word will show up the letter in the word box (WordBox) and add score in a display (ScoreView). On the other hand, the wrong guess will update the hangman animation (HangmanView) with animation and sound feedback to indicate that the guess is incorrect. The both success and failure of the game will give options of the replay and return to the home on the hangnam view by calling the showReplyButton and showHomeButton on the HangmanView class. The score view is responsible for calculating and storing the score in the game. The successful guess of letters and the word will result in the increase of the score. The camera image is provided by the webcam_access class of the system and MainFrame requests for the update of the camera image and the webcam_access access to the camera in the hardware system of the user and provides the picture to MainFrame. The webcam_access class uses pytesseract which is a wrapper class of the tesseract api. Using open-cv it gains access to the webcam on the machine. Using open-cv in tandem with pytesseract it grabs the frames captured by the camera and processes the image. Before sending it to pytesseract the image has dilation, erosion, and a gaussian blur applied. This is done to reduce the amount of noise in the image, ideally getting only what the user wrote. Pytesseract will analyze the image and produce the bounding boxes and the text equivalent to what the user wrote. The text from this is sent to the MainFrame to be processed displaying if the letter was correct or not. 


## Sequence Diagram 1
![image](https://user-images.githubusercontent.com/71058334/204118111-b7e76a52-f04c-4970-b6a7-06deef035314.png)
The player starts the game, startGame(), and will see the MainFrame which is the GUI the user will interact with. When the MainFrame starts up it will display the user interface and activate the WebcamAdapter. When the WebcamAdapter activates it will communicate with the physical hardware and request an image, captureImage(), of what the webcam is currently viewing. This would be done by the user when they confirm what they want to send into the game. The WebcamAdpater will receive the image from the hardware and send it to the MainFrame and the handwritten recognition software, HTR (Handwritten text recognition). HTR will process the image, ProcessLetter(), and send it to the Hangman Core. The Hangman core will evaluate the letter given and send the new information to the GUI so the user can see the feedback from their input.  

## Sequence Diagram 2
![image](https://user-images.githubusercontent.com/71058334/204118131-e0a39d93-64fa-4964-b5ec-5708f4a57f11.png)
The player is an actor in the system and who starts the game. The player interacts with our interface, MainFrame. When a player starts playing the game, which is a startGame() action in the diagram, MainFrame will initialize the interface of the game and be ready for the player input from the virtual keyboard. At the same time, hangman core game program will be initialized and connected to GUI MainFrame by wiring the callback functions to each functionality of MainFrame. For example, keyboard and game are connected by the keyboardListener it is set from Hangman core game by MainFrame.setKeyboardListener(). When MainFrame is instantiated, the frame will show the Home page by setting Home widget as central widget of the MainFrame. Then the player will select difficulty from the home page. The button click on the one of difficulty buttons will trigger the page transition from Home page to HangmanUi, which is main game page of the system. This is done by first taking the Home page out of the frame and setting the HangmanUi as central widget of the frame. The player will see the game interface and interact mainly with virtual keyboard and camera. When keys in the virtual keyboard are pressed, PressButtonOnVirtualKeyboard() in a diagram, keyboardEvent will be signaled to the Keyboard object of MainFrame. This will trigger the callback function or keyboard listener function set to the keyboard from Hangman Core at the beginning of the instantiation. The guess() function in Hangman Core game will be called as a callback function from the keyboard and the core game will update the UI of MainFrame such as changing visibility of characters, remaining life and updating score based on correct and wrong guesses. After updating the UI, MainFrame will automatically repaint itself to show the update of UI to the player.

# Vision statement
**FOR** friends and family **WHO** has limited knowledge of IT/computer technology but wants to enjoy a classic word game. **Hangman EXTRA** is the classic game of hangman with a computerized twist **THAT** can be played without keyboard input and for anyone with little knowledge of computers. **UNLIKE** other basic hangman or word games **OUR** product is more engaging to play because of the image recognition AI. 

# Personas
Persona: James, a elementary school teacher: Timothy

James is a 33 year old elementary school teacher that lives in Abington, PA. He teaches
Second grade students at Copper Beech elementary school. He was born and raised in Philadelphia and went to Temple University for his teaching degree. Eventually he moved out of the city with his wife to try and start a family in the suburbs. One of his hobbies is playing table-top games. Every weekend James and his friends get together 
to play these games. 

James likes to use games to help teach his second grade students. It keeps the students engaged with the material and it is fun for everyone involved. During the pandemic it became more difficult to employ these games over a zoom meeting. James wants to keep using games to teach his students since the kids are having more trouble focusing at home. One day he comes across a hangman game that uses handwriting recognition to play. James is not the most experienced with technology but wants to try this game, Hangman Extra, with his students. James thinks this will be a good way for his students to better their spelling skills. Also, since this is a piece of software James hopes that his students will play Hangman Extra in their free time with each other. 

Persona: Kevin McGibler, a 7 year old first grader: Mingjie

Kevin McGibler, age 7, he is a first grade student lives in Philadelphia, PA, Kevin goes to Ethan Allen elementary school. Growing up Kevin had many friends to play with, he loves American football, basketball and baseball. Kevin is a very energetic kid who loves physical activities and he is very good at it, he never found computer or video games to be interesting, so growing up Kevin isn’t good with technology especially computers, the only technology he knows how to use is the TV, he uses the TV remote to watch his favorite cartoon films and sport channels.

One day Kevin walked into the classroom and saw many of his classmates were playing a game called Hangman Extra. Kevin wasn’t interested at first because he doesn’t like to play computer games but as time passed by more and more people joined the game and it seems like everybody is enjoying the game. Now Kevin wants to play the game but he is worried that people will laugh at him because he doesn’t know how to use a computer. As Kevin stands there his friends saw him and ask him if he wants to play the game or not, Kevin explains his worry to his friends and they told Kevin not to worry, he can play the game without any knowledge of computer because the game Hangman Extra was built on the famous Hangman game with extra features. The game can recognize text and images and take them as commands to play the game, all he has to do is write down a letter and then show it to the camera. Kevin doesn’t even have to touch the computer to participate in the game.

 Persona: Bryon Hopkins, a 19 year old college student : Keita
 
Bryon Hopkins, age 19, is a college student in Halmstad, a large coastal city in sweden. He grew up in Stensjö, a village located north from Halmstad. From childhood, he loved to play with his grandparents who lived together with his parents and his grandparents were very caring with him and loved spending time with him. He entered Halmstad University when he was 18 years old with an eagerness to learn business and acquire a bachelor degree in the field. 

As he entered university in Halmstad, he started to live in a dormitory with his roommates and he misses the time he spent with his grandparents. He returned to his hometown every holiday between semesters but he wished to meet grandparents every month to see they are doing fine. During his second semester, he found an online game Hangman Extra, which has an ability to play famous game hangman over the internet with a camera so that players do not need to type letters but only show letters to camera to play the game. He uses this game every weekend to share time with his grandparents. This game was best for him to play with his parents with a given situation, where they live far away and they are not good at computers from their ages. They can play games together without worrying about computer technology and he is very thankful to modern AI technology.
