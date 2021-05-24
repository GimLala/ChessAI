try:
	
	#Pydroid run tkinter
	
	import turtle
	import config
	from config import *
	import Board
	from Coordinates import *
	import Piece
	import cProfile, pstats, io
	
	def profile(fnc):
	    
	    def inner(*args, **kwargs):
	        
	        profile = cProfile.Profile()
	        profile.enable()
	        retval = fnc(*args, **kwargs)
	        profile.disable()
	        
	        s = io.StringIO()
	        
	        sortby = 'cumulative'
	        ps = pstats.Stats(profile, stream=s).sort_stats(sortby)
	        ps.print_stats()
	        
	        with open("lol.txt", "w") as f:
	        	f.write((s.getvalue()))
	        #print(s.getvalue())
	        
	        return retval
	
	    return inner
	
	
	@profile
	def init_chess():
		
		point_definer()
		link_points()
		board1 = Board.Board("black", light_square_colour, dark_square_colour, board_brush_size)
		
		config.piece_classes += [Piece.King, Piece.Queen, Piece.Bishop,
													Piece.Knight, Piece.Rook, Piece.Pawn]
		Piece.fen_string_decoder("/rnbqkbnr/pppppppp/////PPPPPPPP/RNBQKBNR")
		
		wn.onscreenclick(Piece.on_click)
		
		while True:
			wn.update()
		
		#wn.update()
		
	init_chess()

except turtle.Terminator:
	
	pass
