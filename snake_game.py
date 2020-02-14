import random
from curses import wrapper
import curses
from curses import textpad

def Put_Score(stdscr, score):
	sh, sw = stdscr.getmaxyx()
	score_txt = "Score : {}".format(score)
	stdscr.addstr(0, sw//2 - len(score_txt)//2, score_txt)
	stdscr.refresh()

def initilize(stdscr):
	curses.curs_set(0)
	stdscr.nodelay(1)
	stdscr.timeout(150)
	sh, sw = stdscr.getmaxyx()
	score = 0
	box = [[3, 3], [sh - 3, sw - 3]]
    # Creating the boundry for the game
	textpad.rectangle(stdscr, box[0][0], box[0][1], box[1][0], box[1][1])
    # create the snake body
	snake = [[sh//2, sw//2+1], [sh//2, sw//2], [sh//2, sw//2-1]]
	direction = curses.KEY_RIGHT
	for y, x in snake:
		stdscr.addch(y, x, curses.ACS_ULCORNER)
    # setting the food for the first time
	food = create_food(snake, box)
	stdscr.addch(food[0], food[1], curses.ACS_PI)
	Put_Score(stdscr, score)
	return snake, box, direction, food, score, sh, sw

def create_food(snake, box):
	food = None
	while food is None:
		food = [random.randint(box[0][0]+1,box[1][0]-1), random.randint(box[0][1]+1,box[1][1]+1)]
		if food in snake:
			food = None
	return food

def game_loop(stdscr, snake, box, direction, food, score, sh, sw):
	while 1:
		key = stdscr.getch()
		if key in [curses.KEY_RIGHT, curses.KEY_LEFT, curses.KEY_UP, curses.KEY_DOWN]:
			direction = key
        # creating the new head
		head = snake[0]
		if direction == curses.KEY_RIGHT:
			new_head = [head[0], head[1] + 1]
		elif direction == curses.KEY_LEFT:
			new_head = [head[0], head[1] - 1]
		elif direction == curses.KEY_UP:
			new_head = [head[0] - 1, head[1]]
		elif direction == curses.KEY_DOWN:
			new_head = [head[0] + 1, head[1]]
            
        # insert new_head to 0th position
		snake.insert(0, new_head)
		stdscr.addch(new_head[0], new_head[1], curses.ACS_ULCORNER)

        # check if snake ate the food
		if snake[0] == food:
			food = create_food(snake, box)
			stdscr.addch(food[0], food[1], curses.ACS_PI)
			score = score + 1
			Put_Score(stdscr, score)
		else:
			stdscr.addstr(snake[-1][0], snake[-1][1], ' ')
			snake.pop()
        
        # check game over conditions
		if(snake[0][0] in [box[0][0], box[1][0]] or snake[0][1] in [box[0][1], box[1][1]] or snake[0] in snake[1:]):
			msg = "Game Over"
			stdscr.addstr(sh//2, sw//2 - len(msg)//2, msg)
			stdscr.nodelay(0)
			stdscr.getch() 
			break
		stdscr.refresh()

def main(stdscr):
	snake, box, direction, food, score, sh, sw = initilize(stdscr)
	game_loop(stdscr, snake, box, direction, food, score, sh, sw)

wrapper(main)