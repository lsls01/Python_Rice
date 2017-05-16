# template for "Stopwatch: The Game"
import simplegui

# define global variables
current_time = 0
total_stop_time = 0
stop_on_whole_second_time = 0
is_started = False

# define helper function format that converts time
# in tenths of seconds into formatted string A:BC.D
def format(val):
    part1 = str(val // 600)
    part2 = ('0' if len(str(val % 600 // 10)) == 1 else '') + str(val % 600 // 10)
    part3 = str(val % 600 % 10)
    return (part1 + ':' + part2 + '.' + part3)    

# define event handlers for buttons; "Start", "Stop", "Reset"
def start_handler():
    global is_started
    is_started = True
    timer.start()

def stop_handler():
    global total_stop_time
    global stop_on_whole_second_time
    global is_started
    if is_started == True:
        is_started == False
        timer.stop()
        total_stop_time += 1
        if current_time % 10 == 0:
            stop_on_whole_second_time += 1
    
def reset_handler():
    global is_started
    global current_time
    global total_stop_time
    global stop_on_whole_second_time
    timer.stop()
    current_time = 0
    timer.start()
    is_started = True
    total_stop_time = 0
    stop_on_whole_second_time = 0

# define event handler for timer with 0.1 sec interval
def timer_handler():
    global current_time
    current_time += 1
    #print current_time

# define draw handler
def draw_handler(canvas):
    reflexes = (str(stop_on_whole_second_time) + '/' + 
               str(total_stop_time))
    canvas.draw_text(format(current_time), (110, 150), 30, 'Red')
    canvas.draw_text(reflexes, (260, 15), 20, 'Yellow')
    
# create frame
frame = simplegui.create_frame("Stopwatch", 300, 300)

# register event handlers
timer = simplegui.create_timer(100, timer_handler)
frame.set_draw_handler(draw_handler)
start_button = frame.add_button('Start', start_handler)
stop_button = frame.add_button('Stop', stop_handler)
reset_button = frame.add_button('Reset', reset_handler)

# start frame
frame.start()

# Please remember to review the grading rubric
