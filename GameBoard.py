import numpy as np
import math
import copy
class GameBoard:

    def __init__(self,board=None):
        if board == None:
            self.squares = [[0,0,0] for _ in range(3)]
        else:
            self.squares = board
        self.playerOneToken = 1
        self.playerTwoToken = 2
        self.blank = 0

    def check_win(self,token):
        #Check horizontal
        for i in range(3):
            if self.squares[i][0] == token and  self.squares[i][1] == token and self.squares[i][2] == token:
                    return True
        #Check Vertical
        for i in range(3):
            if self.squares[0][i] == token and self.squares[1][i] == token and self.squares[2][i] == token  :
                return True
        #Check diagonal

        if self.squares[0][0] == token and self.squares[1][1] == token and self.squares[2][2] == token:
            return True
        if self.squares[0][2] == token and self.squares[1][1] ==token and self.squares[2][0] == token:
            return True

        return False

    def set_board(self,board):
        self.board = board

    def play(self,square,token,inplace=True):
        r,c = square
        if inplace:
            if self.squares[r][c] == self.blank:
                self.squares[r][c] = token

            else:
                print("Error, square already played!")
        else:
            gb = GameBoard(board = self.squares)
            if gb.squares[r][c] == gb.blank:
                gb.squares[r][c] = token
                return gb




    def terminal_test(self):
        if self.check_win(self.playerOneToken) or self.check_win(self.playerTwoToken):
            return True
        else:
            for row in self.squares:
                for token in row:
                    if token == 0:
                        return False
        return True

    def utility(self):
        if not self.terminal_test():
            return 0
        else:
            if self.check_win(1):
                return -10
            elif self.check_win(2):
                return 10
            else:
                return 0

class GameAgent:

    def __init__(self,token=2):
        self.token = token
        self.opponent_token = 1 if token == 2 else 2
    def possible_actions(self,gameboard,token):
        possible_moves = []
        for idx_r,row in enumerate(gameboard.squares):
            for idx_c,square in enumerate(row):
                if square == 0:
                    b = copy.deepcopy(gameboard.squares)
                    ngb = GameBoard(board=b)
                    ngb.play((idx_r,idx_c),token)
                    possible_moves.append(ngb)
        return possible_moves


    def min_value(self,gameboard):
        if gameboard.terminal_test():
            #print(gameboard.squares,gameboard.utility(),gameboard.terminal_test())
            return gameboard.utility()
        v = math.inf
        possible_moves = self.possible_actions(gameboard,self.opponent_token)
        for move in possible_moves:
            v = min(v,self.max_value(move))
        return v

    def max_value(self,gameboard):
        if gameboard.terminal_test():
            #print(gameboard.squares,gameboard.utility(),gameboard.terminal_test())
            return gameboard.utility()

        v = -math.inf
        possible_moves = self.possible_actions(gameboard,self.token)
        for move in possible_moves:
            v = max(v,self.min_value(move))
        return v



    def minmax_decision(self,gameboard):

        possible_moves = self.possible_actions(gameboard,self.token)
        possible_moves_v = []
        for x in possible_moves:
            g = gameboard

            possible_moves_v.append((x.squares,self.min_value(x)))
        #import pdb; pdb.set_trace()
        best_value = -math.inf
        best_action = None

        for move in possible_moves_v:
            action,value = move
            if value > best_value:
                best_value = value
                best_action = action
        return best_action


if __name__ == "__main__":
    board = GameBoard()
    token = 1 #Player is 1, AI is 2
    agent = GameAgent()


    while not board.terminal_test():
        for row in board.squares:
            print(row)
        if token == 1:
            print("Turn of player",token)
            sq = int(input("Enter square from 1 to 9:"))
            sq_r = sq // 3
            sq_c = sq % 3
            board.play((sq_r,sq_c),token)

            if board.check_win(token):
                print("Player",token,"has won!")

            token = (token % 2) + 1
        elif token == 2:
            print("Turn of AI")
            move = agent.minmax_decision(board)
            board.squares = move
            #print(move.squares)
            if board.check_win(token):
                print("AI has won!")
            token = (token % 2) + 1
