import pygame
import time

pygame.init()
display_width = 1350
display_height = 900
gameDisplay = pygame.display.set_mode((display_width,display_height))
pygame.display.set_caption('The Trial')
FONT = pygame.font.SysFont('Comic Sans MS', 32)
clock = pygame.time.Clock()
crashed = False
current_button = 0
white = (255,255,255)
black = (0,0,0)
x =  (display_width * 0.45)
y = (display_height * 0.8)
initial_state = True
Up = False;
Down = False;
Left = False;
Right = False;

TRIANGLE = 0
SQUARE = 1
CIRCLE = 2
DIAMOND = 3
TRIANGLE2 = 4
SQUARE2 = 5
CIRCLE2 = 6
DIAMOND2 = 7

pictures = {
				TRIANGLE : pygame.image.load('triangle.png'),
				SQUARE : pygame.image.load('square.png'),
				CIRCLE : pygame.image.load('circle.png'),
				DIAMOND : pygame.image.load('diamond.png'),
				TRIANGLE2 : pygame.image.load('triangle2.png'),
				SQUARE2 : pygame.image.load('square2.png'),
				CIRCLE2 : pygame.image.load('circle2.png'),
				DIAMOND2 : pygame.image.load('diamond2.png')
			}

TILESIZE = 160
MAPWIDTH = 8
MAPHEIGHT = 5
currentLoc = (0,0)
button_map = [8,5]

tilemap = [
			[TRIANGLE, CIRCLE, SQUARE, TRIANGLE, TRIANGLE, SQUARE, SQUARE, CIRCLE],
			[TRIANGLE, DIAMOND, CIRCLE, CIRCLE, DIAMOND, TRIANGLE, CIRCLE, TRIANGLE],
			[DIAMOND, CIRCLE, DIAMOND, TRIANGLE, SQUARE, SQUARE, CIRCLE, SQUARE],
			[CIRCLE, SQUARE, SQUARE, SQUARE, TRIANGLE, DIAMOND, DIAMOND, CIRCLE],
			[DIAMOND, SQUARE, TRIANGLE, SQUARE, CIRCLE, CIRCLE, TRIANGLE, DIAMOND]
			]

#make the button class. 
class Button:
	def __init__(self, image_number, is_clickable, x, y, row, column):
		self.image_number =image_number
		self.click_image = pictures[image_number]
		self.unclick_image = pictures[image_number+4]
		#self.Toggle = False
		self.is_clickable = is_clickable
		self.row = row
		self.column = column
		self.x = x
		self.y = y
		self.direction = "None"
		self.width, self.height = pictures[image_number].get_rect().size
		#check if mouse click location is within a button's image
	def within_rect(self,xpos,ypos):
		#print("checking between Xs: ", self.x, " & ", (self.x+self.width), "and between Ys: ", self.y, " & ", (self.y +self.height))
		if self.x+self.height > xpos > self.x and self.y < ypos < self.y+self.width:
			return True
		else:
			return False
	#switch the button's image to the blue/black version, by adding or subtracting 4. draw_buttons display picture based on number.
	def Toggle(self):
		if self.image_number >= 4:
			self.image_number -= 4 
		else:
			self.image_number +=4

#make a 2D array of buttons
array_of_buttons = [[0 for x in range(MAPWIDTH)] for y in range(MAPHEIGHT)]
for column in range(MAPWIDTH):
	for row in range(MAPHEIGHT):
		#print ("column = ", column, ", row = ", row, ", image", tilemap[row][column])
		#print (column, row)
		array_of_buttons[row][column] = Button(tilemap[row][column], False, column*TILESIZE, row*TILESIZE + 100, row, column)

#draw button based on image number. 0-3 = black, 4-7 = blue
def draw_buttons(Button):
	b = Button
	#print (b.x, " , ",b.y, " , ", b.click_image)
	gameDisplay.blit(pictures[b.image_number], (b.x, b.y))

def text_objects(text, font):
    textSurface = font.render(text, True, black)
    return textSurface, textSurface.get_rect()

#set up initial stuff
gameDisplay.fill(white)
largeText = pygame.font.Font('augustus.ttf', 105)
TextSurf, TextRect = text_objects("THE TRIAL", largeText)
TextRect.center = (650,55)
gameDisplay.blit(TextSurf, TextRect)
pygame.mouse.set_cursor(*pygame.cursors.arrow)


#initialize display of buttons
for column in range(MAPWIDTH):
	for row in range (MAPHEIGHT):
		draw_buttons(array_of_buttons[row][column])
		#print (array_of_buttons[row][column].column, array_of_buttons[row][column].row)

#main logic
#set all buttons in last row to be clickable, as initial game state. 
#change pointer logic to only be a "diamond" when over a clickable button, an arrow over nothing, and an X over non-clickable buttons
#when a clickable button is clicked for the first time, set the current position to that button location.
#set buttons around it, within riddle logic, to clickable.
#on click, store direction
#execute direction, toggling buttons

#function for setting initial state, regarding clickability and images, and initial state bool
def initialize_buttons():
	initial_state = True
	for column in range(MAPWIDTH):
		for row in range (MAPHEIGHT):
			b = array_of_buttons[row][column]
			if b.image_number >= 4:
				b.Toggle()
				draw_buttons(b)
			if row == 4:
				b.is_clickable = True
			else:
				b.is_clickable = False

def select_first_button(Button):
	for column in range(MAPWIDTH):
		for row in range (MAPHEIGHT):
			d = array_of_buttons[row][column]
			d.is_clickable = False
	return (Button.column, Button.row)

#most logicy function. must contain logic for finding buttons surrounding current button that are selectable i.e. do not have a direction yet, and are within the bounds of the game
def find_clickable_buttons(currentLoc):
	#print("###")
	#print(currentLoc)
	#print(array_of_buttons[currentLoc[1]][currentLoc[0]].column, array_of_buttons[currentLoc[1]][currentLoc[0]].row)
	#print("###")
	#currentLoc is tuple
	#logic: is there a button is each direction? check currentLoc vs bounds of the map width/height, and then check if that button has a direction set
	#if the current button's direction is equal to any of the surrounding buttons' directions, then that surrounding button is not clickable
	#left of current
	#print ("current location: ", currentLoc)
	if currentLoc[0]-1 >= 0 and not Left: 
		if array_of_buttons[currentLoc[1]][currentLoc[0]-1].image_number < 4:
			array_of_buttons[currentLoc[1]][currentLoc[0]-1].is_clickable = True
			print ("left is clickable")
		else: 
			print("left has already been selected :", array_of_buttons[currentLoc[0]-1][currentLoc[1]].image_number)
	else:
		print ("left out of range: ", currentLoc[0]-1, " vs ", 0)

	#right	
	if currentLoc[0]+1 < MAPWIDTH and not Right: 
		#print ("check")
		#print (currentLoc[0]+1, " ", MAPWIDTH, " , ", Right)
		if array_of_buttons[currentLoc[1]][currentLoc[0]+1].image_number < 4:
			array_of_buttons[currentLoc[1]][currentLoc[0]+1].is_clickable = True
			print ("right is clickable")
		else: 
			print("right has already been selected :", array_of_buttons[currentLoc[0]+1][currentLoc[1]].image_number)
	else:
		print ("Right out of range: ", currentLoc[0]+1, " is not < than ", MAPWIDTH)


	#up	
	if currentLoc[1]-1 >= 0 and not Up: 
		if array_of_buttons[currentLoc[1]-1][currentLoc[0]].image_number < 4:
			array_of_buttons[currentLoc[1]-1][currentLoc[0]].is_clickable = True

	#down	
	if currentLoc[1]+1 < MAPHEIGHT and not Down:
		if array_of_buttons[currentLoc[1]+1][currentLoc[0]].image_number < 4:
			array_of_buttons[currentLoc[1]+1][currentLoc[0]].is_clickable = True

	
def reset_clickability():
	for column in range(MAPWIDTH):
		for row in range (MAPHEIGHT):
			d = array_of_buttons[row][column]
			d.is_clickable = False

#store direction in each button
def set_direction_on_buttons(button_array, direction, image_number):
	#print ("setting ", image_number, " button to", direction)
	for column in range(MAPWIDTH):
		for row in range (MAPHEIGHT):
			d = array_of_buttons[row][column]
			if d.image_number == image_number or d.image_number == image_number+4:
				d.direction = direction
				#print ("setting a ", image_number, " button to", direction, ". location: ", d.column, d.row)

def check_within_bounds(x, y):
	if 0 <= x < MAPWIDTH and 0 <= y <MAPHEIGHT:
		return True
	else:
		return False

#print(array_of_buttons[4][7].x, array_of_buttons[4][7].y, array_of_buttons[4][7].image_number, array_of_buttons[4][7].column, array_of_buttons[4][7].row)
#how to do? not recursive, but execute this function in a loop until it no longer can be executed. do this loop in the main loop
#also needs to kick the player back to initial if it fails
#just do all the necessary stuff to the current button input, and then return the next button in that direction. also needs to toggle, redraw the button in that direction.
def follow_direction(button):
	#time.sleep(1)
	#print("test")
	#print ("left: ", Left, " , right: ", Right, " , up: ", Up, " , down: ", Down)
	#print ("follow_direction() location: ", button.column, button.row)
	#print (button.direction, button.x, button.y)
	#direction is already set, and the current location is still pointing to button parameter by this point
	#button input starts out as the button clicked.
	if button.direction != "None":
		#print("test2. button.direction is not None")
		if button.direction == "Left" and check_within_bounds(button.column - 1, button.row):
			#print ("checking left")
			currentLoc = (button.column, button.row)
			#array_of_buttons[button.column-1][button.row].Toggle()
			#draw_buttons(array_of_buttons[button.column-1][button.row])
			return array_of_buttons[button.row][button.column-1]

		elif button.direction == "Right" and check_within_bounds(button.column + 1, button.row):
			#print ("checking right")
			currentLoc = (button.column, button.row)
			#array_of_buttons[button.row][button.column+1].Toggle()
			#draw_buttons(array_of_buttons[button.row][button.column+1])
			return array_of_buttons[button.row][button.column +1]

		elif button.direction == "Up" and check_within_bounds(button.column, button.row -1):
			#print ("checking up")
			currentLoc = (button.column , button.row)
			#print (currentLoc, "in follow_direction")
			#print (button.column, button.row, "in follow_direction. current button")
			#array_of_buttons[button.row-1][button.column].Toggle()
			#print ("toggled button with column: ", button.column, "and row: ",button.row)
			#draw_buttons(array_of_buttons[button.row-1][button.column])
			#print ("return a button with image_number: ", array_of_buttons[button.column][button.row -1].image_number, ", column:", array_of_buttons[button.column][button.row -1].column, ", row: ", array_of_buttons[button.column][button.row -1].row)
			return array_of_buttons[button.row -1][button.column]

		elif button.direction == "Down" and check_within_bounds(button.column , button.row + 1):
			#print ("checking down")
			currentLoc = (button.column, button.row)
			#array_of_buttons[button.row+1][button.column].Toggle()
			#draw_buttons(array_of_buttons[button.row+1][button.column])
			return array_of_buttons[button.row +1][button.column]
		#win con
		elif button.direction == "Up" and button.row == 0:
			#print("won the game!")
			return "WIN"

		#else:
			#print ("failed to find")
	else:
		return button

	#return new button location. and set new currentLoc

#currentLoc[1] = y. 2d lists are indexed in reverse order


def paused():
	gameDisplay.fill(white)
	largeText = pygame.font.Font('augustus.ttf', 115)
	TextSurf, TextRect = text_objects("THE RETURN", largeText)
	TextRect.center = ((display_width/2),(display_height-800))
	gameDisplay.blit(TextSurf, TextRect)
	smallText = pygame.font.Font('augustus.ttf', 40)
	TextSurf, TextRect = text_objects("Proper journies end where they began:", smallText)
	TextRect.center = ((display_width/2),(display_height-500))
	gameDisplay.blit(TextSurf, TextRect)
	smallerText = pygame.font.Font('augustus.ttf', 40)
	TextSurf, TextRect = text_objects("A gathering place for friends.", smallerText)
	TextRect.center = ((display_width/2),(display_height-400))
	gameDisplay.blit(TextSurf, TextRect)

	pause = True

	while pause:
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()
				quit()
                
        #gameDisplay.fill(white)
        

        #button("Continue",150,450,100,50,green,bright_green,unpause)
        #button("Quit",550,450,100,50,red,bright_red,quitgame)

		pygame.display.update()
		clock.tick(15)  


def main():
	global crashed
	global display_width
	global display_height
	global gameDisplay
	global clock
	global current_button
	global white
	global black
	global x 
	global y 
	global initial_state
	global Up
	global Down
	global Left
	global Right
	global MAPWIDTH
	global MAPHEIGHT
	global currentLoc
	global button_map
	initialize_buttons()
	Up = False
	Down = False
	Left = False
	Right = False
	set_direction_on_buttons(array_of_buttons, "None", 0)
	set_direction_on_buttons(array_of_buttons, "None", 1)
	set_direction_on_buttons(array_of_buttons, "None", 2)
	set_direction_on_buttons(array_of_buttons, "None", 3)
	currentLoc = (0,0)
	while not crashed:
		event = pygame.event.poll()
		if event.type == pygame.QUIT:
			crashed = True
		#if a button is clicked on, find out which button, toggle it, and redraw it. most logic happens here
		elif event.type == pygame.MOUSEBUTTONUP:
			pos = pygame.mouse.get_pos()
			for j in range (MAPWIDTH): #j = column
				for i in range (MAPHEIGHT): # i = row
					#print ("i:", j,"j: ", i)
					butt = array_of_buttons[i][j]
					if butt.within_rect(pos[0], pos[1]) and butt.is_clickable:
						#print (butt.column, butt.row)
						if initial_state:
							initial_state = False
							currentLoc = select_first_button(butt)
							reset_clickability()
							find_clickable_buttons(currentLoc)
							butt.Toggle()
							draw_buttons(butt)
							#print ("initial state done")
							#print ("initial button loc: ", currentLoc)
						else:
							#print ("mouse:", pos)
							#print ("rect:", butt.x, butt.x+butt.height, butt.y, butt.y+butt.width)
							#print (butt.column, butt.row)
							#print (butt.image_number)
							#print (currentLoc)
							#is_clickable already vets for clickability of button. don't need to do it again here. actually, maybe not true, since follow directions will be run in a loop.
							if currentLoc[0]-1 == j:
								Left = True
								set_direction_on_buttons(array_of_buttons, "Left", array_of_buttons[currentLoc[1]][currentLoc[0]].image_number-4)
								#print("LEFT!")
							elif currentLoc[0]+1 == j:
								Right = True
								set_direction_on_buttons(array_of_buttons, "Right", array_of_buttons[currentLoc[1]][currentLoc[0]].image_number-4)
								#print("RIGHT!")
							elif currentLoc[1]-1 == i:
								Up = True
								set_direction_on_buttons(array_of_buttons, "Up", array_of_buttons[currentLoc[1]][currentLoc[0]].image_number-4)
								#print("UP!")
							elif currentLoc[1]+1 == i:
								Down = True
								set_direction_on_buttons(array_of_buttons, "Down", array_of_buttons[currentLoc[1]][currentLoc[0]].image_number-4)
								#print("DOWN!")				

							#execute moving
							#print (currentLoc)
							#print ("butt location: ", butt.column, butt.row)	

							#if the latest button has a direction, follow that direction.

							#print (butt.direction)
							butt.Toggle()
							#print (butt.image_number)
							draw_buttons(butt)
							pygame.display.update()
							while butt.direction != "None":
								time.sleep(.3)

								#print("following...")
								butt_copy = butt
								butt = follow_direction(butt)
								#sometimes out of bounds will fuck up
								if (butt is None):
									main()
								if butt is "WIN":
									#print (butt)
									#print ("setting crashed to true")
									crashed = True
								if crashed == True:
									paused()
									#print (b.x, " , ",b.y, " , ", b.click_image)
									#gameDisplay.blit(pictures[b.image_number], (b.x, b.y))

  									#textSurface = font.render(text, True, black)
  									#gameDisplay.fill(white)
  									#largeText = pygame.font.Font('augustus.ttf', 105)
  									#TextSurf, TextRect = text_objects("THE REVELATION", largeText)
  									#TextRect.center = (650,55)
  									#gameDisplay.blit(TextSurf, TextRect)

								#print (butt.column, butt.row, butt.image_number)
								## if the next button in order is already selected, fail out
								if (butt.image_number >= 4):
									#print ("crash")
									main()
								elif(butt == butt_copy): #signifying the thing didn't move, meaning it's an out of bounds movement, reset
									#print ("out of bounds")
									main()
								butt.Toggle()
								draw_buttons(butt)
								pygame.display.update()
								#print (currentLoc, "while loop")
								#print (butt.column, butt.row)
							#butt.Toggle()
							#draw_buttons(butt)
							currentLoc = (butt.column, butt.row)
							#print (currentLoc)
							#current_button = array_of_buttons[i][j]
							reset_clickability()
							find_clickable_buttons(currentLoc)
							pygame.display.update()
							##if no clickable shapes, fail and reset
							click = 0
							for column in range(MAPWIDTH):
								for row in range (MAPHEIGHT):
									if (array_of_buttons[row][column].is_clickable):
										click += 1
							if (click < 1):
								#print ("no clickable shapes ", click)
								main()
							#current_button.Toggle()
							#draw_buttons(current_button)
							##if all buttons are donezo, and the game isn't complete, fail out and reset
							if (Up and Down and Left and Right):
								main()


		#set the mouse to a different cursor if it's over a button. will be discared later
		elif event.type == pygame.MOUSEMOTION:
			x,y = event.pos
			#print (x,y)
			mouse_on_button = False
			for k in range (MAPWIDTH):
				for l in range (MAPHEIGHT):
					if array_of_buttons[l][k].within_rect(x, y):
						mouse_on_button = True
						if array_of_buttons[l][k].is_clickable:
							pygame.mouse.set_cursor(*pygame.cursors.tri_left)
						else:
							pygame.mouse.set_cursor(*pygame.cursors.broken_x)
			if mouse_on_button == False:
				pygame.mouse.set_cursor(*pygame.cursors.arrow)

		pygame.display.update()
		clock.tick(30)

	pygame.quit()
	quit()

main()