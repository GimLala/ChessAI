from copy import copy
import config
from config import *
from Coordinates import Point


# All pieces will be inheriting from this class.

class Piece(turtle.Turtle):
	
	def __init__(self, piece_colour, piece_type, opposite_piece_colour, point):
		
		super().__init__()
		
		# Sets default properties.
		
		self.piece_colour = piece_colour
		self.piece_type = piece_type
		self.absolute_piece_type = f"{self.piece_colour} {self.piece_type}"
		self.opposite_piece_colour = opposite_piece_colour
		
		self.has_moved = False
		self.point = point
		self.point.state = [self.piece_colour, self.piece_type]
		
		self.attacked_points = ()
		
		# Piece goes to the position it is supposed to.
		
		self.penup()
		self.goto(self.point.x, self.point.y)
		
		# Draws the pieces.
		
		self.shape(f"{self.piece_colour} {self.piece_type}")
		point.piece = self
		
		# Appends itself in appropriate lists.
		
		pieces_group.append(self)
		getattr(config, f"{self.piece_colour}_pieces_group").append(self)
	
	# For Zobrist hashing and FEN string decoding.
	
	@staticmethod
	def letter_to_num(letter):
		
		letter_to_num_dict = {
			"K": 0,
			"Q": 1,
			"B": 2,
			"N": 3,
			"R": 4,
			"P": 5,
			"k": 6,
			"q": 7,
			"b": 8,
			"n": 9,
			"r": 10,
			"p": 11
		}
		return letter_to_num_dict.get(letter)


class King(Piece):
	
	def __init__(self, piece_colour, opposite_piece_colour, point):
		
		super().__init__(piece_colour, "king", opposite_piece_colour, point)
		
		if self.piece_colour == "white":
			
			white_king_piece = self
		
		else:
			
			black_king_piece = self
		
		self.set_attacked_points()
	
	def set_attacked_points(self):
		
		self.attacked_points = [point for point in (self.point.top, self.point.top_right,
												self.point.right, self.point.bottom_right,
												self.point.bottom, self.point.bottom_left,
												self.point.left, self.point.top_left) if point]
	
	def get_valid_moves(self):
		
		valid_moves = ()
		 
		for linked_point in self.attacked_points:
			
			# Normal Moves
			
			if not linked_point.state[0]:
				
				valid_moves += (linked_point, )
			
			# Captures.
			
			elif linked_point.state[0] == self.opposite_piece_colour:
				
				valid_moves += ((linked_point, linked_point.piece), )
		
		# Castling
		
		if not self.has_moved:
			
			for rook in getattr(config, f"{self.piece_colour}_rooks"):
				
				if not rook.has_moved:
					
					# Short side.
					
					if rook.point.board_cor[0] == 8:
						
						if not self.point.right.state[0] and not self.point.right.right.state[0]:
							
							valid_moves += ((self.point.right.right, rook, self.point.right), )
					
					# Long side.
					
					if rook.point.board_cor[0] == 1:
						
						if not self.point.left.state[0] and not self.point.left.left.state[0] and not self.point.left.left.left.state[0]:
							
							valid_moves += ((self.point.left.left, rook, self.point.left), )
		
		return valid_moves


class Queen(Piece):
	
	def __init__(self, piece_colour, opposite_piece_colour, point):
		
		super().__init__(piece_colour, "queen", opposite_piece_colour, point)
		
		if self.piece_colour == "white":
			
			white_queens.append(self)
		
		else:
			
			black_queens.append(self)
		
		self.set_attacked_points()
	
	def set_attacked_points(self):
		
		self.attacked_points = ()
		
		for attr_name in point_attr_name_list:
			
			linked_point = getattr(self.point, attr_name)
			attacked_line = ()
			
			while linked_point:
				
				attacked_line += (linked_point, )
				linked_point = getattr(linked_point, attr_name)
			
			if attacked_line:
				
				self.attacked_points += (attacked_line, )
	
	def get_valid_moves(self):
		
		valid_moves = ()
		 
		for attacked_line in self.attacked_points:
			
			for linked_point in attacked_line:
				
				if not linked_point.state[0]:
					
					valid_moves += (linked_point, )
				
				elif linked_point.state[0] == self.opposite_piece_colour:
					
					valid_moves += ((linked_point, linked_point.piece), )
					
					break
				
				else:
					
					break
		
		return valid_moves


class Bishop(Piece):
	
	def __init__(self, piece_colour, opposite_piece_colour, point):
		
		super().__init__(piece_colour, "bishop", opposite_piece_colour, point)
		
		if self.piece_colour == "white":
			
			white_bishops.append(self)
		
		else:
			
			black_bishops.append(self)
		
		self.set_attacked_points()
	
	def set_attacked_points(self):
		
		self.attacked_points = ()
		
		for attr_name in point_attr_name_list[1::2]:
			
			linked_point = getattr(self.point, attr_name)
			attacked_line = ()
			
			while linked_point:
				
				attacked_line += (linked_point, )
				linked_point = getattr(linked_point, attr_name)
			
			if attacked_line:
				
				self.attacked_points += (attacked_line, )
	
	def get_valid_moves(self):
		
		valid_moves = ()
		 
		for attacked_line in self.attacked_points:
			
			for linked_point in attacked_line:
				
				if not linked_point.state[0]:
					
					valid_moves += (linked_point, )
				
				elif linked_point.state[0] == self.opposite_piece_colour:
					
					valid_moves += ((linked_point, linked_point.piece), )
					
					break
				
				else:
					
					break
		
		return valid_moves


class Knight(Piece):
	
	def __init__(self, piece_colour, opposite_piece_colour, point):
		
		super().__init__(piece_colour, "knight", opposite_piece_colour, point)
		
		if self.piece_colour == "white":
			
			white_knights.append(self)
		
		else:
			
			black_knights.append(self)
		
		self.attacked_paths = (("top", "top_right"), ("top", "top_left"),
												("right", "top_right"), ("right", "bottom_right"),
												("bottom", "bottom_right"), ("bottom", "bottom_left"),
												("left", "bottom_left"), ("left", "top_left"))
		
		self.set_attacked_points()
	
	def set_attacked_points(self):
		
		self.attacked_points = ()
		
		for attacked_path in self.attacked_paths:
			
			linked_point = self.point
			
			for attr_name in attacked_path:
				
				linked_point = getattr(linked_point, attr_name)
				
				if not linked_point:
					
					break
			
			else:
				
				self.attacked_points += (linked_point, )
	
	def get_valid_moves(self):
		
		valid_moves = ()
		 
		for linked_point in self.attacked_points:
			
			if not linked_point.state[0]:
				
				valid_moves += (linked_point, )
			
			elif linked_point.state[0] == self.opposite_piece_colour:
				
				valid_moves += ((linked_point, linked_point.piece), )
		
		return valid_moves


class Rook(Piece):
	
	def __init__(self, piece_colour, opposite_piece_colour, point):
		
		super().__init__(piece_colour, "rook", opposite_piece_colour, point)
		
		if self.piece_colour == "white":
			
			white_rooks.append(self)
		
		else:
			
			black_rooks.append(self)
		
		self.set_attacked_points()
	
	def set_attacked_points(self):
		
		self.attacked_points = ()
		
		for attr_name in point_attr_name_list[::2]:
			
			linked_point = getattr(self.point, attr_name)
			attacked_line = ()
			
			while linked_point:
				
				attacked_line += (linked_point, )
				linked_point = getattr(linked_point, attr_name)
			
			if attacked_line:
				
				self.attacked_points += (attacked_line, )
	
	def get_valid_moves(self):
		
		valid_moves = ()
		 
		for attacked_line in self.attacked_points:
			
			for linked_point in attacked_line:
				
				if not linked_point.state[0]:
					
					valid_moves += (linked_point, )
				
				elif linked_point.state[0] == self.opposite_piece_colour:
					
					valid_moves += ((linked_point, linked_point.piece), )
					
					break
				
				else:
					
					break
		
		return valid_moves


class Pawn(Piece):
	
	def __init__(self, piece_colour, opposite_piece_colour, point):
		
		super().__init__(piece_colour, "pawn", opposite_piece_colour, point)
		
		if self.piece_colour == "white":
			
			white_pawns.append(self)
		
		else:
			
			black_pawns.append(self)
		
		self.forward = "top" if self.piece_colour == "white" else "bottom"
		self.set_attacked_points()
	
	def set_attacked_points(self):
		
		self.forward_point = getattr(self.point, self.forward)
		self.forward_forward_point = getattr(self.forward_point, self.forward) if self.forward_point else None
		self.attacked_points = [point for point in [point for point in (self.forward_point.left, self.forward_point.right) if self.forward_point] if point]
		
		self.promote_rank = 8 if self.piece_colour == "white" else 1
		self.can_promote = True if (self.point.board_cor[1] == 7 and self.promote_rank == 8) or (self.point.board_cor[1] == 2 and self.promote_rank == 1) else False
	
	def get_valid_moves(self):
		
		valid_moves = ()
		 
		 # Captures and capture promotions.
		 
		for linked_point in self.attacked_points:
			
			if linked_point.state[0] == self.opposite_piece_colour:
				
				valid_moves += ((linked_point, linked_point.piece) if not self.can_promote else (linked_point, linked_point.piece, "promote"), )
		
		# Normal pawn pushes and normal promotions.
		
		if self.forward_point and not self.forward_point.state[0]:
			
			valid_moves += (self.forward_point, ) if not self.can_promote else ((self.forward_point, "promote"), )
		
		# Double pawn pushes.
		
		if not self.has_moved and not self.forward_point.state[0] and self.forward_forward_point and not self.forward_forward_point.state[0]:
			
			valid_moves += (self.forward_forward_point, )
		
		# En passant.
		
		# To be implemented.
		
		return valid_moves


def init_promote_squad():
	
	


def bring_promote_squad(x, y):
	


# Returns nothing. Gets called when clicked on the screen.

def on_click(x1, y1):
	
	# If checks if the player clicked on a piece or anywhere else.
	
	if (-4 <= x1 / square_len < 4 and 0.5 * (square_len - side) <= abs(x1 % square_len) <= side + 0.5 * (square_len - side)) and (-4 < y1 / square_len < 4 and 0.5 * (square_len - side) <= abs(x1 % square_len) <= side + 0.5 * (square_len - side)):
		
		point = points[(7 - (int(y1 // square_len) + 4)) * 8 + (int(x1 // square_len) + 4)]
		
		# If checks if the user has already clicked on a piece or not.
		
		if not config.is_selected:
			
			# If the state of the point is not empty, then it calls the show_valid_moves function.
			
			if point.state[0] == config.turn:
				
				# Shows all the possible moves.
				
				config.valid_moves, config.valid_promotions, config.valid_captures, config.valid_castles = show_hint_moves(point.piece)
				
				# Sets the from point and from piece.
				
				config.from_point = point
				config.from_piece = point.piece
				
				# Flips the boolean.
				
				config.is_selected = True
					
				return
		
		# If it is in else it means that the player clicked on a piece before.
		
		else:
			
			# For takes each point in the valid moves list of the from piece.
			
			for to_point in config.valid_moves:
				
				# If checks if the clicked point is in the valid points to move. 
				
				if point.board_cor == to_point.board_cor:
					
					# Moves the piece and adds a count to the draw_move_count and adds the move to the appropriate list.
					
					move(config.from_piece, config.from_point, point, grey_dot_maker)
					config.draw_move_count = config.draw_move_count + 1 if config.from_piece.piece_type != "pawn" else 0
					add_move_to_draw_move_list(config.from_point, to_point)
					
					# Flips the boolean is_selected and the turn.
					
					config.is_selected = False
					flip_turn()
					
					# Sets the move in RDB.
					
					'''set_move(game_ID, config.from_piece, [point])'''
					
					# Checks if the game has ended.
					
					if check_game_end() != "IP":
						end_of_game(check_game_end()[0], check_game_end()[1])
					
					break
			
			# For takes each list of the point in the valid_jump_point_lists_list list of the from piece.
			
			for valid_promotion in config.valid_promotions:
				
				# Promotion_point is the point on which the piece can promote.
				
				promotion_point = valid_capture[0]
				
				# If checks if the clicked point is in the valid points to move. 
				
				if point.board_cor == promotion_point.board_cor:
					
					# Makes the pawn promote.
					
					promote(config.from_piece, config.from_point, valid_promotion, grey_dot_maker)
							
					# It flips the boolean is_selected and the turn.
					
					config.draw_move_count = 0
					config.is_selected = False
					flip_turn()
					
					# Sets the capture in RDB.
					
					'''set_move(game_ID, config.from_piece, config.to_moves, config.the_pieces_that_were_killed)
					config.to_moves = []
					config.the_pieces_that_were_killed = []'''
					
					# Checks if the game has ended.
					
					if check_game_end() != "IP":
						
						end_of_game(check_game_end()[0], check_game_end()[1])
					
					break
			
			# For takes each list of the point in the valid_jump_point_lists_list list of the from piece.
			
			for valid_capture in config.valid_captures:
				
				# Capture_point is the point on which the piece can capture and the captured_piece is the piece that will be captured.
				
				capture_point, captured_piece = valid_capture
				
				# If checks if the clicked point is in the valid points to move. 
				
				if point.board_cor == capture_point.board_cor:
					
					# Makes the piece capture.
					
					capture(config.from_piece, config.from_point, captured_piece, point, grey_dot_maker)
							
					# It flips the boolean is_selected and the turn.
					
					config.draw_move_count = 0
					config.is_selected = False
					flip_turn()
					
					# Sets the capture in RDB.
					
					'''set_move(game_ID, config.from_piece, config.to_moves, config.the_pieces_that_were_killed)
					config.to_moves = []
					config.the_pieces_that_were_killed = []'''
					
					# Checks if the game has ended.
					
					if check_game_end() != "IP":
						
						end_of_game(check_game_end()[0], check_game_end()[1])
					
					break
			
			for valid_castle in config.valid_castles:
				
				# Jump_point_index is the index of the point onto which the piece can jump and the kill_point_index is the index of the point of which the piece will be killed.
				
				castle_point, castle_rook, castle_rook_point = valid_castle
				
				# If checks if the clicked point is in the valid points to move. 
				
				if point.board_cor == castle_point.board_cor:
					
					# Makes the piece castle.
					
					castle(config.from_piece, config.from_point, castle_rook, castle_rook_point, point, grey_dot_maker)
							
					# It flips the boolean is_selected and the turn.
					
					config.draw_move_count += 1
					config.is_selected = False
					flip_turn()
					
					# Sets the capture in RDB.
					
					'''set_move(game_ID, config.from_piece, config.to_moves, config.the_pieces_that_were_killed)
					config.to_moves = []
					config.the_pieces_that_were_killed = []'''
					
					# Checks if the game has ended.
					
					if check_game_end() != "IP":
						
						end_of_game(check_game_end()[0], check_game_end()[1])
			
			# If it is not a valid point then it checks if the user clicked on the same piece again.
			
			if point.board_cor == config.from_point.board_cor:
				
				# It resets the hints.
				
				grey_dot_maker.clear()
				
				# Flips the boolean is_selected.
				
				config.is_selected = False
			
			# If none of the above conditions are it checks if the state of the point is the same as the from position.
			
			elif point.state[0] == config.from_point.state[0]:
				
				# Flips the boolean is_selected and calls the function again for the piece that the player clicked.
				
				config.is_selected = False
				on_click(x1, y1)


# Returns the valid moves and captures and other moves in a list of sorted tuples. Gets called if the user clicked on a piece.

def show_hint_moves(piece):
	
	valid_moves_and_captures = [(), (), (), ()]
	
	# Resets the hints.
	
	grey_dot_maker.clear()
	
	# For loop takes each valid move and makes a grey dot on that coordinate.
	
	for valid_move in piece.get_valid_moves():
		
		# Normal move.
		
		if isinstance(valid_move, Point):
			
			# Goes to the place to make the grey dot.
			
			#grey_dot_maker.color(board_colours[(valid_move.board_cor[0] + valid_move.board_cor[1]) % 2])
			
			grey_dot_maker.goto(valid_move.x, valid_move.y - radius)
			
			# Sorted addition of move.
			
			valid_moves_and_captures[0] += (valid_move, )
		
		# Promotion.
		
		elif valid_move[-1] == "promote":
			
			# Promotion_point is the point on which the pawn will promote.
			
			promotion_point = valid_move[0]
			
			# Goes to the place to make the grey dot.
			
			#grey_dot_maker.color(board_colours[(promotion_point.board_cor[0] + promotion_point.board_cor[1]) % 2])
			
			grey_dot_maker.goto(capture_point.x, capture_point.y - radius)
			
			# Sorted addition of move.
			
			valid_moves_and_captures[1] += (valid_move, )
		
		# Capture.
		
		elif len(valid_move) == 2:
				
			# Capture_point is the point on which the piece can capture.
			
			capture_point = valid_move[0]
			
			# Goes to the place to make the grey dot.
			
			#grey_dot_maker.color(board_colours[(capture_point.board_cor[0] + capture_point.board_cor[1]) % 2])
			
			grey_dot_maker.goto(capture_point.x, capture_point.y - square_len / 2)
			
			# Makes a grey dot where the piece can move.
			
			grey_dot_maker.pensize(board_brush_size)
			
			grey_dot_maker.pendown()
			
			grey_dot_maker.circle(square_len / 2)
			
			grey_dot_maker.penup()
			
			grey_dot_maker.pensize(1)
			
			# Sorted addition of capture.
			
			valid_moves_and_captures[2] += (valid_move, )
			
			continue
		
		# Castle.
		
		else:
			
			# Castle_point is the point where king goes when he castles.
			
			castle_point = valid_move[0]
			
			# Goes to the place to make the dot.
			
			#grey_dot_maker.color(board_colours[(castle_point.board_cor[0] + castle_point.board_cor[1]) % 2])
			
			grey_dot_maker.goto(castle_point.x, castle_point.y - radius)
			
			# Sorted addition of move.
			
			valid_moves_and_captures[3] += (valid_move, )
		
		# Makes a grey dot where the piece can move.
		
		grey_dot_maker.pendown()
		
		grey_dot_maker.begin_fill()
		grey_dot_maker.circle(radius)
		grey_dot_maker.end_fill()
		
		grey_dot_maker.penup()
		
	
	return valid_moves_and_captures


# Returns nothing. Moves the from_piece to the to_point.

def move(from_piece, from_point, to_point, hint_turtle_obj):
	
	# Sets the state of the point onto which the piece has moved.
	
	to_point.state = from_point.state
	to_point.piece = from_point.piece
	
	# Resets the hints and also sets the state and piece (that is on it) of the from point to empty.
	
	hint_turtle_obj.clear()
	from_point.state = [None, None]
	from_point.piece = ""
	
	from_piece.point = to_point
	from_piece.set_attacked_points()
	from_piece.has_moved = True
	
	# Makes the piece move.
	
	from_piece.goto(to_point.x, to_point.y)


# Returns nothing. Makes the piece capture another piece.

def capture(from_piece, from_point, captured_piece, to_point, hint_turtle_obj):
	
	config.to_moves.append(to_point)
	config.captured_pieces.append(captured_piece)
	
	# Sets the state of the point onto which the piece has moved.
	
	to_point.state = from_point.state
	to_point.piece = from_point.piece
	
	# Resets the hints and the kill piece and also sets the state of the from point and kill point to empty.
	
	hint_turtle_obj.clear()
	
	from_point.state = [None, None]
	from_point.piece = ""
	
	from_piece.point = to_point
	from_piece.set_attacked_points()
	from_piece.has_moved = True
	
	captured_piece.hideturtle()
	
	# Removes captured piece from any list to which it belongs and then deletes it.
	
	pieces_group.remove(captured_piece)
	
	if captured_piece.piece_colour == "white":
		white_pieces_group.remove(captured_piece)
	
	else:
		black_pieces_group.remove(captured_piece)
	
	del captured_piece
	
	# Makes the piece jump.
	
	from_piece.goto(to_point.x, to_point.y)


# Returns nothing. Makes the piece castle.

def castle(from_piece, from_point, castled_rook, castled_rook_point, castle_point, hint_turtle_obj):
	
	config.to_moves.append(castle_point)
	
	# Sets the state of the point onto which the piece has moved.
	
	castle_point.state = from_point.state
	castle_point.piece = from_point.piece
	
	castled_rook_point.state = castled_rook.point.state
	castled_rook_point.piece = castled_rook.point.piece
	
	# Resets the hints and the and also sets the state of the from point to None.
	
	hint_turtle_obj.clear()
	
	from_point.state = [None, None]
	from_point.piece = ""
	castled_rook.point.state = [None, None]
	castled_rook.point.piece = ""
	
	from_piece.point = castle_point
	from_piece.set_attacked_points()
	from_piece.has_moved = True
	
	castled_rook.point = castled_rook_point
	castled_rook.set_attacked_points()
	castled_rook.has_moved = True
	
	# Makes the piece castle.
	
	from_piece.goto(castle_point.x, castle_point.y)
	castled_rook.goto(castled_rook_point.x, castled_rook_point.y)


# Return nothing. Adds the move to the appropriate list.

def add_move_to_draw_move_list(from_point, to_point):

	config.draw_move_repetition_lists[config.list_to_add_move_in_draw_check].append([from_point, to_point])
	
	if len(config.draw_move_repetition_lists[config.list_to_add_move_in_draw_check]) == 2:
		
		if config.list_to_add_move_in_draw_check < 4:
			config.list_to_add_move_in_draw_check += 1
		
		else:
			config.list_to_add_move_in_draw_check = 0


# Returns nothing. Flips the turn.

def flip_turn():
	
	# Try tries to add the index of the turn in the turns and inserts the value into turn.
	
	try:
		
		config.turn = config.turns[config.turns.index(config.turn) + 1]
	
	# If an IndexError comes it means that the last index of the turns was the turn and had already been played by the player and that the turn must loop back to the 0th index of turns.
	
	except IndexError:
		
		config.turn = config.turns[0]


# Returns a list with 2 arguments: first one being one of the strings -> "IP" for in progress, "black" if black won, "draw" if the game is a draw and "white" if white won and second one being the reason for the game ending. Checks if game has ended by any player winning or by a draw or it is in progress.

def check_game_end():
	
	# If checks if the all the white or black pieces are eaten, and if they are it returns the other player's side.
	
#	if not white_pieces_group:
#		return ["black won", "killing all pieces"]
#	
#	elif not black_pieces_group:
#		return ["white won", "killing all pieces"]
	
	# If none of the above statements are true, it checks if the player has played the same move 5 times.
	
	if config.draw_move_repetition_lists[0] == config.draw_move_repetition_lists[2] == config.draw_move_repetition_lists[4] and config.draw_move_repetition_lists[1] == config.draw_move_repetition_lists[3]:
		return ["draw", "repetition"]
	
	# It lastly checks if the players have played 50 moves without a jump, and if one of this is true, then it returns draw.
	
	elif config.draw_move_count == 100:
		return ["draw", "50 move draw rule"]
	
	return "IP"


# Returns nothing. Makes the animation of white screen rolling from down to below and displays message saying that which side won.

def end_of_game(text, reason):
	
	# Animates the end white screen (moves it upwards from below the screen).
	
	while end_of_game_screen.ycor() < 0:
		
		end_of_game_screen.forward(0.75 * square_len)
		wn.update()
	
	# Lastly it stamps the white screen to allow turtle objects to write on it.
	
	end_of_game_screen.hideturtle()
	end_of_game_screen.clearstamps()
	end_of_game_screen.stamp()
	
	# It writes the text and the reason (for eg: white won = text and by killing all pieces = reason).
	
	end_result_writer.write(f"{text.capitalize()} by {reason.capitalize()}", True, "center", ("Arial", 15, "bold"))


# Returns nothing. Draws pieces on the board, given the FEN string.

def fen_string_decoder(fen_string):
	
	# Current rank and file.
	
	rank = -1
	file = 0
	
	# Loops through all the characters in the FEN string.
	
	for character in fen_string:
		
		# The index of the piece the letter represents.
		
		character_numbered = Piece.letter_to_num(character)
		
		# The next rank is considered if "/" is present.
		
		if character == "/":
			
			rank += 1
			file = 0
			continue
		
		# Piece is drawn if possible.
		
		elif character_numbered is not None:
			
			if character_numbered < 6:
				
				piece_colour = "white"
				opposite_piece_colour = "black"
			
			else:
				
				piece_colour = "black"
				opposite_piece_colour = "white"
			
			piece = piece_classes[character_numbered % 6](piece_colour, opposite_piece_colour, points[(rank * 8) + file])
			pieces_group.append(piece)
		
		# Else it means that the current character is a number and so it leaves that many files empty.
		
		else:
			
			file += int(character)
		
		file += 1
