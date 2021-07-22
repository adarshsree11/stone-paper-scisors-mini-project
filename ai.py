import random


nn = 0
np = 0
ns = 0
pn = 0
pp = 0
ps = 0
sn = 0
sp = 0
ss = 0
	
c = 0

ai_points = 0
user_points = 0
draw_points = 0
win_perc = 0

user_move = 0
comp_move = 0
winner = ""
points = []
last_move = 0
last_winner = "User"
sec_last_winner = "User"

def next(choice):
	choice = choice + 1
	if choice == 3:
		choice = 0
	return choice

def prev(choice):
	choice = choice - 1
	if choice == -1:
		choice = 2
	return choice



def aiPredicts(last, choice):


	global nn
	global np
	global ns	
	global pn
	global pp
	global ps
	global sn
	global sp
	global ss
	



	def nextNext(last,choice):
		print("using next-next")
		print("User won or lost last round, counteracting next move")
		return prev(choice)


	def nextPrev(last,choice):
		print("using next-prev")
		if last == "User":
			print("User won last round, counteracting next move")
			return prev(choice)
		else:
			print("User lost last round, counteracting prev move")
			return choice


	def nextSame(last,choice):
		print("using next-same")
		if last == "User":
			print("User won last round, counteracting next move")
			return prev(choice)
		else:
			print("User lost last round, counteracting same move")
			return next(choice)


	def prevNext(last,choice):
		print("using prev-next")
		if last == "User":
			print("User won last round, counteracting prev move")
			return choice
		else:
			print("User lost last round, counteracting next move")
			return prev(choice)


	def prevPrev(last,choice):
		print("using prev-prev")
		print("User win or lost last round, counteracting prev move")
		return choice
		

	def prevSame(last,choice):
		print("using prev-same")
		if last == "User":
			print("User won last round, counteracting prev move")
			return choice
		else:
			print("User lost last round, counteracting same move")
			return next(choice)


	def sameNext(last,choice):
		print("using same-next")
		if last == "User":
			print("User won last round, counteracting same move")
			return next(choice)
		else:
			print("User lost last round, counteracting next move")
			return prev(choice)


	def samePrev(last,choice):
		print("using same-prev")
		if last == "User":
			print("User won last round, counteracting same move")
			return next(choice)
		else:
			print("User lost last round, counteracting prev move")
			return choice


	def sameSame(last,choice):
		print("using same-same")
		print("User won or lost last round, counteracting same move")
		return next(choice)


	selected_algo = "ss"

	algorithm_dict = {"ss":ss, "sp":sp, "sn":sn, "ps":ps, "pp":pp, "pn":pn, "ns":ns, "np":np, "nn":nn} 

	for algo in algorithm_dict.keys():
		if algorithm_dict[algo] > algorithm_dict[selected_algo]:
			selected_algo = algo


	if selected_algo == "nn":
		return nextNext(last, choice)
	elif selected_algo == "ns":
		return nextSame(last, choice)
	elif selected_algo == "np":
		return nextPrev(last, choice)
	elif selected_algo == "pp":
		return prevPrev(last, choice)
	elif selected_algo == "ps":
		return prevSame(last, choice)
	elif selected_algo == "pn":
		return prevNext(last, choice)
	elif selected_algo == "ss":
		return sameSame(last, choice)
	elif selected_algo == "sn":
		return sameNext(last, choice)
	elif selected_algo == "sp":
		return samePrev(last, choice)
	

def ai_calc(last_choice,curr_choice,winner):


	global nn
	global np
	global ns	
	global pn
	global pp
	global ps
	global sn
	global sp
	global ss
	

	def calcAiWins():
		return 1

	if winner == "User" and (next(last_choice) == curr_choice):
		nn = nn + calcAiWins()
		ns = ns + calcAiWins()
		np = np + calcAiWins()
	elif winner == "User" and (prev(last_choice) == curr_choice):
		pp = pp + calcAiWins()
		ps = ps + calcAiWins()
		pn = pn + calcAiWins()
	elif winner == "User" and (last_choice == curr_choice):
		ss = ss + calcAiWins()
		sn = sn + calcAiWins()
		sp = sp + calcAiWins()
	elif winner != "User" and (next(last_choice) == curr_choice):
		nn = nn + calcAiWins()
		pn = pn + calcAiWins()
		sn = sn + calcAiWins()
	elif winner != "User" and (prev(last_choice) == curr_choice):
		pp = pp + calcAiWins()
		np = np + calcAiWins()
		sp = sp + calcAiWins()
	elif winner != "User" and (last_choice == curr_choice):
		ss = ss + calcAiWins()
		ns = ns + calcAiWins()
		ps = ps + calcAiWins()


	print("win_count-- nn-{} np-{} ns-{} pn-{} pp-{} ps-{} sn-{} sp-{} ss-{} \n".format(nn,np,ns,pn,pp,ps,sn,sp,ss))

	ai_wins = nn + np + ns + pn + pp + ps + sn + sp + ss


def getInput():
	user_input = input("Enter stone, paper,  or scissors?").lower()
	return int(user_input)


mapper = { 0:'stone',
			1:'paper',
			2:'scissors',
			3:'none'}

'''
reverse_mapper = { '1':0,
					'2':1,
					'3':2}
'''

def chooseRandom():
	choice = random.choice([0,1,2])
	return(choice)


def getWinner(user, comp):
	if(user == comp):
		return "Draw"

	else:
		if (user == 2 and comp == 0):
			comp = 3

		if (comp == 2 and user == 0):
			user = 3

		if(user > comp):
			return "User"

		elif(comp > user):
			return "Ai"


def give_points(winner):

	global ai_points
	global user_points
	global draw_points
	global win_perc

	if winner == "Ai":
		ai_points = ai_points + 1
	elif winner == "User":
		user_points = user_points + 1
	elif winner == "Draw":
		draw_points = draw_points + 1

	try:
		win_perc = round(ai_points / (ai_points + user_points) *100)
	except ZeroDivisionError:
		win_perc = 0

	print("\nAI : {}  USER : {}  DRAW : {}   	WIN% : {}%\n".format(ai_points, user_points, draw_points, win_perc))

	return_list = [ai_points, user_points, draw_points, win_perc]
	return (return_list)

def reset_points():
	global ai_points
	global user_points
	global draw_points
	global win_perc

	global nn
	global np
	global ns	
	global pn
	global pp
	global ps
	global sn
	global sp
	global ss

	global c

	nn = 0
	np = 0
	ns = 0
	pn = 0
	pp = 0
	ps = 0
	sn = 0
	sp = 0
	ss = 0
		
	c = 0
	ai_points = 0
	user_points = 0
	draw_points = 0
	win_perc = 0

def compMoveRandom(user_input):

	global user_move
	global comp_move
	global winner
	global points

	user_move = user_input
	comp_move = chooseRandom()
	print("user : " + mapper[user_move])
	print("ai : " + mapper[comp_move])
	winner = getWinner(user_move, comp_move)
	points = give_points(winner)
	return comp_move, points, winner


def compMoveAi(user_input):
	global user_move
	global comp_move
	global winner
	global points

	global c
	
	global last_move
	global last_winner
	global sec_last_winner
	
	if c == 1:
		last_move = user_move
		sec_last_winner = last_winner
		last_winner = winner
		user_move = user_input

		
		comp_move = aiPredicts(sec_last_winner, last_move)
		print("user : " + mapper[user_move])
		print("ai : " + mapper[comp_move])
		winner = getWinner(user_move, comp_move)
		ai_calc(last_move, user_move, last_winner)
		points = give_points(winner)
		return comp_move, points, winner
	else:
		c = 1
		return compMoveRandom(user_input)

def main():
	#faulty needs change
	display_elements = compMoveRandom(user_move)
	print("display_elements {}".format(display_elements))
	while True:
		print("ai")
		display_elements = compMoveAi(user_move)
		print("display_elements {}".format(display_elements))
	
	'''print("user : " + mapper[user_move])
	#comp_move = chooseRandom()
	print("ai : " + mapper[comp_move])
	winner = getWinner(user_move, comp_move)
	print("winner :" + winner)
	give_points(winner)

	while True:

		last_move = user_move
		last_winner = winner
		user_move = getInput()
		
		comp_move = aiPredicts(winner, last_move)
		print("\nuser : " + mapper[user_move])
		print("ai : " + mapper[comp_move] +"\n")
		winner = getWinner(user_move, comp_move)
		print("winner :" + winner)
		give_points(winner)
		ai_calc(last_move, user_move, last_winner)
	'''	

if __name__ == '__main__':
	main()