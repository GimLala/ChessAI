from config import *
#import config


# Every (centre point of a) square will be an instance of the point class.

class Point:
	
	def __init__(self, board_cor, x_cor, y_cor, chess_cor, list_cor):
		
		self.board_cor = board_cor
		self.x = x_cor
		self.y = y_cor
		self.state = [None, None]
		self.piece:any = ""
		self.chess_cor = chess_cor
		self.list_cor = list_cor
	
	@classmethod
	def instantiate_without_chess_cor(cls, board_cor, x_cor, y_cor, list_cor):
		
		chess_cor = f"{num_to_file[board_cor[0]]}{board_cor[1]}"
		
		return cls(board_cor, x_cor, y_cor, chess_cor, list_cor)


# Returns nothing. Defines all the points on the board (37). Appends the points to the list point_and_cor.

def point_definer():
	
	# Offset of 0.5 to make the point in the center of the square.
	
	x_cor = [(x + 0.5) * square_len for x in range(-4, 5)]
	y_cor = x_cor[:]
	
	# Outer loop is for the y coordinates.
	
	for y in range(8, 0, -1):
		
		# Inner loop is for the x coordinates.
		
		for x in range(1, 9):
			
			board_cor = (x, y)
			x_cor = (x - 4.5) * square_len
			y_cor = (y - 4.5) * square_len
			list_cor = (8 - y, x - 1)
						
			point = Point.instantiate_without_chess_cor(board_cor, x_cor, y_cor, list_cor)
			points.append(point)


def link_points():
	
	for point in points:
		
		rank, file = point.list_cor
		
		for (attr_name, (attr_value_rank, attr_value_file)) in tuple(zip(point_attr_name_list, point_attr_value_list)):
			
			new_rank = rank + attr_value_rank
			new_file = file + attr_value_file
			
			if -1 < new_rank < 8 and -1 < new_file < 8:
				
				setattr(point, attr_name, points[(new_rank * 8) + new_file])
			
			else:
				
				setattr(point, attr_name,  None)
