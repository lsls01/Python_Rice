# implementation of card game - Memory

import simplegui
import random

# helper function to initialize globals
def new_game():
    global deck_list, card_flipped, state, turns, current_flipped
    deck_list = range(8) * 2
    random.shuffle(deck_list)
    card_flipped = [False] * 16
    state = 0
    turns = 0
    current_flipped = [[0, 0]] * 2

     
# define event handlers
def mouseclick(pos):
    # add game state logic here
    global state, turns, current_flipped
    idx = pos[0] // 50
    if not card_flipped[idx]:
        if state == 0:
            state = 1
            current_flipped[0] = [deck_list[idx], idx]
        elif state == 1:
            state = 2
            current_flipped[1] = [deck_list[idx], idx]
            turns += 1
            label.set_text("Turns = " + str(turns))
        else:
            state = 1
            if current_flipped[0][0] != current_flipped[1][0]:
                card_flipped[current_flipped[0][1]] = False
                card_flipped[current_flipped[1][1]] = False
            current_flipped[0] = [deck_list[idx], idx]
                
    
    card_flipped[idx] = True

                        
# cards are logically 50x100 pixels in size    
def draw(canvas):
    for idx in range(16):
        if not card_flipped[idx]:
            canvas.draw_polygon(
                [(idx * 50, 0), (idx * 50, 100), \
                 ((idx + 1) * 50, 100), ((idx + 1) * 50, 0)], \
                5, 'Black', 'Green')
        else:
            canvas.draw_polygon(
                [(idx * 50, 0), (idx * 50, 100), \
                 ((idx + 1) * 50, 100), ((idx + 1) * 50, 0)], \
                3, 'Green')
            canvas.draw_text(str(deck_list[idx]), (idx * 50 + 8, 70), 60, 'Lime', 'monospace')


# create frame and add a button and labels
frame = simplegui.create_frame("Memory", 800, 100)
frame.add_button("Reset", new_game)
label = frame.add_label("Turns = 0")

# register event handlers
frame.set_mouseclick_handler(mouseclick)
frame.set_draw_handler(draw)

# get things rolling
new_game()
frame.start()


# Always remember to review the grading rubric