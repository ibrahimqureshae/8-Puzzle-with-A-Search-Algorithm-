from os import system
from copy import deepcopy
import time
goalState = [[1, 2, 3], [4, 0, 5], [6, 7, 8]]


class Node:

    def __init__(self, stateOfTheBoard: list, parentNode=None):
        self.stateOfTheBoard = stateOfTheBoard
        self.parentNode = parentNode
        self.g = 0
        self.h = self.eucilideanDistance(stateOfTheBoard, goalState)
        self.initializeG()

    def initializeG(self):

        if self.parentNode != None:
            self.g = self.parentNode.g+1

    def eucilideanDistance(self, stateOfTheBoard: list, goalState: list) -> int:
        cost = 0
        board_len = len(stateOfTheBoard)
        for i in range(board_len):
            for j in range(board_len):
                pos = self.getPosition(goalState, stateOfTheBoard[i][j])
                cost += abs(i - pos[0]) + abs(j - pos[1])  # Distance formulae
        return cost

    def getPosition(self, goalState: list, element):
        for i in range(len(goalState)):
            if element in goalState[i]:
                return (i, goalState[i].index(element))

    def calculateF(self):
        return self.g+self.h

    def getNeighbour(self):
        neighbours = []
        for i in range(4):
            temporaryState = deepcopy(self.stateOfTheBoard)
            position = findZero(temporaryState)
            X = position[0]
            Y = position[1]
            if (i == 0 and X != 0 and 0 <= X <= 2):
                up(X, Y, temporaryState)
            elif(i == 1 and X != 2 and 0 <= X <= 2):
                down(X, Y, temporaryState)
            elif(i == 2 and Y != 0 and 0 <= Y <= 2):
                left(X, Y, temporaryState)
            elif(i == 3 and Y != 2 and 0 <= Y <= 2):
                right(X, Y, temporaryState)
            else:
                continue
            neighbours += [Node(temporaryState, self)]
        return neighbours


def getBestNode(openList: list):
    firstIteration = True
    for item in openList.values():
        if firstIteration or item.calculateF() < bestF:
            firstIteration = False
            bestNode = item
            bestF = bestNode.calculateF()
    return bestNode


def AStar(currentState: list):
    openList = {str(currentState): Node(currentState)}  # non visited nodes
    closedList = {}  # visited nodes
    while len(openList) > 0:
        node = getBestNode(openList)
        closedList[str(node.stateOfTheBoard)] = node
        if node.stateOfTheBoard == goalState:
            printAnimate(node)
            return True
        neighbours = node.getNeighbour()
        for item in neighbours:
            if str(item.stateOfTheBoard) in closedList.keys() or str(item.stateOfTheBoard) in openList.keys() and openList[str(item.stateOfTheBoard)].calculateF() < item.calculateF():
                continue
            openList[str(item.stateOfTheBoard)] = item
        del openList[str(node.stateOfTheBoard)]
    return None


def generateParent(node):
    parentList = []
    while node != None:
        parentList.append(list(node.stateOfTheBoard))
        node = node.parentNode
    return parentList


def printAnimate(node):
    steps = node.g
    parentList = generateParent(node)

    for i in range(len(parentList)-1, -1, -1):
        time.sleep(.5)

        system('cls')
        print(f"Steps Taken : {steps}")
        for row in parentList[i]:
            for number in row:
                if(number == 0):
                    print(' ', end=' | ')
                else:
                    print(number, end=' | ')
            print()  # Goes to new line


def takeInput(numbers):
    system('cls')  # clears the whole screen
    userInput = list(map(int, input(" Enter a Sequence: ")))
    numbers[0] = userInput[0:3]
    numbers[1] = userInput[3:6]
    numbers[2] = userInput[6:9]
    solvable = checkSolvability(userInput)
    while(solvable == False):
        print("Puzzle is not Solvable, Enter a solvable sequence")
        time.sleep(1)
        takeInput(numbers)
        solvable = checkSolvability(userInput)


def checkSolvability(userInput):
    """Check whether the given puzzle is solvable or not"""
    count = 0
    for i in range(8):
        for j in range(i+1, 9):
            if userInput[j] and userInput[i] and userInput[i] > userInput[j]:
                count += 1

    return count % 2 == 0


def up(X, Y, numbers):
    """This function performs the Upward movement"""
    numbers[X][Y] = numbers[X-1][Y]
    numbers[X-1][Y] = 0


def down(X, Y, numbers):
    """This function performs the Downward movement"""
    numbers[X][Y] = numbers[X+1][Y]
    numbers[X+1][Y] = 0


def left(X, Y, numbers):
    """This function performs the left movement"""

    numbers[X][Y] = numbers[X][Y-1]
    numbers[X][Y-1] = 0


def right(X, Y, numbers):
    """This function performs the right movement"""

    numbers[X][Y] = numbers[X][Y+1]
    numbers[X][Y+1] = 0


def printBox(numbers):
    system('cls')
    for row in numbers:
        for number in row:
            if(number == 0):
                print(' ', end=' | ')
            else:
                print(number, end=' | ')
        print()  # Goes to new line


def findZero(numbers):

    Y = 0
    for x in range(0, len(numbers)):
        try:
            Y = numbers[x].index(0)
            break
        except:
            pass
    X = x

    return X, Y


def checkWin(numbers):

    if all(i in numbers for i in goalState):
        printBox(numbers)
        print("\nCongratulations You've Won!")
        return True
    else:
        printBox(numbers)
        return False


def main():
    numbers = [[0 for i in range(3)] for j in range(3)]
    takeInput(numbers)

    isWinner = AStar(numbers)
    if isWinner:
        exit()
    else:
        print("Loser")

    """ while(checkWin(numbers) == False):
        position = findZero(numbers)
        X = position[0]
        Y = position[1]
        keyInput = input("Press ( W , S , A , D )  For Directions: ").upper()
        if(keyInput == 'W'):
            if(X != 0 and 0 <= X <= 2):
                up(X, Y, numbers)
            else:
                printBox(numbers)
                pass

        if(keyInput == 'S'):
            if(X != 2 and 0 <= X <= 2):
                down(X, Y, numbers)
            else:
                printBox(numbers)
                pass

        if(keyInput == 'A'):
            if(Y != 0 and 0 <= Y <= 2):
                left(X, Y, numbers)
            else:
                printBox(numbers)
                pass

        if(keyInput == 'D'):
            if(Y != 2 and 0 <= Y <= 2):
                right(X, Y, numbers)
            else:
                printBox(numbers)
                pass

        if(keyInput == 'Z'):
            break """


if __name__ == "__main__":
    main()
