import tkinter as tk
import numpy as np
import random
import matplotlib.pyplot as plt

class State:
	def __init__(self, rR,rC,pR,pC):
		self.rC = rC
		self.rR = rR
		self.pC = pC
		self.pR = pR

	def isTaken(self):
		if (self.rC == self.pC and self.rR == self.pR):
			return True
		return False

	def isAtBank(self):
		if self.rR == bank[0] and self.rC == bank[1]:
			return True
		return False

	def isInitState(self):
		if self.rR == rS[0] and self.rC == rS[1] and self.pR == pS[0] and self.pC == pS[1]:
			return True
		return False

	def isSameState(self, state):
		if self.rR == state.rR and self.rC == state.rC and self.pR == state.pR and self.pC == state.pC:
			return True
		return False

def getReward(state, action):
	if state.isTaken():
		return -10.0
	if state.isAtBank() and action == "S":
		return 1.0
	return 0.0

def playerTransition(goalState, state, action):

	#TAKEN??!?!?!?
	if state.isTaken():
		if goalState.isInitState():
			return 1.0
		else:
			return 0.0
	else:
		#borders
		if ((state.rC == 0 and action == "L") or (state.rC == maxC and action == "R") or (state.rR == 0 and action == "U") or (state.rR == maxR and action == "D")):
			if state.isSameState(goalState):
				return 1.0
			else:
				return 0.0

		if (action == "L" and not(goalState.rC == state.rC-1 and goalState.rR == state.rR)):
			return 0.0
		if (action == "R" and not(goalState.rC == state.rC+1 and goalState.rR == state.rR)):
			return 0.0
		if (action == "U" and not(goalState.rR == state.rR-1 and goalState.rC == state.rC)):
			return 0.0
		if (action == "D" and not(goalState.rR == state.rR+1 and goalState.rC == state.rC)):
			return 0.0
		if (action == "S" and not(goalState.rR == state.rR and goalState.rC == state.rC)):
			return 0.0
	return 1.0

def policeTransitions(goalState, state, action):
	if state.isTaken():
		if goalState.isInitState():
			return 1.0
		else:
			return 0.0
	else:
		if abs(goalState.pC-state.pC) + abs(goalState.pR-state.pR) != 1:
			return 0.0

		moves = 0.0
		if (state.pC > 0):
			moves+=1.0
		if (state.pC < maxC):
			moves+=1.0
		if (state.pR > 0):
			moves+=1.0
		if (state.pR < maxR):
			moves+=1.0

		return 1.0/moves
	return 0

def getTransitionProbability(goalState, state, action):
	return playerTransition(goalState, state, action) * policeTransitions(goalState, state, action)

def getExpectedReward(state, action, valState):
	accumulate = 0.0
	for rR in range(maxR + 1):
		for rC in range(maxC + 1):
			for pR in range(maxR + 1):
				for pC in range(maxC + 1):
					goalState = State(rR,rC,pR,pC)
					if goalState.isInitState() or ((abs(rC-state.rC) + abs(rR-state.rR) <= 1) and (abs(pC-state.pC) + abs(pR-state.pR) <= 1)):
						accumulate += getTransitionProbability(goalState, state, action)*valState[rR,rC,pR,pC]
	return accumulate

def solveHoward(valState, pi, lam):
	#lam = 0.95
	piPrev = np.zeros((maxR+1,maxC+1,maxR+1,maxC+1), dtype=np.int8)
	valStatePrev = np.zeros((maxR+1,maxC+1,maxR+1,maxC+1), dtype=np.double)
	counter = 0
	while True:
		print(counter)
		counter+=1
		for rR in range(maxR + 1):
			for rC in range(maxC + 1):
				for pR in range(maxR + 1):
					for pC in range(maxC + 1):
						state = State(rR,rC,pR,pC)
						a = actions[pi[rR,rC,pR,pC]]
						valState[rR,rC,pR,pC] = getReward(state, a) + lam*getExpectedReward(state, a, valStatePrev)
		for rR in range(maxR + 1):
			for rC in range(maxC + 1):
				for pR in range(maxR + 1):
					for pC in range(maxC + 1):
						state = State(rR,rC,pR,pC)
						best = float("-inf")
						for i in range(len(actions)):
							a = actions[i]
							value = getReward(state, a) + lam*getExpectedReward(state, a, valState)
							if value > best:
								best = value
								pi[rR,rC,pR,pC] = i

		if ((pi == piPrev).all()):
			break

		copy(piPrev, pi)
		copy(valStatePrev, valState)

def copy(take, give):
	for rR in range(maxR + 1):
		for rC in range(maxC + 1):
			for pR in range(maxR + 1):
				for pC in range(maxC + 1):
					take[rR,rC,pR,pC] = give[rR,rC,pR,pC]

def create_grid(pi, valState, rR, rC, pR, pC):
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
    		if (row == bank[0] and col == bank[1]):
    			c.create_text((col)*colWidth+colWidth*0.85, (row)*rowWidth + rowWidth*0.75, text=u'\u2721', font=("Helvetica", colWidth//6), tag='grid_line')
    		c.create_text((col)*colWidth+colWidth*0.5, (row)*rowWidth + rowWidth*0.33, text=actions[pi[row,col, pR, pC]], font=("Helvetica", colWidth//5), tag='grid_line')
    		c.create_text((col)*colWidth+colWidth*0.5, (row)*rowWidth + rowWidth*0.66, text="{:.2f}".format(valState[row, col, pR, pC]), font=("Helvetica", colWidth//6), tag='grid_line')

    c.create_text((pC)*colWidth+colWidth*0.75, (pR)*rowWidth + rowWidth*0.33, text=u'\u2620', font=("Helvetica", colWidth//4), tag='grid_line')
    c.create_text((rC)*colWidth+colWidth*0.25, (rR)*rowWidth + rowWidth*0.33, text=u'\u263a', font=("Helvetica", colWidth//4), tag='grid_line')

def policeMoveRollOut(rR, rC, pR, pC):
	state = State(rR, rC, pR, pC)

	if state.isTaken():
		return (pS[0], pS[1])

	goalStateUp = State(rR, rC, max(pR-1, 0), pC)
	goalStateDown = State(rR, rC, min(pR+1, maxR), pC)
	goalStateLeft = State(rR, rC, pR , max(pC-1, 0))
	goalStateRight = State(rR, rC, pR , min(pC+1, maxC))

	trans = [policeTransitions(goalStateUp, state, "U"), policeTransitions(goalStateDown, state, "D"), policeTransitions(goalStateLeft, state, "L"), policeTransitions(goalStateRight, state, "R")]

	cumSum = np.cumsum(trans)

	val = random.random()

	for i in range(len(cumSum)):
		if cumSum[i] > val:
			if i == 0:
				return (pR - 1, pC)
			if i == 1:
				return (pR + 1, pC)
			if i == 2:
				return (pR, pC - 1)
			if i == 3:
				return (pR, pC + 1)
	return (pR, pC)

def robberMoveRollOut(pi, rR, rC, pR, pC):
	state = State(rR, rC, pR, pC)
	if state.isTaken():
		return (rS[0], rS[1])

	a = actions[pi[rR, rC, pR, pC]]
	if a == "L":
		rC -= 1
		rC = max(rC, 0)
	elif a == "R":
		rC += 1
		rC = min(maxC, rC)
	elif a == "U":
		rR -= 1
		rR = max(rR, 0)
	elif a == "D":
		rR += 1
		rR = min(maxR, rR)
	return (rR, rC)

def advanceGame(pi):
	global gameRR
	global gameRC
	global gamePR
	global gamePC

	newRR, newRC = robberMoveRollOut(pi, gameRR, gameRC, gamePR, gamePC)
	gamePR, gamePC = policeMoveRollOut(gameRR, gameRC, gamePR, gamePC)
	gameRR = newRR	
	gameRC = newRC
	create_grid(pi, valState, gameRR, gameRC, gamePR, gamePC)

bank = (1,1)

actions = ["S" ,"U", "R", "D", "L"]

pS = (3,3)

rS = (0,0)

maxR = 3
maxC = 3

pi = np.zeros((maxR+1,maxC+1,maxR+1,maxC+1), dtype=np.int8)
valState = np.zeros((maxR+1,maxC+1,maxR+1,maxC+1))
solveHoward(valState,pi, 0.8)

gameRR = rS[0]
gameRC = rS[1]
gamePR = pS[0]
gamePC = pS[1]

root = tk.Tk()

c = tk.Canvas(root, height=250, width=500, bg='white')
c.pack(fill=tk.BOTH, expand=True)

c.bind('<Configure>', lambda e: create_grid(pi, valState, rS[0], rS[1], pS[0], pS[1]))

c.bind_all('<Return>', lambda e: advanceGame(pi))

#c.bind_all('<Left>', lambda e,val = -1: changeDebug(val))
#c.bind_all('<Right>', lambda e,val = 1: changeDebug(val))

#c.bind_all('<Left>', lambda e,rightMove = -1, leftMove = 0: moveMino(rightMove, leftMove))
#c.bind_all('<Right>', lambda e,rightMove = 1, leftMove = 0: moveMino(rightMove, leftMove))
#c.bind_all('<Up>', lambda e,rightMove = 0, leftMove = -1: moveMino(rightMove, leftMove))
#c.bind_all('<Down>', lambda e,rightMove = 0, leftMove = 1: moveMino(rightMove, leftMove))

#c.bind_all('r', lambda e: resetGame())

root.mainloop()