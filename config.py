from PIL import Image, ImageTk
import turtle
import pygame
#import math
#import json
import cProfile, pstats, io

quit = False


def profile(fnc):
	
	def inner(*args, **kwargs):
	 	
		profile = cProfile.Profile()
		profile.enable()
		
		for _ in range(100):
			
			retval = fnc(*args, **kwargs)
		
		profile.disable()
		
		s = io.StringIO()
		
		sortby = 'cumulative'
		ps = pstats.Stats(profile, stream=s).sort_stats(sortby)
		ps.print_stats()
		
		with open("lol.txt", "w") as f:
			f.write((s.getvalue()))
			#print(s.getvalue())
		
		global quit
		
		#quit = True
		
		return retval
	
	return inner

turtle.colormode(255)

# Window setup.

wn = turtle.Screen()
wn_len = 2000
wn_height = 1400
wn.title("Chess")
wn.bgcolor((225,)*3)
wn.tracer(0)
wn.setup(wn_len, wn_height, 0, 0)

images_path = "Imgs/"
sounds_path = "Sounds/Standard/"

pygame.mixer.init()
move_sound = pygame.mixer.Sound(f"{sounds_path}Move.mp3")
capture_sound = pygame.mixer.Sound(f"{sounds_path}Capture.mp3")
#castle_sound = pygame.mixer.Sound(f"{sounds_path}Castle.mp3")

# Background

Image.open(f"{images_path}Background.gif").resize((wn_len, wn_height), Image.ANTIALIAS).save(f"{images_path}Background.gif")
#wn.bgpic("Background.gif")

# Square length and triangle length.

# If checks if the window length is greater than or less than 720 and sets the square length accordingly.

if wn_height < 1500:
	square_len = wn_height / 10

# Else sets the square length to the maximum value of 150.

else:
	square_len = 150

# All the pieces and coordinates are in these lists.

points = []
pieces_group = []

white_pieces_group = []
white_king_piece = None
white_queens = []
white_bishops = []
white_knights = []
white_rooks = []
white_pawns = []

black_pieces_group = []
black_king_piece = None
black_queens = []
black_bishops = []
black_knights = []
black_rooks = []
black_pawns = []

# Used for linking the points and generating valid moves.

point_attr_name_list = ["top", "top_right", "right", "bottom_right", "bottom", "bottom_left", "left", "top_left"]
point_attr_value_list = [(-1, 0), (-1, 1), (0, 1), (1, 1), (1, 0), (1, -1), (0, -1), (-1, -1)]

# List of instances of different pieces. Used for decoding fen strings.

piece_classes = []

#triangle_len = math.sqrt(2 * square_len * square_len)

num_to_file = {
	1: "A",
	2: "B",
	3: "C",
	4: "D",
	5: "E",
	6: "F",
	7: "G",
	8: "H"
}

# Board.

board = None
light_square_colour = (245, 222, 179)
dark_square_colour = (150, 120, 87)
board_colours = [light_square_colour, dark_square_colour]
board_brush_size = square_len / 30

# Game_ID and Game_ID_writer.

# Game_ID is the current game going on.

#game_ID = len(rdb)

game_ID_writer = turtle.Turtle()
game_ID_writer.hideturtle()
game_ID_writer.penup()

#game_ID_writer.goto(0, 4.5 * square_len)

#game_ID_writer.write(game_ID, True, align="center", font=("Arial", 15, "normal"))

# Valid_moves is just the list of points that a piece can move to.

valid_moves = []
draw_move_count = 0
draw_move_repetition_lists = [[], [], [], [], []]
list_to_add_move_in_draw_check = 0

# Jump stuff.

# Valid_jump_point_list_list is just the list of lists of indices of jumps that a piece can do and the kill points.

valid_captures = []
to_moves = []
captured_pieces = []

valid_castles = []

valid_promotions = []

promote_piece = None

# Is_selected is just a toggleable boolean. it is used for checking if the user has already clicked on a piece or not.

is_selected = False

# Pieces.

# Radius of pieces and the piece_types.

radius = square_len * 0.27
side = int(square_len * 0.85)
piece_types = ["white", "black"]

# Adds pieces images.

white_king = ImageTk.PhotoImage(Image.open(f"{images_path}white king.png").resize((side, side)))
wn.addshape("white king", turtle.Shape("image", white_king))

white_queen = ImageTk.PhotoImage(Image.open(f"{images_path}white queen.png").resize((side, side)))
wn.addshape("white queen", turtle.Shape("image", white_queen))

white_bishop = ImageTk.PhotoImage(Image.open(f"{images_path}white bishop.png").resize((side, side)))
wn.addshape("white bishop", turtle.Shape("image", white_bishop))

white_knight = ImageTk.PhotoImage(Image.open(f"{images_path}white knight.png").resize((int(side * 0.95), int(side * 0.95))))
wn.addshape("white knight", turtle.Shape("image", white_knight))

white_rook = ImageTk.PhotoImage(Image.open(f"{images_path}white rook.png").resize((int(side * 0.85), int(side * 0.95))))
wn.addshape("white rook", turtle.Shape("image", white_rook))

white_pawn = ImageTk.PhotoImage(Image.open(f"{images_path}white pawn.png").resize((int(side * 0.8), int(side * 0.95))))
wn.addshape("white pawn", turtle.Shape("image", white_pawn))

black_king = ImageTk.PhotoImage(Image.open(f"{images_path}black king.png").resize((side, side)))
wn.addshape("black king", turtle.Shape("image", black_king))

black_queen = ImageTk.PhotoImage(Image.open(f"{images_path}black queen.png").resize((side, side)))
wn.addshape("black queen", turtle.Shape("image", black_queen))

black_bishop = ImageTk.PhotoImage(Image.open(f"{images_path}black bishop.png").resize((side, side)))
wn.addshape("black bishop", turtle.Shape("image", black_bishop))

black_knight = ImageTk.PhotoImage(Image.open(f"{images_path}black knight.png").resize((int(side * 0.95), int(side * 0.95))))
wn.addshape("black knight", turtle.Shape("image", black_knight))

black_rook = ImageTk.PhotoImage(Image.open(f"{images_path}black rook.png").resize((int(side * 0.85), int(side * 0.95))))
wn.addshape("black rook", turtle.Shape("image", black_rook))

black_pawn = ImageTk.PhotoImage(Image.open(f"{images_path}black pawn.png").resize((int(side * 0.8), int(side * 0.95))))
wn.addshape("black pawn", turtle.Shape("image", black_pawn))

promote_squad = []

# From Piece and from point.

from_piece = ""
from_point = ""

# Stamp maker.

stamp_maker = turtle.Turtle()
stamp_maker.hideturtle()
stamp_maker.penup()

# End of game screen object.

end_of_game_screen = turtle.Turtle()
end_of_game_screen.speed(0)
end_of_game_screen.setheading(90)

end_of_game_screen.shape("square")
end_of_game_screen.color("white")
end_of_game_screen.shapesize(50)

end_of_game_screen.penup()
end_of_game_screen.goto(0, -11 * square_len)

# End result writer.

end_result_writer = turtle.Turtle()
end_result_writer.hideturtle()
end_result_writer.goto(0, 2 * square_len)

# Grey dot maker.

grey_dot_maker = turtle.Turtle()
grey_dot_maker.alpha = 0.7
#light_square_colour = (245, 222, 179)
#dark_square_colour = (150, 120, 87)
#r = int(245 * (1 - grey_dot_maker.alpha) + 115 * grey_dot_maker.alpha)
#g = int(222 * (1 - grey_dot_maker.alpha) + 115 * grey_dot_maker.alpha)
#b = int(179 * (1 - grey_dot_maker.alpha) + 115 * grey_dot_maker.alpha)
grey_dot_maker.color((154, 147, 134), (154, 147, 134))
grey_dot_maker.shape("circle")
grey_dot_maker.shapesize(radius/10)
grey_dot_maker.hideturtle()
grey_dot_maker.penup()

# Game starts with white.

turns = ["white", "black"]
turn = "white"
