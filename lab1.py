
class State:
	def __init__(myC,myR,tC,tR):
		self.myC = myC
		self.myR = myR
		self.tC = tC
		self.tR = tR

	def posEquals(r,c):
		return self.myC == c and self.myR == r

class Action:
	def __init__(a):
		self.a = a


def transition(state, action):

	if((state.myC == 0 and action == "L") or (state.myC == 5 and action == "R") or (state.myR == 0 and action == "U") or (state.myR == 4 and action == "D")):
		return 0
	if((state.posEquals(0,1) and action == "R") or (state.posEquals(1,0) and action == "L")):
		return 0

	return 1