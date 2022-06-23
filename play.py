import chess
import chess.svg
import chess.engine
import random as r
from net import *
import numpy as np
import copy as copy
# from get_data import *



net = Net([64, 10, 20, 1])
piece_val_table = {"k":1.0, "q":0.7, "r":0.5, "b":0.3, "n":0.2, "p":0.1, ".":0.0, "K":-1.0, "Q":-0.7, "R":-0.5, "B":-0.3, "N":-0.2, "P":-0.1}


# bord = chess.Board()


def random_board(max_depth=200):
        board = chess.Board()
        depth = 3
        if r.randint(0,1) == 1:
            depth = r.randrange(0, max_depth)
        else:
            depth = r.randrange(0, 10)
        for _ in range(depth):
            all_moves = list(board.legal_moves)
            random_move = r.choice(all_moves)
            board.push(random_move)
            if board.is_game_over():
                break
        
        return board


# bord = random_board()
# print(bord)
# print(net.forward(net.board_to_ai_inp(bord))[0][0])

# def get_best_move(board):
#     pass

def minimax(net, board, depth, alpha, beta, maximizingplayer):
    if depth == 0 or board.is_checkmate() or board.is_stalemate():
        if board.is_checkmate():
            if maximizingplayer:
                return None, -np.inf
            else:
                return None, np.inf
        if board.is_stalemate():
            return None, 0
        return None, net.forward(net.board_to_ai_inp(board))[0][0]
    if maximizingplayer:
        maxEval = -np.inf
        bm = r.choice(list(board.legal_moves))
        for move in list(board.legal_moves):
            board.push(move)
            eval = minimax(net, board, depth-1, alpha, beta, False) [1]
            board.pop()
            if eval > maxEval:
                maxEval = eval
                bm = move
            # maxEval = max(maxEval, eval)
            alpha = max(alpha, eval)
            if beta <= alpha:
                break
        return bm, maxEval
    else:
        minEval = np.inf
        bm = r.choice(list(board.legal_moves))
        for move in list(board.legal_moves):
            board.push(move)
            eval = minimax(net, board, depth-1, alpha, beta, True) [1]
            board.pop()
            if eval < minEval:
                minEval = eval
                bm = move
            minEval = min(minEval, eval)
            beta = min(beta, eval)
            if beta <= alpha:
                break
        return bm, minEval

# print(minimax(net, bord, 4, -np.inf, np.inf, True))




def play_game(net1, net2):
    # net1.mutate(10)
    white_to_move = True
    b = chess.Board()
    ending = ""
    while ending == "":
        if white_to_move:
            res = minimax(net1, b, 2, -np.inf, np.inf, True)
            b.push(res[0])
            # print(res[0])
            white_to_move = not white_to_move
        else:
            res = minimax(net2, b, 2, -np.inf, np.inf, True)
            b.push(res[0])
            # print(res[0])
            white_to_move = not white_to_move
        
        # print(b)
        # print()
        if b.halfmove_clock > 99 or b.is_insufficient_material() or b.is_stalemate():
            ending = "draw"
        if b.is_checkmate():
            ending = f"win white: {white_to_move}"
    # print(b)
    return ending

# n1 = Net([64, 5, 8, 1])
# n2 = Net([64, 5, 8, 1])

# print(play_game(n1, n2))


def play_roster(net_list):
    score_list = [0 for i in range(len(net_list))]
    for n in net_list:
        no_list = net_list[:]
        no_list.remove(n)
        for m in no_list:
            end = play_game(n, m)
            if end == "win white: True":
                score_list[net_list.index(n)] = score_list[net_list.index(n)] + 1
            elif end == "win white: False":
                score_list[net_list.index(m)] = score_list[net_list.index(m)] + 1
            else:
                score_list[net_list.index(m)] = score_list[net_list.index(m)] + 0.5
                score_list[net_list.index(n)] = score_list[net_list.index(n)] + 0.5
    return score_list

n1 = Net([64, 5, 8, 1])
n2 = Net([64, 5, 8, 1])
n3 = Net([64, 5, 8, 1])
print(play_roster([n1, n2, n3]))

def evolve(cycles, num_nets):
    nets = []
    for i in range(num_nets):
        nets.append(Net([64, 5, 8, 1]))
    
    for c in range(cycles):
        res = play_roster(nets)
        best = nets[res.index(max(res))]
        # print(best)
        leng = len(nets)
        nets = [best]
        for i in range(leng-1):
            n = copy.deepcopy(best)
            n.mutate(0.01)
            nets.append(n)
        print(f"cycle: {c}")
        print(res)

evolve(10, 3)


# p = bord.piece_at(chess.D1)
# pies_sim = p.symbol()
# print(pies_sim)

# import pygame

# pygame.init()
# print(pygame.init())

# height = 600
# width = 800

# dark = (100, 50, 0)
# light = (235, 235, 100)

# clock = pygame.time.Clock()
# FPS = 60

# gameDisplay = pygame.display.set_mode((width, height))
# pygame.display.set_caption("base")

# pygame.display.update()

# gameExit = False

# while not gameExit:
#     for event in pygame.event.get():
#         # print(event)
#         if event.type == pygame.QUIT:
#             gameExit = True

#     gameDisplay.fill((0, 0, 0))

#     for i in range(8):
#         for j in range(8):
#             if (i+j)%2 == 0:
#                 pygame.draw.rect(gameDisplay, light, [width/8 * i, height/8 * j, width/8, height/8])
#             else:
#                 pygame.draw.rect(gameDisplay, dark, [width/8 * i, height/8 * j, width/8, height/8])

#     pygame.display.update()

#     clock.tick(FPS)

# pygame.quit()
# quit()