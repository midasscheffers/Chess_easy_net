from network import *

import chess
import random as r

board = chess.Board()

cycles = 100
endings = []

for i in range(cycles):
    ending = ""
    players = ["white", "black"]
    turn_off = "white"
    board.reset()
    while ending == "":
        l_moves = list(board.legal_moves)
        rand_legal_move = r.choice(l_moves)
        board.push(rand_legal_move)
        # print(board)
        
        # switch turn
        if turn_off == "white":
            turn_off = players[1]
        else:
            turn_off = players[0]

        # check for win or draw
        if board.halfmove_clock > 99 or board.is_insufficient_material() or board.is_stalemate():
            ending = "draw"
        if board.is_checkmate():
            ending = "win " + turn_off
    endings.append(ending)


draws = endings.count("draw")
WW = endings.count("win white")
BW = endings.count("win black")

print(f"draw: {draws}, WW: {WW}, BW: {BW}")