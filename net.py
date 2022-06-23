import random as r
import numpy as np
import math


# def act_func(x):
#     return max(x/2, x)

def act_func(x):
    return math.tanh(x)



class Net:
    def __init__(self, layers):
        self.vals = [np.zeros((layers[i],1)) for i in range(len(layers))]
        self.biases = [np.random.random_sample((layers[i],1)) * 2 - 1 for i in range(len(layers))]
        self.weights = [np.random.random_sample((layers[i+1], layers[i])) * 2 - 1 for i in range(len(layers)-1)]

    def forward(self, inp):
        for i in range(len(inp)):
            self.vals[0][i][0] = inp[i]

        for i in range(1, len(self.vals)):
            self.vals[i] = self.weights[i-1] @ self.vals[i-1]
            self.vals[i] = self.vals[i] + self.biases[i]
            for j in range(len(self.vals[i])):
                self.vals[i][j][0] = act_func(self.vals[i][j][0])
        return self.vals[-1]
    
    def mutate(self, factor):
        for k in range(len(self.weights)):
            for i in range(len(self.weights[k])):
                for j in range(len(self.weights[k][i])):
                    self.weights[k][i][j] = self.weights[k][i][j] + r.uniform(-factor, factor)
    

    def board_to_ai_inp(self, board):
        piece_val_table = {"k":1.0, "q":0.7, "r":0.5, "b":0.3, "n":0.2, "p":0.1, ".":0.0, "K":-1.0, "Q":-0.7, "R":-0.5, "B":-0.3, "N":-0.2, "P":-0.1}
        b = str(board)
        inp = []
        for i in range(len(b)):
            if b[i] in piece_val_table:
                inp.append(piece_val_table[b[i]])
        return inp
