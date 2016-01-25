from sys import argv
from sys import maxint
move_name_map = {0:"B", 1:"A"}
traverse_log = list()

class Board(object):

	def __init__(self, board2, board1, mancala2, mancala1, player_no, move_name = "root"):
		self.board = [board1, board2]
		self.mancala = [mancala1, mancala2]
		self.player_no = player_no
		self.boardsize = len(self.board[0])+2
		self.move_name = move_name
		self.game_over = False

	def __repr__(self):
		return " ".join(str(i) for i in self.board[1]) + "\r\n" + " ".join(str(i) for i in self.board[0]) + "\r\n" + str(self.mancala[1]) + "\r\n" + str(self.mancala[0]) + "\r\n"

	def move(self, player_no, pit): #pit number from 0 to boardsize-3, returns True if another chance available otherwise False
		marbles = self.board[player_no][pit]
		self.board[player_no][pit] = 0
		last_index=-2
		
		size = (self.boardsize-2)*2 + 1
		quotient = marbles/size
		for i in range(len(self.board[0])):
			self.board[0][i] += quotient
			self.board[1][i] += quotient
		self.mancala[player_no] += quotient
		marbles = marbles%size

		side = player_no
		direction = 1 if side == 0 else -1
		start = pit+1 if side == 0 else pit-1
		end = self.boardsize-2 if side == 0 else -1

		while marbles>0:
			for i in range(start, end, direction):
				self.board[side][i]+=1
				marbles -= 1
				if marbles==0:
					last_index = i
					break

			if marbles>0 and player_no==side: #ToDo: Optimize here
				self.mancala[player_no]+=1
				marbles -= 1
				last_index = -1 #last_index=-1 for player's mancala

			if marbles==0:
				break

			side = 1-side
			direction *= -1
			start = 0 if side == 0 else self.boardsize-3
			end = self.boardsize-2 if side == 0 else -1
		if last_index!=-1 and side==player_no and self.board[side][last_index]==1:
			self.mancala[side] = self.mancala[side] + self.board[1-side][last_index] + 1
			self.board[1-side][last_index] = 0
			self.board[side][last_index] = 0

		if self.board[0].count(0)==self.boardsize-2:
			self.mancala[1] += sum(self.board[1])
			self.board[1] = [0]*(self.boardsize-2)
			self.game_over = True

		if self.board[1].count(0)==self.boardsize-2:
			self.mancala[0] += sum(self.board[0])
			self.board[0] = [0]*(self.boardsize-2)
			self.game_over = True

		if last_index==-1:# and not self.game_over:
			return True
		else:
			return False


	def get_eval(self):
		return self.mancala[self.player_no] - self.mancala[1-self.player_no]

	def next_board(self, player, pit, move_name):
		b = self.copy_board(move_name)
		extra = b.move(player, pit)
		return b, extra

	def copy_board(self, move_name):
		return Board([i for i in self.board[1]], [i for i in self.board[0]], self.mancala[1], self.mancala[0], self.player_no, move_name)

def greedy(board):
	global move_name_map
	pl = board.player_no
	optimum = None #optimum eval func should be highest always
	for i in range(0, board.boardsize-2):
		if board.board[pl][i]==0:
			continue
		b, extra = board.next_board(pl, i, None) #Move name not required but is: move_name_map[pl] + str(i+2)
		if extra:
			b = greedy(b)
		if not optimum or optimum.get_eval()<b.get_eval():
			optimum = b

	return optimum

def print_mm_log(move_name, depth, value): #Print log for minimax
	global traverse_log
	traverse_log.append(move_name + "," + str(depth) + "," + str(value) + "\r\n")

def minimax(board, cutoff): #new, as per textbook
	return maxM(board, cutoff, 0, False) #return board, val

def maxM(board, cutoff, depth, extra_move): #extra_move boolean tells if it has free move available
	
	pl = board.player_no
	boardval = board.get_eval()
	if depth == cutoff and not extra_move:
		print_mm_log(board.move_name, depth, boardval)
		return board, boardval

	optimumBoard = board
	optimumVal = "-Infinity"# if depth!=cutoff else boardval : Changed for Question version 3
	b = board
	depth_next = depth + 1 if not extra_move else depth	
	print_mm_log(board.move_name, depth, optimumVal)

	if board.game_over:
		print_mm_log(board.move_name, depth, boardval)
		return optimumBoard, boardval

	for i in range(0, board.boardsize-2):
		
		if board.board[pl][i]==0:
				continue

		next_board, next_extra = board.next_board(pl, i, move_name_map[pl] + str(i+2))

		if next_extra:
			b, v = maxM(next_board, cutoff, depth_next, next_extra)
		else:
			b, v = minM(next_board, cutoff, depth_next, next_extra)
		if optimumVal=="-Infinity" or v>optimumVal:
			optimumBoard = next_board if not next_extra else b
			optimumVal = v
		print_mm_log(board.move_name, depth, optimumVal)

	return optimumBoard, optimumVal

def minM(board, cutoff, depth, extra_move): #extra_move boolean tells if it has free move available

	pl =  1-board.player_no
	boardval = board.get_eval()
	if depth == cutoff and not extra_move:
		print_mm_log(board.move_name, depth, boardval)
		return board, boardval

	optimumBoard = board
	optimumVal = "Infinity"# if depth!=cutoff else boardval : Changed for Question version 3
	b = board
	depth_next = depth + 1 if not extra_move else depth
	print_mm_log(board.move_name, depth, optimumVal)

	if board.game_over:
		print_mm_log(board.move_name, depth, boardval)
		return optimumBoard, boardval

	for i in range(0, board.boardsize-2):
		if board.board[pl][i]==0:
				continue
		next_board, next_extra = board.next_board(pl, i, move_name_map[pl] + str(i+2))
		
		if next_extra:
			b, v = minM(next_board, cutoff, depth_next, next_extra)
		else:
			b, v = maxM(next_board, cutoff, depth_next, next_extra)
		if optimumVal=="Infinity" or v<optimumVal:
			optimumBoard = next_board if not next_extra else b
			optimumVal = v
		print_mm_log(board.move_name, depth, optimumVal)

	return optimumBoard, optimumVal












#Alpha-Beta

def print_ab_log(move_name, depth, value, alpha, beta): #Print log for alpha beta
	global traverse_log
	traverse_log.append(move_name + "," + str(depth) + "," + str(value) + "," + str(alpha) + "," + str(beta) +  "\r\n")# + ", " + str(board.board[1]) + ";" + str(board.board[0]) + ", " + str(board.mancala[1]) + ";" + str(board.mancala[0]) +  "\r\n")

def alphabeta(board, cutoff): #new, as per textbook
	return maxAB(board, cutoff, 0, False, "-Infinity", "Infinity") #return board, val

def maxAB(board, cutoff, depth, extra_move, alpha, beta): #extra_move boolean tells if it has free move available
	pl = board.player_no
	
	boardval = board.get_eval()
	if depth == cutoff and not extra_move:
		print_ab_log(board.move_name, depth, boardval, alpha, beta)
		return board, boardval

	optimumBoard = board
	optimumVal = "-Infinity" #if depth!=cutoff else boardval
	b = board
	depth_next = depth + 1 if not extra_move else depth	
	print_ab_log(board.move_name, depth, optimumVal, alpha, beta)

	if board.game_over:
		print_ab_log(board.move_name, depth, boardval, alpha, beta)
		return optimumBoard, boardval

	for i in range(0, board.boardsize-2):
		
		if board.board[pl][i]==0:
				continue

		next_board, next_extra = board.next_board(pl, i, move_name_map[pl] + str(i+2))

		if next_extra:
			b, v = maxAB(next_board, cutoff, depth_next, next_extra, alpha, beta)
		else:
			b, v = minAB(next_board, cutoff, depth_next, next_extra, alpha, beta)
		#print "max", board.move_name, optimumVal, b.move_name, v, next_board.move_name, next_board.get_eval()
		if optimumVal=="-Infinity" or v>optimumVal:
			optimumBoard = next_board if not next_extra else b
			optimumVal = v

		if beta != "Infinity" and v>=beta:
			print_ab_log(board.move_name, depth, optimumVal, alpha, beta)
			return optimumBoard, v

		if alpha=="-Infinity" or v>alpha:
			alpha = v
		
		#print "update", optimumBoard.move_name, optimumVal
		print_ab_log(board.move_name, depth, optimumVal, alpha, beta)
		
		

	return optimumBoard, optimumVal

def minAB(board, cutoff, depth, extra_move, alpha, beta): #extra_move boolean tells if it has free move available

	pl =  1-board.player_no

	#print "min, pl:", pl, ", move: ", board.move_name, " depth: ", depth, " extra: ", extra_move, ", board: \n", board
	
	boardval = board.get_eval()
	if depth == cutoff and not extra_move:
		print_ab_log(board.move_name, depth, boardval, alpha, beta)
		return board, boardval

	optimumBoard = board
	optimumVal = "Infinity" #if depth!=cutoff else boardval
	b = board
	depth_next = depth + 1 if not extra_move else depth
	print_ab_log(board.move_name, depth, optimumVal, alpha, beta)

	if board.game_over:
		print_ab_log(board.move_name, depth, boardval, alpha, beta)
		return optimumBoard, boardval

	for i in range(0, board.boardsize-2):
		if board.board[pl][i]==0:
				continue
		next_board, next_extra = board.next_board(pl, i, move_name_map[pl] + str(i+2))
		
		if next_extra:
			b, v = minAB(next_board, cutoff, depth_next, next_extra, alpha, beta)
		else:
			b, v = maxAB(next_board, cutoff, depth_next, next_extra, alpha, beta)
		#print "min", board.move_name, optimumVal, b.move_name, v, next_board.move_name, next_board.get_eval()
		if optimumVal=="Infinity" or v<optimumVal:
			optimumBoard = next_board if not next_extra else b
			optimumVal = v

		if alpha != "-Infinity" and alpha>=v:
			print_ab_log(board.move_name, depth, optimumVal, alpha, beta)
			return optimumBoard, v

		if beta=="Infinity" or v<beta:
			beta = v
		#print "update", optimumBoard.move_name, optimumVal
		print_ab_log(board.move_name, depth, optimumVal, alpha, beta)
		
		

	return optimumBoard, optimumVal

def main():
	global traverse_log

	f = open(argv[2])
	task = int(f.readline()) #Greedy=1, MiniMax=2, AlphaBeta=2, Competition=4
	my_player_no = int(f.readline()) - 1
	cutoff = int(f.readline())
	board2 = [int(i) for i in f.readline().strip().split()] #A = board 2 for player 2 ie player 1 from now on
	board1 = [int(i) for i in f.readline().strip().split()] #B = board 1 for player 1 ie player 0 from now on
	mancala2 = int(f.readline()) # A1 for player 2 ie person 1
	mancala1 = int(f.readline()) # Bn for player 1 ie person 0
	f.close()


	b = Board(board2, board1, mancala2, mancala1, my_player_no)

	if task==1:
		next_state = greedy(b)
	elif task==2:
		next_state, val = minimax(b, cutoff)
		traverse = open("traverse_log.txt", 'w')
		traverse.write("Node,Depth,Value\r\n")
		traverse.writelines(traverse_log)
		traverse.close()
	elif task==3:
		next_state, val = alphabeta(b, cutoff)
		traverse = open("traverse_log.txt", 'w')
		traverse.write("Node,Depth,Value,Alpha,Beta\r\n")
		traverse.writelines(traverse_log)
		traverse.close()

	out = open("next_state.txt", 'w')
	out.write(next_state.__repr__())
	out.close()

if __name__=="__main__":
	main()