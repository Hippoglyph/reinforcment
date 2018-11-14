import tkinter as tk
#import numpy as np

maxC = 5
maxR = 4

class State:
	def __init__(self, myC,myR,tC,tR):
		self.myC = myC
		self.myR = myR
		self.tC = tC
		self.tR = tR

	def posEquals(self, r,c):
		return self.myC == c and self.myR == r

	def getInitState():
		return State(0,0,4,4)

class Action:
	def __init__(a):
		self.a = a

	def getAllActions():
		return ["U", "R", "D", "L", "S"]


def getWalls():
	return [[getWall(i,j) for j in range(maxC + 1)] for i in range(maxR + 1)]

def getWall(r,c):

	#Wall 1
	if (r == 0 and c == 1):
		return ["R"]
	if (r == 1 and c == 1):
		return ["R"]
	if (r == 2 and c == 1):
		return ["R"]
	if (r == 0 and c == 2):
		return ["L"]
	if (r == 1 and c == 2):
		return ["L"]
	if (r == 2 and c == 2):
		return ["L"]

	#Wall 2
	if (r == 1 and c == 3):
		return ["R"]
	if (r == 2 and c == 3):
		return ["R"]
	if (r == 1 and c == 4):
		return ["L", "D"]
	if (r == 2 and c == 4):
		return ["L", "U"]
	if (r == 2 and c == 5):
		return ["U"]
	if (r == 1 and c == 5):
		return ["D"]

	#Wall 3
	if (r == 3 and c == 1):
		return ["D"]
	if (r == 4 and c == 1):
		return ["U"]
	if (r == 3 and c == 2):
		return ["D"]
	if (r == 4 and c == 2):
		return ["U"]
	if (r == 3 and c == 3):
		return ["D"]
	if (r == 4 and c == 3):
		return ["U", "R"]
	if (r == 3 and c == 4):
		return ["D"]
	if (r == 4 and c == 4):
		return ["U", "L"]

	return []



def playerTransition(state, action):
	#borders
	if ((state.myC == 0 and action == "L") or (state.myC == maxC and action == "R") or (state.myR == 0 and action == "U") or (state.myR == maxR and action == "D")):
		return 0

	#Wall 1
	if ((state.posEquals(0,1) and action == "R") or (state.posEquals(0,2) and action == "L")):
		return 0
	if ((state.posEquals(1,1) and action == "R") or (state.posEquals(1,2) and action == "L")):
		return 0
	if ((state.posEquals(2,1) and action == "R") or (state.posEquals(2,2) and action == "L")):
		return 0

	#Wall 2
	if ((state.posEquals(1,3) and action == "R") or (state.posEquals(1,4) and action == "L")):
		return 0
	if ((state.posEquals(2,3) and action == "R") or (state.posEquals(2,4) and action == "L")):
		return 0
	if ((state.posEquals(2,4) and action == "D") or (state.posEquals(3,4) and action == "U")):
		return 0
	if ((state.posEquals(2,5) and action == "D") or (state.posEquals(3,5) and action == "U")):
		return 0

	#Wall 3
	if ((state.posEquals(4,1) and action == "D") or (state.posEquals(5,1) and action == "U")):
		return 0
	if ((state.posEquals(4,2) and action == "D") or (state.posEquals(5,2) and action == "U")):
		return 0
	if ((state.posEquals(4,3) and action == "D") or (state.posEquals(5,3) and action == "U")):
		return 0
	if ((state.posEquals(4,4) and action == "D") or (state.posEquals(5,4) and action == "U")):
		return 0
	if ((state.posEquals(5,3) and action == "R") or (state.posEquals(5,4) and action == "L")):
		return 0	

	return 1

def minotaurTransition(state, action):
	#borders
	if ((state.tC == 0 and action == "L") or (state.tC == maxC and action == "R") or (state.tR == 0 and action == "U") or (state.tR == maxR and action == "D")):
		return 0

	moves = 0
	if (state.tC > 0):
		moves+=1
	if (state.tC < maxC):
		moves+=1
	if (state.tR > 0):
		moves+=1
	if (state.tR < maxR):
		moves+=1

	return 1/moves


def create_grid(event=None, state=State.getInitState(), walls = getWalls()):
    w = c.winfo_width() # Get current width of canvas
    h = c.winfo_height() # Get current height of canvas
    c.delete('grid_line') # Will only remove the grid_line

    colWidth = w//(maxC + 1)
    rowWidth = h//(maxR + 1)
    # Creates all vertical lines at intevals of 100
    for i in range(0, w, colWidth):
        c.create_line([(i, 0), (i, h)], tag='grid_line', fill="grey")

    # Creates all horizontal lines at intevals of 100
    for i in range(0, h, rowWidth):
        c.create_line([(0, i), (w, i)], tag='grid_line', fill="grey")

    for row in range(0, maxR + 1):
    	for col in range(0, maxC + 1):
    		if "L" in walls[row][col]:
    			c.create_line([(col*colWidth + 1, row*rowWidth), (col*colWidth + 1, (row+1)*rowWidth)], tag='grid_line', fill="black", width=1)
    		if "R" in walls[row][col]:
    			c.create_line([((col + 1)*colWidth - 1, row*rowWidth), ((col+1)*colWidth - 1, (row+1)*rowWidth)], tag='grid_line', fill="black", width=1)
    		if "D" in walls[row][col]:
    			c.create_line([(col*colWidth, (row + 1)*rowWidth - 1), ((col+1)*colWidth, (row+1)*rowWidth - 1)], tag='grid_line', fill="black", width=1)
    		if "U" in walls[row][col]:
    			c.create_line([(col*colWidth, row*rowWidth + 1), ((col+1)*colWidth, row*rowWidth + 1)], tag='grid_line', fill="black", width=1)


initState = State(0,0, 4, 4)
walls = getWalls()

root = tk.Tk()

c = tk.Canvas(root, height=500, width=500, bg='white')
c.pack(fill=tk.BOTH, expand=True)

c.bind('<Configure>', lambda inState = initState, walls = walls : create_grid(inState, walls))

root.mainloop()