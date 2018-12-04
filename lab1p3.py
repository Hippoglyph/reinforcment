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

	def initState():
		return State(rS[0], rS[1], pS[0], pS[1])

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

def canMove(state, action):
	#borders
	if ((state.rC == 0 and action == "L") or (state.rC == maxC and action == "R") or (state.rR == 0 and action == "U") or (state.rR == maxR and action == "D")):
		return False
	return True

def canPoliceMove(state, action):
	#borders
	if ((state.pC == 0 and action == "L") or (state.pC == maxC and action == "R") or (state.pR == 0 and action == "U") or (state.pR == maxR and action == "D")):
		return False
	return True

def QLearn(iterations, res, eps):
	Q = np.zeros((maxR+1, maxC+1, maxR+1, maxC+1, len(actions)))
	alpha = np.zeros((maxR+1, maxC+1, maxR+1, maxC+1, len(actions)))
	lam = 0.8
	state = State(rS[0],rS[1],pS[0],pS[1])
	values = np.zeros((iterations//res))
	counter = 0


	for t in range(iterations):
		ai = getEGreedyActionQIndex(state, eps, Q)
		a = actions[ai]
		r = getReward(state, a)
		nextState = getNextState(state, a)
		alpha[state.rR, state.rC, state.pR, state.pC, ai]+=1
		step = 1/(alpha[state.rR, state.rC, state.pR, state.pC, ai]**(2.0/3.0))
		Q[state.rR, state.rC, state.pR, state.pC, ai] += step*(r + lam*max([Q[nextState.rR, nextState.rC, nextState.pR, nextState.pC, i] for i in range(len(actions))]) - Q[state.rR, state.rC, state.pR, state.pC, ai])
		state = nextState
		if t % res == 0:
			values[counter] = max([Q[rS[0], rS[1], pS[0], pS[1], i] for i in range(len(actions))])
			counter+=1
			print(counter)

	pi = np.zeros((maxR+1, maxC+1, maxR+1, maxC+1), dtype=int)
	for rR in range(maxR + 1):
		for rC in range(maxC + 1):
			for pR in range(maxR + 1):
				for pC in range(maxC + 1):
					pi[rR, rC, pR, pC] = np.argmax([Q[rR, rC, pR, pC, i] for i in range(len(actions))])

	return pi, values

def SARSAlearn(iterations, res,eps):
	Q = np.zeros((maxR+1, maxC+1, maxR+1, maxC+1, len(actions)))
	alpha = np.zeros((maxR+1, maxC+1, maxR+1, maxC+1, len(actions)))
	pi = np.zeros((maxR+1, maxC+1, maxR+1, maxC+1), dtype=int)
	lam = 0.8
	state = State(rS[0],rS[1],pS[0],pS[1])
	values = np.zeros((iterations//res))
	counter = 0

	ai = pi[rS[0],rS[1],pS[0],pS[1]]
	#eps = 0.1
	for t in range(iterations):
		a = actions[ai]
		r = getReward(state, a)
		nextState = getNextState(state, a)
		nextAi = getEGreedyActionIndex(nextState, eps, pi)
		#nextAi = pi[nextState.rR, nextState.rC, nextState.pR, nextState.pC]
		alpha[state.rR, state.rC, state.pR, state.pC, ai]+=1
		step = 1/(alpha[state.rR, state.rC, state.pR, state.pC, ai]**(2.0/3.0))
		Q[state.rR, state.rC, state.pR, state.pC, ai] += step*(r + lam*(Q[nextState.rR, nextState.rC, nextState.pR, nextState.pC, nextAi]) - Q[state.rR, state.rC, state.pR, state.pC, ai])
		pi[state.rR, state.rC, state.pR, state.pC] = np.argmax([Q[state.rR, state.rC, state.pR, state.pC, i] for i in range(len(actions))])

		state = nextState
		ai = nextAi
		if t % res == 0:
			values[counter] = max([Q[rS[0], rS[1], pS[0], pS[1], i] for i in range(len(actions))])
			counter+=1
			print(counter)
	return pi, values

def getEGreedyActionIndex(state, eps, pi):
	if random.random() < eps:
		return selectRandomActionIndex(state)
	return pi[state.rR, state.rC, state.pR, state.pC]

def getEGreedyActionQIndex(state, eps, Q):
	if random.random() < eps:
		return selectRandomActionIndex(state)
	return np.argmax([Q[state.rR, state.rC, state.pR, state.pC, i] for i in range(len(actions))])


def getNextState(state, action):
	newState = State(state.rR, state.rC, state.pR, state.pC)
	if state.isTaken():
		return State.initState()

	if action == "L":
		newState.rC = max(newState.rC-1, 0)
	elif action == "R":
		newState.rC = min(newState.rC+1, maxC)
	elif action == "U":
		newState.rR = max(newState.rC-1, 0)
	elif action == "D":
		newState.rR = min(newState.rC+1, maxC)

	a = policeWalk(state)
	if a == "L":
		newState.pC -= 1
	elif a == "R":
		newState.pC += 1
	elif a == "U":
		newState.pR -= 1
	elif a == "D":
		newState.pR += 1

	return newState


def selectRandomActionIndex(state):
	return random.randint(0, len(actions)-1)
	'''
	probs = np.zeros(len(actions), dtype=np.double)
	moves = 0.0
	for i in range(len(probs)):
		if canMove(state, actions[i]):
			moves+=1
			probs[i] = 1

	for p in range(len(probs)):
		probs[p] /= moves

	cumSum = np.cumsum(probs)

	val = random.random()

	for i in range(len(cumSum)):
		if cumSum[i] > val:
			return i
	return len(actions)-1
	'''

def policeWalk(state):

	probs = np.zeros(len(actions)-1, dtype=np.double)
	moves = 0.0
	for i in range(len(probs)):
		if canPoliceMove(state, actions[i+1]):
			moves+=1
			probs[i] = 1

	for p in range(len(probs)):
		probs[p] /= moves

	cumSum = np.cumsum(probs)

	val = random.random()

	for i in range(len(cumSum)):
		if cumSum[i] > val:
			return actions[i+1]
	return actions[-1]

def copy(take, give):
	for rR in range(maxR + 1):
		for rC in range(maxC + 1):
			for pR in range(maxR + 1):
				for pC in range(maxC + 1):
					take[rR,rC,pR,pC] = give[rR,rC,pR,pC]

def create_grid(pi, rR, rC, pR, pC):
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
    		#c.create_text((col)*colWidth+colWidth*0.5, (row)*rowWidth + rowWidth*0.66, text="{:.2f}".format(valState[row, col, pR, pC]), font=("Helvetica", colWidth//6), tag='grid_line')

    c.create_text((pC)*colWidth+colWidth*0.75, (pR)*rowWidth + rowWidth*0.33, text=u'\u2620', font=("Helvetica", colWidth//4), tag='grid_line')
    c.create_text((rC)*colWidth+colWidth*0.25, (rR)*rowWidth + rowWidth*0.33, text=u'\u263a', font=("Helvetica", colWidth//4), tag='grid_line')

def advanceGame(pi, state):
	nextState = getNextState(state, actions[pi[state.rR, state.rC, state.pR, state.pC]])
	state.rR = nextState.rR
	state.rC = nextState.rC
	state.pR = nextState.pR
	state.pC = nextState.pC
	create_grid(pi, state.rR, state.rC, state.pR, state.pC)

def changePi(val, eps):
	global pid
	pid = max(0,min(len(eps)-1, pid+val))
	print("Pi for eps = ", str(eps[pid]))

bank = (1,1)

actions = ["S" ,"U", "R", "D", "L"]

pS = (3,3)

rS = (0,0)

maxR = 3
maxC = 3

eps = [0.1,0.2,0.4,0.6, 0.8, 1.0]
pis = np.zeros((len(eps), maxR+1, maxC+1, maxR+1, maxC+1), dtype=int)
pid = 0

pi, qValues = QLearn(200000, 1000, 1.0)
plt.plot(qValues)
#

#for ei in range(len(eps)):
#	pi, Values = SARSAlearn(100000, 1000, eps[ei])
#	copy(pis[ei], pi)
#	plt.plot(Values, label="Eps " + str(eps[ei]))

plt.xlabel("Iteration (1e+3)")
plt.ylabel("Values at initial state")
plt.legend()
plt.show()

stateRollOut = State.initState()


root = tk.Tk()

c = tk.Canvas(root, height=250, width=500, bg='white')
c.pack(fill=tk.BOTH, expand=True)


c.bind('<Configure>', lambda e: create_grid(pis[pid], rS[0], rS[1], pS[0], pS[1]))
c.bind_all('<Return>', lambda e: advanceGame(pis[pid], stateRollOut))

c.bind_all('<Left>', lambda e,val = -1: changePi(val, eps))
c.bind_all('<Right>', lambda e,val = 1: changePi(val, eps))

#c.bind_all('<Left>', lambda e,rightMove = -1, leftMove = 0: moveMino(rightMove, leftMove))
#c.bind_all('<Right>', lambda e,rightMove = 1, leftMove = 0: moveMino(rightMove, leftMove))
#c.bind_all('<Up>', lambda e,rightMove = 0, leftMove = -1: moveMino(rightMove, leftMove))
#c.bind_all('<Down>', lambda e,rightMove = 0, leftMove = 1: moveMino(rightMove, leftMove))

#c.bind_all('r', lambda e: resetGame())

root.mainloop()