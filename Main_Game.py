try:
	
	#Pydroid run tkinter
	
	import turtle
	import config
	from config import *
	import Board
	from Coordinates import *
	import Piece
	
	#@profile
	def init_chess():
		
		point_definer()
		link_points()
		board1 = Board.Board("black", light_square_colour, dark_square_colour, board_brush_size)
		
		config.piece_classes += [Piece.King, Piece.Queen, Piece.Bishop,
													Piece.Knight, Piece.Rook, Piece.Pawn]
		Piece.fen_string_decoder("/rnbqkbnr/pppppppp/////PPPPPPPP/RNBQKBNR")
		
		wn.onscreenclick(Piece.on_click)
		
		while wn:
			
			if config.quit:
				
				break
			
			wn.update()
			
			#wn.onscreenclick(Piece.on_click)
			
			if config.promote_piece and config.promote_piece.shape() != "white queen":
				
				print(config.promote_piece.shape())
				pass
		
		#wn.update()
		
		wn.bye()
		
		return
		
	init_chess()

except turtle.Terminator:
	
	pass
