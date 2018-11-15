import tkinter as tk
import numpy as np

maxC = 5
maxR = 4
goalC = 4
goalR = 4
startC = 0
startR = 0

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
		return ["S" ,"U", "R", "D", "L"]


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

def playerTransition(goalState, currentState, action):
	#borders
	if ((currentState.myC == 0 and action == "L") or (currentState.myC == maxC and action == "R") or (currentState.myR == 0 and action == "U") or (currentState.myR == maxR and action == "D")):
		return 0.0

	if (currentState.myC == currentState.tC and currentState.myR == currentState.tR and action != "S"):
		return 0.0

	if (action == "L" and (goalState.myC != currentState.myC-1 or goalState.myR != currentState.myR)):
		return 0.0
	if (action == "R" and (goalState.myC != currentState.myC+1 or goalState.myR != currentState.myR)):
		return 0.0
	if (action == "U" and (goalState.myR != currentState.myR-1 or goalState.myC != currentState.myC)):
		return 0.0
	if (action == "D" and (goalState.myR != currentState.myR+1 or goalState.myC != currentState.myC)):
		return 0.0
	if (action == "S" and (goalState.myR != currentState.myR or goalState.myC != currentState.myC)):
		return 0.0

	if (action in getWall(currentState.myR, currentState.myC)):
		return 0.0

	return 1.0

def minotaurTransition(goalState, currentState, action):
	#if (not(goalState.tC-1 == currentState.tC or goalState.tC+1 == currentState.tC or goalState.tR-1 == currentState.tR or goalState.tR+1 == currentState.tR)):
	#	return 0

	if (abs(goalState.tC-currentState.tC) + abs(goalState.tR-currentState.tR) != 1):
		return 0.0

	if (currentState.myC == currentState.tC and currentState.myR == currentState.tR):
		if (goalState.tR == currentState.tR and goalState.tC == currentState.tC):
			return 1.0

	moves = 0.0
	if (currentState.tC > 0):
		moves+=1.0
	if (currentState.tC < maxC):
		moves+=1.0
	if (currentState.tR > 0):
		moves+=1.0
	if (currentState.tR < maxR):
		moves+=1.0

	return 1.0/moves

def getRewardAtState(rewardState, action):
	if(rewardState.tC == rewardState.myC and rewardState.tR == rewardState.myR):
		return -1.0
	if(rewardState.myC == goalC and rewardState.myR == goalR):
		return 1.0
	return 0.0

def initValueState(states):
	for mc in range(maxC + 1):
		for mr in range(maxR + 1):
			for tc in range(maxC + 1):
				for tr in range(maxR + 1):
					states[mc][mr][tc][tr] = max([getRewardAtState(State(mc,mr,tc,tr), a) for a in Action.getAllActions()])

def getProbability(goalState, currentState, action):
	return playerTransition(goalState, currentState, action) * minotaurTransition(goalState, currentState, action)

def getExpectedReward(state, action, valState):
	accumulate = 0.0
	for mc in range(maxC + 1):
		for mr in range(maxR + 1):
			for tc in range(maxC + 1):
				for tr in range(maxR + 1):
					accumulate += getProbability(State(mc,mr,tc,tr), state, action)*valState[mc][mr][tc][tr]
	return accumulate

def solveBellman(T, valState, valStatePrev, debugValState):
	pi = np.zeros((maxC+1,maxR+1,maxC+1,maxR+1), dtype=np.int8)
	for t in range(T, 0, -1):
		print(t)
		for mc in range(maxC + 1):
			for mr in range(maxR + 1):
				for tc in range(maxC + 1):
					for tr in range(maxR + 1):
						#probSum = 0.0
						#global minProbSUm
						state = State(mc,mr,tc,tr)
						best = float("-inf")
						actions = Action.getAllActions()
						for i in range(len(actions)):
							a = actions[i]
							value = getRewardAtState(state, a) + getExpectedReward(state, a, valState)
							#for mc_ in range(maxC + 1):
							#	for mr_ in range(maxR + 1):
							#		for tc_ in range(maxC + 1):
							#			for tr_ in range(maxR + 1):		
							#				probSum += getProbability(State(mc_,mr_,tc_,tr_), state, a)
							if value > best:
								best = value
								valStatePrev[mc][mr][tc][tr] = best
								pi[mc][mr][tc][tr] = i
						#minProbSUm = min(minProbSUm, probSum)
		#valState = valStatePrev.copy()
		copy(valState, valStatePrev)
		valStateCopy = np.zeros((maxC+1,maxR+1,maxC+1,maxR+1))
		copy(valStateCopy, valState)
		debugValState.append(valStateCopy)
	return pi

def copy(take, give):
	for mc in range(maxC + 1):
		for mr in range(maxR + 1):
			for tc in range(maxC + 1):
				for tr in range(maxR + 1):
					take[mc][mr][tc][tr] = give[mc][mr][tc][tr]


def create_grid(event=None):
    w = c.winfo_width() # Get current width of canvas
    h = c.winfo_height() # Get current height of canvas
    c.delete('grid_line') # Will only remove the grid_line

    #print(state)
    #print(walls)


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
    		c.create_text((col)*colWidth+colWidth*0.5, (row)*rowWidth + rowWidth/2, text="{:.1f}".format(debugValState[deIndex][col, row, 5, 0]), font=("Helvetica", colWidth//4), tag='grid_line')
    		#text="{:.1f}".format(valState[col, row, 5-1, 0])
    		#text=Action.getAllActions()[pi[col,row, 5, 0]]

    c.create_text((globalState.myC)*colWidth+colWidth*0.33, (globalState.myR)*rowWidth + rowWidth/2, text=u'\u263a', font=("Helvetica", colWidth//4), tag='grid_line')
    c.create_text((globalState.tC)*colWidth+colWidth*0.66, (globalState.tR)*rowWidth + rowWidth/2, text=u'\u2620', font=("Helvetica", colWidth//4), tag='grid_line')

def changeDebug(val):
	global deIndex
	deIndex += val
	deIndex = deIndex % len(debugValState)
	print("index", deIndex)
	create_grid()


globalState = State(startC,startR, 5, 0)
walls = getWalls()

valState = np.zeros((maxC+1,maxR+1,maxC+1,maxR+1))
valStatePrev = np.zeros((maxC+1,maxR+1,maxC+1,maxR+1))

initValueState(valState)

debugValState = []
deIndex = 0
minProbSUm = 99999999.0

pi = solveBellman(11, valState, valStatePrev, debugValState)

#print(minProbSUm)

root = tk.Tk()

c = tk.Canvas(root, height=500, width=500, bg='white')
c.pack(fill=tk.BOTH, expand=True)

c.bind('<Configure>', create_grid)

c.bind_all('<Left>', lambda e,val = -1: changeDebug(val))
c.bind_all('<Right>', lambda e,val = 1: changeDebug(val))

#root.after(5000,create_grid)
root.mainloop()