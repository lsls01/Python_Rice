# template for "Guess the number" mini-project
# input will come from buttons and an input field
# all output for the game will be printed in the console

import simplegui
import random
import math

# initialize default global variables
num_range = 100
secret_num = 0
guess_time_left = 0

# helper function to start and restart the game
def new_game():
    # initialize global variables used in your code here
    global secret_num
    global num_range
    global guess_time_left
    secret_num = random.randrange(0, num_range)
    
    if num_range == 100:
        guess_time_left = 7
    elif num_range == 1000:
        guess_time_left = 10
    
    print "New game start. The range is from 0 to", num_range, "."
    print "Number of remaining guesses is", guess_time_left
    # remove this when you add your code    
    


# define event handlers for control panel
def range100():
    # button that changes the range to [0,100) and starts a new game 
    
    # remove this when you add your code    
    global num_range
    num_range = 100
    new_game()

def range1000():
    # button that changes the range to [0,1000) and starts a new game     
    
    global num_range
    num_range = 1000
    new_game()
    
def input_guess(guess):
    # main game logic goes here	
    
    # remove this when you add your code
    global secret_num
    global guess_time_left
    
    win = False
    
    print "Guess was", guess
    guess_time_left -= 1
    
    if int(guess) == secret_num:
        print "Correct!"
        win = True
    elif int(guess) > secret_num:
        print "Higher!"
        print "Number of remaining guesses is", guess_time_left
    else:
        print "Lower!"
        print "Number of remaining guesses is", guess_time_left
    
    if win:
        print "Congratulations!"
        new_game()
    elif guess_time_left == 0:
        print "Game over."
        new_game()
    
# create frame
my_frame = simplegui.create_frame("Game: Guess the number!", 250, 250)


# register event handlers for control elements and start frame
my_frame.add_input("Enter your guess", input_guess, 100)
my_frame.add_button("Range is [0,100)", range100, 100)
my_frame.add_button("Range is [0,1000)", range1000, 100)


# call new_game 
new_game()


# always remember to check your completed program against the grading rubric
