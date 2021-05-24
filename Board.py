import turtle
from turtex import *
import config
from config import *


# All boards will be an instance of the Board class.

class Board(turtle.Turtle):
	
	def __init__(self, outline_colour, light_square_colour, dark_square_colour, brush_size):
		
		super().__init__()
		
		# Sets the board in config to itself.
		
		config.board = self
		
		# Initialises the properties.
		
		self.outline_colour = outline_colour
		self.light_square_colour = light_square_colour
		self.dark_square_colour = dark_square_colour
		self.line_thickness = brush_size
		
		# Sets self's properties.
		
		self.hideturtle()
		self.speed(0)
		self.pensize(self.line_thickness)
		
		# Draws the board.
		
		self.new_board()
	
	# Returns nothing. Creates a new board.
	
	def new_board(self):
		
		# Goes to the bottom left of the board.
		
		self.penup()
		self.goto(-4 * square_len, -4 * square_len)
		self.pendown()
		
		# Files loop.
		
		for y in range(8):
			
			# Ranks loop.
			
			for x in range(8):
				
				self.setheading(0)
				
				# Sets the color for each square.
				
				if (y + x) % 2 == 0:
					
					self.color(self.outline_colour, self.dark_square_colour)
				
				else:
					
					self.color(self.outline_colour, self.light_square_colour)
				
				# Each square of the rank
				
				self.begin_fill()
				drawpoly(4, square_len,  self)
				self.end_fill()
				
				if x != 7:
					
					self.forward(square_len)
			
			# Changes rank after each sub-loop.
			
			self.penup()
			self.goto(-4 * square_len, (y - 3) * square_len)
			self.pendown()
