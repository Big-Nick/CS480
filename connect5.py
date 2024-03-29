# Connect Five
#
# Connect 5 Module

import options
import random
import os
import time
from aiplayer import *


class Game(object):
    """ Game object that holds state of Connect 5 board and game values
    """

    board = None
    round = None
    finished = None
    winner = None
    turn = None
    players = [None, None]
    game_name = "Connect Five"
    colors = ["x", "o"]

    def __init__(self, players=None):
        self.round = 1
        self.finished = False
        self.winner = None

        if players is None:
            # Initialize via UI
            # do cross-platform clear screen
            os.system(['clear', 'cls'][os.name == 'nt'])
            print("Welcome to {0}!".format(self.game_name))
            print("Should Player 1 be a Human or a Computer?")
            while self.players[0] == None:
                choice = str(input("Type 'H' or 'C': "))
                if choice == "Human" or choice.lower() == "h":
                    name = str(input("What is Player 1's name? "))
                    self.players[0] = Player(name, self.colors[0])
                elif choice == "Computer" or choice.lower() == "c":
                    name = str(input("What is Player 1's name? "))
                    diff = int(input("Enter difficulty for this AI (1 - 4) "))
                    self.players[0] = AIPlayer(name, self.colors[0], diff+1)
                else:
                    print("Invalid choice, please try again")
            print("{0} will be {1}".format(
                self.players[0].name, self.colors[0]))

            print("Should Player 2 be a Human or a Computer?")
            while self.players[1] == None:
                choice = str(input("Type 'H' or 'C': "))
                if choice == "Human" or choice.lower() == "h":
                    name = str(input("What is Player 2's name? "))
                    self.players[1] = Player(name, self.colors[1])
                elif choice == "Computer" or choice.lower() == "c":
                    name = str(input("What is Player 2's name? "))
                    diff = int(input("Enter difficulty for this AI (1 - 4) "))
                    self.players[1] = AIPlayer(name, self.colors[1], diff+1)
                else:
                    print("Invalid choice, please try again")
            print("{0} will be {1}".format(
                self.players[1].name, self.colors[1]))
        else:
            players[0].setcolor(self.colors[0])
            players[1].setcolor(self.colors[1])
            self.players[0] = players[0]
            self.players[1] = players[1]
            print("{} playing as {} against {} as {}".format(self.players[0].name,
                                                             self.colors[0],
                                                             self.players[1].name,
                                                             self.colors[1]))
    # x always goes first (arbitrary choice on my part)
        self.turn = self.players[0]

        self.board = []
        for i in range(options.getRows()):
            self.board.append([])
            for j in range(options.getCols()):
                self.board[i].append(' ')

    def newGame(self):
        """ Function to reset the game, but not the names or colors
        """
        self.round = 1
        self.finished = False
        self.winner = None

        # x always goes first (arbitrary choice on my part)
        self.turn = self.players[0]

        self.board = []
        for i in range(options.getRows()):
            self.board.append([])
            for j in range(options.getCols()):
                self.board[i].append(' ')

    def switchTurn(self):
        if self.turn == self.players[0]:
            self.turn = self.players[1]
        else:
            self.turn = self.players[0]

        # increment the round
        self.round += 1

    def nextMove(self):
        player = self.turn

        # there are only so many legal places for pieces on the board
        # exactly one piece is added to the board each turn
        if self.round > getTotalCells():
            self.finished = True
            # this would be a stalemate :(
            return

        # move is the column that player want's to play
        move = player.move(self.board)

        print("Move = {}".format(move))

        for i in range(getRows()):
            if self.board[i][move] == ' ':
                self.board[i][move] = player.color
                self.switchTurn()
                self.checkForFives()
                self.printState()
                return

        # if we get here, then the column is full
        print("Invalid move (column is full)")
        return

    def checkForFives(self):
        # for each piece in the board...
        for i in range(options.getRows()):
            for j in range(options.getCols()):
                if self.board[i][j] != ' ':
                    # check if a vertical five-in-a-row starts at (i, j)
                    if self.verticalCheck(i, j):
                        self.finished = True
                        return

                    # check if a horizontal five-in-a-row starts at (i, j)
                    if self.horizontalCheck(i, j):
                        self.finished = True
                        return

                    # check if a diagonal (either way) five-in-a-row starts at (i, j)
                    # also, get the slope of the five if there is one
                    diag_fives, slope = self.diagonalCheck(i, j)
                    if diag_fives:
                        print(slope)
                        self.finished = True
                        return

    def verticalCheck(self, row, col):
        #print("checking vert")
        fiveInARow = False
        consecutiveCount = 0

        for i in range(row, getRows()):
            if self.board[i][col].lower() == self.board[row][col].lower():
                consecutiveCount += 1
            else:
                break

        if consecutiveCount >= 5:
            fiveInARow = True
            if self.players[0].color.lower() == self.board[row][col].lower():
                self.winner = self.players[0]
            else:
                self.winner = self.players[1]

        return fiveInARow

    def horizontalCheck(self, row, col):
        fiveInARow = False
        consecutiveCount = 0

        for j in range(col, options.getCols()):
            if self.board[row][j].lower() == self.board[row][col].lower():
                consecutiveCount += 1
            else:
                break

        if consecutiveCount >= 5:
            fiveInARow = True
            if self.players[0].color.lower() == self.board[row][col].lower():
                self.winner = self.players[0]
            else:
                self.winner = self.players[1]

        return fiveInARow

    def diagonalCheck(self, row, col):
        fiveInARow = False
        count = 0
        slope = None

        # check for diagonals with positive slope
        consecutiveCount = 0
        j = col
        for i in range(row, getRows()):
            if j > getRows():
                break
            elif self.board[i][j].lower() == self.board[row][col].lower():
                consecutiveCount += 1
            else:
                break
            j += 1  # increment column when row is incremented

        if consecutiveCount >= 5:
            count += 1
            slope = 'positive'
            if self.players[0].color.lower() == self.board[row][col].lower():
                self.winner = self.players[0]
            else:
                self.winner = self.players[1]

        # check for diagonals with negative slope
        consecutiveCount = 0
        j = col
        for i in range(row, -1, -1):
            if j > getRows():
                break
            elif self.board[i][j].lower() == self.board[row][col].lower():
                consecutiveCount += 1
            else:
                break
            j += 1  # increment column when row is decremented

        if consecutiveCount >= 5:
            count += 1
            slope = 'negative'
            if self.players[0].color.lower() == self.board[row][col].lower():
                self.winner = self.players[0]
            else:
                self.winner = self.players[1]

        if count > 0:
            fiveInARow = True
        if count == 2:
            slope = 'both'
        return fiveInARow, slope

    def findFives(self):
        """ Finds start i,j of five-in-a-row
            Calls highlightFives
        """

        for i in range(options.boardSize-1):
            for j in range(options.boardSize):
                if self.board[i][j] != ' ':
                    # check if a vertical five-in-a-row starts at (i, j)
                    if self.verticalCheck(i, j):
                        self.highlightFive(i, j, 'vertical')

                    # check if a horizontal five-in-a-row starts at (i, j)
                    if self.horizontalCheck(i, j):
                        self.highlightFive(i, j, 'horizontal')

                    # check if a diagonal (either way) five-in-a-row starts at (i, j)
                    # also, get the slope of the five if there is one
                    diag_fives, slope = self.diagonalCheck(i, j)
                    if diag_fives:
                        self.highlightFive(i, j, 'diagonal', slope)

    def highlightFive(self, row, col, direction, slope=None):
        """ This function enunciates five-in-a-rows by capitalizing
            the character for those pieces on the board
        """

        if direction == 'vertical':
            for i in range(5):
                self.board[row+i][col] = self.board[row+i][col].upper()

        elif direction == 'horizontal':
            for i in range(5):
                self.board[row][col+i] = self.board[row][col+i].upper()

        elif direction == 'diagonal':
            if slope == 'positive' or slope == 'both':
                for i in range(5):
                    self.board[row+i][col+i] = self.board[row+i][col+i].upper()

            elif slope == 'negative' or slope == 'both':
                for i in range(5):
                    self.board[row-i][col+i] = self.board[row-i][col+i].upper()

        else:
            print("Error - Cannot enunciate five-of-a-kind")

    def printState(self):
        # cross-platform clear screen
        os.system(['clear', 'cls'][os.name == 'nt'])
        print(u"{0}!".format(self.game_name))
        print("Round: " + str(self.round))

        for i in range(options.getRows()-1, -1, -1):
            print("\t", end="")
            for j in range(options.boardSize):
                print("| " + str(self.board[i][j]), end=" ")
            print("|")

        print("\t  ", end="")
        for j in range(options.boardSize):
            print("_", end="   ")
        print("")
        print("\t  ", end="")
        for j in range(options.boardSize):
            print(str(j+1), end="   ")
        print("")

        if self.finished:
            print("Game Over!")
            if self.winner != None:
                print(str(self.winner.name) + " is the winner")
            else:
                print("Game was a draw")

    def playGame(self, printGameState):
        while not self.finished:
            self.nextMove()

        self.findFives()
        if printGameState:
            self.printState()
        return self.winner
