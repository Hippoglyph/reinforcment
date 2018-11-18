import tkinter as tk
import numpy as np
import random
import matplotlib.pyplot as plt

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
	if (currentState.myC == currentState.tC and currentState.myR == currentState.tR):
		if (goalState.myR == currentState.myR and goalState.myC == currentState.myC):
			return 1.0
		else:
			return 0.0
	else:
		#borders
		if ((currentState.myC == 0 and action == "L") or (currentState.myC == maxC and action == "R") or (currentState.myR == 0 and action == "U") or (currentState.myR == maxR and action == "D")):
			if (goalState.myR == currentState.myR and goalState.myC == currentState.myC):
				return 1.0
			else:
				return 0.0

		if (action in getWall(currentState.myR, currentState.myC) and goalState.myR == currentState.myR and goalState.myC == currentState.myC):
			return 1.0

		if (action == "L" and not(goalState.myC == currentState.myC-1 and goalState.myR == currentState.myR)):
			return 0.0
		if (action == "R" and not(goalState.myC == currentState.myC+1 and goalState.myR == currentState.myR)):
			return 0.0
		if (action == "U" and not(goalState.myR == currentState.myR-1 and goalState.myC == currentState.myC)):
			return 0.0
		if (action == "D" and not(goalState.myR == currentState.myR+1 and goalState.myC == currentState.myC)):
			return 0.0
		if (action == "S" and not(goalState.myR == currentState.myR and goalState.myC == currentState.myC)):
			return 0.0

		if (action in getWall(currentState.myR, currentState.myC)):
			return 0.0

	return 1.0

def minotaurTransition(goalState, currentState, action):
	#if (not(goalState.tC-1 == currentState.tC or goalState.tC+1 == currentState.tC or goalState.tR-1 == currentState.tR or goalState.tR+1 == currentState.tR)):
	#	return 0

	

	if (currentState.myC == currentState.tC and currentState.myR == currentState.tR):
		if (goalState.tR == currentState.tR and goalState.tC == currentState.tC):
			return 1.0
	else:
		if (minotaurCanStay):
			if (abs(goalState.tC-currentState.tC) + abs(goalState.tR-currentState.tR) > 1):
				return 0.0
		elif (abs(goalState.tC-currentState.tC) + abs(goalState.tR-currentState.tR) != 1):
			return 0.0

		moves = 1.0 if minotaurCanStay else 0.0
		if (currentState.tC > 0):
			moves+=1.0
		if (currentState.tC < maxC):
			moves+=1.0
		if (currentState.tR > 0):
			moves+=1.0
		if (currentState.tR < maxR):
			moves+=1.0

		return 1.0/moves
	return 0.0

def getRewardAtState(rewardState, action, end):
	if(rewardState.myC == goalC and rewardState.myR == goalR and end):
		return 1.0
	#if(rewardState.tC == rewardState.myC and rewardState.tR == rewardState.myR):
	#	return -1.0

	if (abs(rewardState.myC-rewardState.tC) + abs(rewardState.myR-rewardState.tR) <= 1):
			return -1.0
	return 0.0

def initValueState(states, pi):
	for mc in range(maxC + 1):
		for mr in range(maxR + 1):
			for tc in range(maxC + 1):
				for tr in range(maxR + 1):
					state = State(mc,mr,tc,tr)
					best = float("-inf")
					actions = Action.getAllActions()
					for i in range(len(actions)):
						value = getRewardAtState(state, actions[i], True)
						if value > best:
							best = value
							states[mc][mr][tc][tr] = best
							pi[-1][mc][mr][tc][tr] = i

def getProbability(goalState, currentState, action):
	return playerTransition(goalState, currentState, action) * minotaurTransition(goalState, currentState, action)

def getExpectedReward(state, action, valState):
	accumulate = 0.0
	for mc in range(maxC + 1):
		for mr in range(maxR + 1):
			for tc in range(maxC + 1):
				for tr in range(maxR + 1):
					if ((abs(mc-state.myC) + abs(mr-state.myR) <= 1) and (abs(tc-state.tC) + abs(tr-state.tR) <= 1)):
						accumulate += getProbability(State(mc,mr,tc,tr), state, action)*valState[mc][mr][tc][tr]
	return accumulate

def solveBellman(T, valState, valStatePrev, pi):#, debugValState):
	for t in range(T-1, -1, -1):
		print(t)
		for mc in range(maxC + 1):
			for mr in range(maxR + 1):
				for tc in range(maxC + 1):
					for tr in range(maxR + 1):
						state = State(mc,mr,tc,tr)
						best = float("-inf")
						actions = Action.getAllActions()
						for i in range(len(actions)):
							a = actions[i]
							value = getRewardAtState(state, a, False) + getExpectedReward(state, a, valState)
							if value > best:
								best = value
								valStatePrev[mc][mr][tc][tr] = best
								pi[t][mc][mr][tc][tr] = i
		copy(valState, valStatePrev)
		#copy(debugValState[t], valState)

def solveHoward(valState, valStatePrev, pi):
	lam = 1-1/30
	piPrev = np.zeros((maxC+1,maxR+1,maxC+1,maxR+1), dtype=np.int8)
	counter = 0
	while True:
		print(counter)
		counter+=1
		for mc in range(maxC + 1):
			for mr in range(maxR + 1):
				for tc in range(maxC + 1):
					for tr in range(maxR + 1):
						state = State(mc,mr,tc,tr)
						a=Action.getAllActions()[piPrev[mc][mr][tc][tr]]
						valState[mc][mr][tc][tr] = getRewardAtState(state, a, True) + lam*getExpectedReward(state, a, valStatePrev)
		for mc in range(maxC + 1):
			for mr in range(maxR + 1):
				for tc in range(maxC + 1):
					for tr in range(maxR + 1):
						state = State(mc,mr,tc,tr)
						best = float("-inf")
						actions = Action.getAllActions()
						for i in range(len(actions)):
							a = actions[i]
							value = getRewardAtState(state, a, True) + lam*getExpectedReward(state, a, valState)
							if value > best:
								best = value
								pi[mc][mr][tc][tr] = i

		if ((pi == piPrev).all()):
			break

		copy(piPrev, pi)
		copy(valStatePrev, valState)

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
    		#c.create_text((col)*colWidth+colWidth*0.5, (row)*rowWidth + rowWidth/2, text=Action.getAllActions()[pi[deIndex,col,row, globalState.tC, globalState.tR]], font=("Helvetica", colWidth//4), tag='grid_line')
    		#c.create_text((col)*colWidth+colWidth*0.5, (row)*rowWidth + rowWidth/2, text="{:.1f}".format(debugValState[deIndex][col, row, globalState.tC, globalState.tR]), font=("Helvetica", colWidth//4), tag='grid_line')
    		c.create_text((col)*colWidth+colWidth*0.5, (row)*rowWidth + rowWidth*0.33, text=Action.getAllActions()[pi[col,row, minoC, minoR]], font=("Helvetica", colWidth//5), tag='grid_line')
    		c.create_text((col)*colWidth+colWidth*0.5, (row)*rowWidth + rowWidth*0.66, text="{:.2f}".format(valState[col, row, minoC, minoR]), font=("Helvetica", colWidth//6), tag='grid_line')
    		#text="{:.1f}".format(valState[col, row, 5-1, 0])
    		#text=Action.getAllActions()[pi[col,row, 5, 0]]
    		#text="{:.1f}".format(debugValState[deIndex][col, row, 5, 0])

    #c.create_text((globalState.myC)*colWidth+colWidth*0.33, (globalState.myR)*rowWidth + rowWidth/2, text=u'\u263a', font=("Helvetica", colWidth//4), tag='grid_line')
    #c.create_text((globalState.tC)*colWidth+colWidth*0.66, (globalState.tR)*rowWidth + rowWidth/2, text=u'\u2620', font=("Helvetica", colWidth//4), tag='grid_line')
    c.create_text((minoC)*colWidth+colWidth*0.75, (minoR)*rowWidth + rowWidth*0.33, text=u'\u2620', font=("Helvetica", colWidth//4), tag='grid_line')
    c.create_text((pC)*colWidth+colWidth*0.25, (pR)*rowWidth + rowWidth*0.33, text=u'\u263a', font=("Helvetica", colWidth//4), tag='grid_line')

def changeDebug(val):
	global deIndex
	deIndex += val
	deIndex = deIndex % T
	print("index", deIndex)
	create_grid()

def moveMino(rightMove, leftMove):
	global minoC
	global minoR
	prevPR = pR
	prevPC = pC
	playerMove()
	if not(minoR == prevPR and minoC == prevPC):
		minoC += rightMove
		minoC = min(maxC, minoC)
		minoC = max(minoC, 0)
		minoR += leftMove
		minoR = min(maxR, minoR)
		minoR = max(minoR, 0)
	if piTime:
		advanceTime()
	create_grid()

def advanceTime():
	global time
	global minoC
	global minoR
	global pC
	global pR
	time += 1
	if time == T:
		pC = startC
		pR = startR
		minoC = goalC
		minoR = goalR
		time = time % T

def resetGame():
	global time
	global minoC
	global minoR
	global pC
	global pR

	pC = startC
	pR = startR
	minoC = goalC
	minoR = goalR
	create_grid()


def playerMove():
	global pC
	global pR
	global minoC
	global minoR
	if piTime:
		a = Action.getAllActions()[pi[time, pC, pR, minoC, minoR]]
	else:
		a = Action.getAllActions()[pi[pC, pR, minoC, minoR]]
	if a in walls[pR][pC]:
		return
	if a == "L":
		pC -= 1
		pC = max(pC, 0)
	elif a == "R":
		pC += 1
		pC = min(maxC, pC)
	elif a == "U":
		pR -= 1
		pR = max(pR, 0)
	elif a == "D":
		pR += 1
		pR = min(maxR, pR)

def rollOut(pi, T):
	totalGames = 10000
	minT = 9
	maxT = T
	winRate = [0]*(maxT-minT+1)
	for t in range(minT,maxT+1):
		print(t)
		winCounter = 0.0
		for game in range(totalGames):
			winCounter += playGame(pi[-t:])
		winRate[t-minT] = winCounter/totalGames
	return winRate

def rollOutGeo(pi):
	totalGames = 10000
	winCounter = 0.0
	for game in range(totalGames):
		winCounter += playGameGeo(pi)
	print (winCounter/totalGames)


def playGameGeo(pi):
	tC = goalC
	tR = goalR
	plC = startC
	plR = startR

	while (random.random() < 1-1/30):
		newC, newR = playerMoveRollOut(pi, plC, plR, tC, tR)
		tC, tR = minoTaurMoveRollOut(tC, tR, plC, plR)
		plC = newC
		plR = newR	

		if (plC == goalC and plR == goalR):
			return 1.0
		elif (plC == tC and plR == tR):
			return 0.0
	return 0.0


def playGame(pi):
	tC = goalC
	tR = goalR
	plC = startC
	plR = startR

	for t in range(len(pi)):
		newC, newR = playerMoveRollOut(pi[t], plC, plR, tC, tR)
		tC, tR = minoTaurMoveRollOut(tC, tR, plC, plR)
		plC = newC
		plR = newR						

	if (plC == goalC and plR == goalR):
		return 1.0
	return 0.0


def playerMoveRollOut(pi, plC, plR, tC, tR):
	a = Action.getAllActions()[pi[plC, plR, tC, tR]]
	if a in walls[plR][plC]:
		return (plC, plR)
	if a == "L":
		plC -= 1
		plC = max(plC, 0)
	elif a == "R":
		plC += 1
		plC = min(maxC, plC)
	elif a == "U":
		plR -= 1
		plR = max(plR, 0)
	elif a == "D":
		plR += 1
		plR = min(maxR, plR)
	return (plC, plR)


def minoTaurMoveRollOut(tC, tR, plC, plR):
	val = random.randint(0,4) if minotaurCanStay else random.randint(0,3)

	if tR == plR and tC == plC:
		return (tC,tR)
	for off in range(5):
		ofs = (val+off) % 5 if minotaurCanStay else (val + off) % 4
		if (ofs == 0 and tR != 0):
			return (tC, tR-1)
		if (ofs == 1 and tC != maxC):
			return (tC+1, tR)
		if (ofs == 2 and tR != maxR):
			return (tC, tR+1)
		if (ofs == 3 and tC != 0):
			return (tC-1, tR)
		if (ofs == 4):
			return (tC, tR)
	return (tC, tR)

maxC = 5
maxR = 4
goalC = 4
goalR = 4
startC = 0
startR = 0
	

globalState = State(startC,startR, 4, 4)
walls = getWalls()
minotaurCanStay = False
piTime = False

minoC = 4
minoR = 4
pC = 0
pR = 0
time = 0

valState = np.zeros((maxC+1,maxR+1,maxC+1,maxR+1))
valStatePrev = np.zeros((maxC+1,maxR+1,maxC+1,maxR+1))

pi = np.zeros((maxC+1,maxR+1,maxC+1,maxR+1), dtype=np.int8)

solveHoward(valState,valStatePrev,pi)

rollOutGeo(pi)

'''
#Finite Time Horizon
T = 50

debugValState = np.zeros((T+1, maxC+1,maxR+1,maxC+1,maxR+1))
deIndex = 0

pi = np.zeros((T, maxC+1,maxR+1,maxC+1,maxR+1), dtype=np.int8)

initValueState(valState,pi)
#copy(debugValState[T], valState)

solveBellman(T, valState, valStatePrev, pi)#, debugValState)

minoMoveWinRate = rollOut(pi, T)

initValueState(valState,pi)
minotaurCanStay = True
solveBellman(T, valState, valStatePrev, pi)
minoStayWinRate = rollOut(pi, T)

plt.plot(range(9,T+1), minoMoveWinRate, label="Move Win Rate")
plt.plot(range(9,T+1), minoStayWinRate, label="Stay Win Rate")
plt.legend()
plt.show()
'''

root = tk.Tk()

c = tk.Canvas(root, height=500, width=500, bg='white')
c.pack(fill=tk.BOTH, expand=True)

c.bind('<Configure>', create_grid)

#c.bind_all('<Left>', lambda e,val = -1: changeDebug(val))
#c.bind_all('<Right>', lambda e,val = 1: changeDebug(val))

c.bind_all('<Left>', lambda e,rightMove = -1, leftMove = 0: moveMino(rightMove, leftMove))
c.bind_all('<Right>', lambda e,rightMove = 1, leftMove = 0: moveMino(rightMove, leftMove))
c.bind_all('<Up>', lambda e,rightMove = 0, leftMove = -1: moveMino(rightMove, leftMove))
c.bind_all('<Down>', lambda e,rightMove = 0, leftMove = 1: moveMino(rightMove, leftMove))

c.bind_all('r', lambda e: resetGame())

#root.after(5000,create_grid)
root.mainloop()