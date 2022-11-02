import random
import time

#welcome user the game
print("\nWelcome to Hangman game\n")
#ask player for their name
name = input("Enter your name: ")
#wait for the game to start
print("Hello " + name + ", welcome to Hangman Extra!")
time.sleep(2)
print("The game is about to start!\n Let's play Hangman!")
time.sleep(3)


#main function
def main():
    #variables for the game
    global count
    global display
    global word
    global already_guessed
    global length
    global play_game
    #test of the words, later will be placed
    words_to_guess = ["one","two","three","four","five","six","sevent","eight","nine","ten"
                   ,"zero"]
    #varibale word to set a randomly picked word as the word to guess
    word = random.choice(words_to_guess)
    #set the length of the guessing word to the length of the picked word
    length = len(word)
    #initalize count as 0
    count = 0
    #dispaly the word the underline will show how many letter are in the word.
    display = '_' * length
    already_guessed = []
    play_game = ""

#loop the game, as user if he or she wants to restart the game
def play_loop():
    global play_game
    #prompt user if he or she wants to play the game again
    play_game = input("Do You want to play again? y = yes, n = no \n")
    #accepted inputs are y,Y,n,N
    while play_game not in ["y", "n","Y","N"]:
        #if not them prompt the user again
        play_game = input("Please use valid input? y = yes, n = no \n")
    #if yes execute the main method again
    if play_game == "y":
        main()
    #if no then exit the game
    elif play_game == "n":
        print("Thanks For Playing! We expect you back again!")
        exit()

#hangman method with each stage of the hangman
def hangman():
    global count
    global display
    global word
    global already_guessed
    global play_game
    #set lives
    limit = 5
    guess = input("This is the Hangman Word: " + display + " Enter your guess: \n")
    guess = guess.strip()
    #invalid input
    if len(guess.strip()) == 0 or len(guess.strip()) >= 2 or guess <= "9":
        print("Please enter a letter\n")
        hangman()

    #if guessed letter is correct
    elif guess in word:
        #add an index when letter correctly guessed
        already_guessed.extend([guess])
        index = word.find(guess)
        word = word[:index] + "_" + word[index + 1:]
        display = display[:index] + guess + display[index + 1:]
        print(display + "\n")

    #ask user to guess another guess
    elif guess in already_guessed:
        print("Try another letter.\n")

    #lost 1 live count +1
    else:
        count += 1

        if count == 1:
            time.sleep(1)
            print("   _____ \n"
                  "  |      \n"
                  "  |      \n"
                  "  |      \n"
                  "  |      \n"
                  "  |      \n"
                  "  |      \n"
                  "__|__\n")
            print("Wrong guess. " + str(limit - count) + " guesses remaining\n")

        #lost 2 lives count +2
        elif count == 2:
            time.sleep(1)
            print("   _____ \n"
                  "  |     | \n"
                  "  |     |\n"
                  "  |      \n"
                  "  |      \n"
                  "  |      \n"
                  "  |      \n"
                  "__|__\n")
            print("Wrong guess. " + str(limit - count) + " guesses remaining\n")

        #lost 3 lives count +3
        elif count == 3:
           time.sleep(1)
           print("   _____ \n"
                 "  |     | \n"
                 "  |     |\n"
                 "  |     | \n"
                 "  |      \n"
                 "  |      \n"
                 "  |      \n"
                 "__|__\n")
           print("Wrong guess. " + str(limit - count) + " guesses remaining\n")

        #lost 4 lives count +4
        elif count == 4:
            time.sleep(1)
            print("   _____ \n"
                  "  |     | \n"
                  "  |     |\n"
                  "  |     | \n"
                  "  |     O \n"
                  "  |      \n"
                  "  |      \n"
                  "__|__\n")
            print("Wrong guess. " + str(limit - count) + " last guess remaining\n")

        #lost 5 lives count +5
        elif count == 5:
            time.sleep(1)
            print("   _____ \n"
                  "  |     | \n"
                  "  |     |\n"
                  "  |     | \n"
                  "  |     O \n"
                  "  |    /|\ \n"
                  "  |    / \ \n"
                  "__|__\n")
            #show the word if the user failed to guess the word and lost all lives.
            print("Wrong guess. You are hanged!!!\n")
            print("The word was:",already_guessed,word)
            play_loop()

    #when guessed word equal to length
    if word == '_' * length:
        print("You won the game.")
        play_loop()

    elif count != limit:
        hangman()


main()


hangman()