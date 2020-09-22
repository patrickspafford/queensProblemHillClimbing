from copy import deepcopy
from operator import attrgetter
import random
import math
import sys

class Coordinate():
    x, y = 0, 0
    def __init__(self, x, y):
        self.x = x
        self.y = y

class State():
    board = []
    fitness = 0
    def __init__(self, board, fitness):
        self.board = board
        self.fitness = fitness

queens = []

def defineQueens(size = 25):
    for index in range(size):
        queens.append(index)

def getMatchingColumns(queens, value):
    matches = []
    for index in range(len(queens)):
        if queens[index] == value and index not in matches:
            matches.append(index)
    return matches
 # 15, 22, 23   
def getPairsInSameRow(queens):
    valueDict, pairs = {}, []
    for index in range(len(queens)):
        valueDict[str(index)] = 0
    for queen in queens:
        valueDict[str(queen)] += 1
    for key in valueDict:
        if valueDict[key] > 1:
            matches = getMatchingColumns(queens, int(key))
            pairs = pairs + matches
    return pairs


def getDiagonalPairs(queens, pairsInSameRow):
    count = 0  # index from bottom left
    conflicts_list = deepcopy(pairsInSameRow)
    maxIndex = len(queens) - 1
    for queen in queens:
        countAdded = count in pairsInSameRow
        queen_coord = Coordinate(x = count, y = queen)
        newX = queen_coord.x
        newY = queen_coord.y
        while newX > 0 and newY < maxIndex: # top left diagonal
            newX -= 1
            newY += 1
            temp_queen = Coordinate(x = newX, y = newY)
            if queens[temp_queen.x] == temp_queen.y and temp_queen.x not in conflicts_list:
                conflicts_list.append(temp_queen.x)
                if not countAdded and count not in conflicts_list:
                    conflicts_list.append(count)
                    countAdded = True
        newX = queen_coord.x
        newY = queen_coord.y
        while newX > 0 and newY > 0: # bottom left
            newX -= 1
            newY -= 1
            temp_queen = Coordinate(x = newX, y = newY)
            if queens[temp_queen.x] == temp_queen.y and temp_queen.x not in conflicts_list:
                conflicts_list.append(temp_queen.x)
                if not countAdded and count not in conflicts_list:
                    conflicts_list.append(count)
                    countAdded = True
        newX = queen_coord.x
        newY = queen_coord.y
        while newX < maxIndex and newY > 0: # bottom right
            newX += 1
            newY -= 1
            temp_queen = Coordinate(x = newX, y = newY)
            if queens[temp_queen.x] == temp_queen.y and temp_queen.x not in conflicts_list:
                conflicts_list.append(temp_queen.x)
                if not countAdded and count not in conflicts_list:
                    conflicts_list.append(count)
                    countAdded = True
        newX = queen_coord.x
        newY = queen_coord.y
        while newX < maxIndex and newY < maxIndex: # top right
            newX +=  1
            newY += 1
            temp_queen = Coordinate(x = newX, y = newY)
            if queens[temp_queen.x] == temp_queen.y and temp_queen.x not in conflicts_list:
                conflicts_list.append(temp_queen.x)
                if not countAdded and count not in conflicts_list:
                    conflicts_list.append(count)
        count += 1
    return conflicts_list

def conflictingPairs(queens):
    pairs = getPairsInSameRow(queens)
    pairs = getDiagonalPairs(queens, pairs)
    return len(pairs)

def getNeighbors(current_state):
    nbrs = []
    board = current_state.board
    maxIndex = len(board) - 1
    column = 0
    for queen in board:
        nbr_value = deepcopy(queen)
        while nbr_value > 0:
            nbr = deepcopy(board)
            nbr_value -= 1
            nbr[column] = nbr_value
            nbrs.append(State(nbr, conflictingPairs(nbr)))
        nbr_value = deepcopy(queen)
        while nbr_value < maxIndex:
            nbr = deepcopy(board)
            nbr_value += 1
            nbr[column] = nbr_value
            nbrs.append(State(nbr, conflictingPairs(nbr)))
        column += 1
    return nbrs

def hillClimbing(initial_board):
    fitnessCeiling = 10
    current = State(initial_board, conflictingPairs(initial_board))
    repeatedFitness = 0
    while True:
        neighbors = getNeighbors(current)
        best_neighbor = min(neighbors, key = attrgetter('fitness'))
        print(best_neighbor.board, best_neighbor.fitness)
        if current.fitness < best_neighbor.fitness:
            print('Solved!', current.fitness, current.board)
            return current
        elif current.fitness == best_neighbor.fitness:
            repeatedFitness += 1
            if repeatedFitness >= fitnessCeiling:
                print('Got stuck!', current.fitness, current.board)
                return current
        else:
            repeatedFitness = 0
        current = deepcopy(best_neighbor)

def singleRandomResetHillClimb(board):
    fitnessCeiling = 10
    current = State(board, conflictingPairs(board))
    repeatedFitness = 0
    while True:
        neighbors = getNeighbors(current)
        best_neighbor = min(neighbors, key = attrgetter('fitness'))
        print(best_neighbor.board, best_neighbor.fitness)
        if current.fitness == 0:
            print('Solved!')
            return current
        elif current.fitness == best_neighbor.fitness:
            repeatedFitness += 1
            if repeatedFitness >= fitnessCeiling:
                print('Got stuck!')
                return current
        else:
            repeatedFitness = 0
        current = deepcopy(best_neighbor)
def randomResetHillClimbing(initial_board):
    board = deepcopy(initial_board)
    numberIterations = 0
    fitness = 25
    while fitness != 0:
        current = singleRandomResetHillClimb(board)
        fitness = current.fitness
        print(fitness)
        random.shuffle(board)
        numberIterations +=1
        print(f'Iterations so far: {numberIterations}')
    print('Solved!')
    print(current.board, current.fitness)


def schedule(time):
    return 6000 / (time ** 4 + 0.01)

def simulatedAnnealing(board, schedule):
    current = State(board, conflictingPairs(board))
    iterations = 0
    for t in range(sys.maxsize ** 10):
        T = schedule(t)
        if T <= 0.000001:
            print(iterations, current.fitness, current.board)
            return current
        neighbors = getNeighbors(current)
        successor = random.choice(neighbors)
        changeInE = current.fitness - successor.fitness
        if changeInE > 0:
            current = successor
        else:
            probability = math.e ** (changeInE / T)
            shouldAccept = random.random() < probability
            if shouldAccept:
                current = successor
        iterations += 1
        print(iterations)
    


defineQueens()
# hillClimbing(queens)
# randomResetHillClimbing(queens)
simulatedAnnealing(queens, schedule)


    
    

