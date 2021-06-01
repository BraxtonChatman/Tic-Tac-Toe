# Tic-Tac-Toe
# Author: Braxton Chatman
# Written: 1/16/2021
# Strategy from https://en.wikipedia.org/wiki/Tic-tac-toe


from random import random
from os import system

# list of tuples of straights that can be achieved
straights = [(0,1,2), (3,4,5), (6,7,8), (0,3,6), (1,4,7), (2,5,8), (0,4,8), (2,4,6)]

# If there is any straight of two in a row for the computer with an empty third space, that space will be 
# selected and 1 will be returned. If this is not possible, 0 will be returned.
def win(board):
    for straight in straights:
        if sum([board[i] for i in straight])==-2:
            for i in straight:
                if board[i]==0:
                    board[i]=-1
                    return 1
    return 0

# If the Player has a straight of two with an empty third, the computer will select the third space and the 
# function will return 1. If the Player does not have a straight of two, the function will return 0.
def block(board):
    for straight in straights:
        if sum([board[i] for i in straight])==2:
            for i in straight:
                if board[i]==0:
                    board[i]=-1
                    return 1
    return 0

# If there is any space that the computer can select to make a fork, it will be selected
# and the function will return 1. If no fork is possible, 0 will be returned.
def fork(board):
    for i in range(9):
        if board[i]==0:
            board[i]=-1
            if [sum([board[i] for i in straight]) for straight in straights].count(-2) > 1:
                return 1
            board[i]=0
    return 0

# If there are any spaces that the player could select to make a fork, then the
# computer will select a space that blocks the fork or forces the Player to select a different space and return 1. If the Player does not have an
# if player1 can fork, blocks the fork and returns 1, returns 0 if player1 can't fork
def blockFork(board):
    #find list of indices that player1 can make a fork by selecting
    forkList=[]
    for i in range(9):
        if board[i]==0:
            board[i]=1
            if [sum([board[i] for i in straight]) for straight in straights].count(2)>1:
                forkList.append(i)
            board[i]=0
    
    # if the Player can't make any forks, then return 0
    if forkList==[]:
        return 0

    #select the space that blocks the indices in the forkList
    for i in range(9):
        if board[i]==0:
            board[i]=-1
            for straight in straights:
                if sum([board[i] for i in straight])==-2:
                    for j in straight:
                        if board[j]==0 and (j not in forkList):
                            return 1
            board[i]=0
    print('Error in blockFork')
                    
# if the center space is not occupied, select it and return 1. else return 0
def center(board):
    if board[4]==0:
        board[4]=-1
        return 1
    return 0

# if player1 has marked a corner space, mark the opposite corner if it is empty
def oppositeCorner(board):
    for i in [0,2,6,8]:
        if board[i]==1 and board[8-i]==0:
            board[8-i]=-1
            return 1
    return 0
        
# if there is an available corner, select one
def corner(board):
    for i in [0,2,6,8]:
        if board[i]==0:
            board[i]=-1
            return 1
    return 0

# select a side
def side(board):
    for i in [1,3,5,7]:
        if board[i]==0:
            board[i]=-1
            return 1
    print('Error: no side was selected')

# print the game board
def printBoard(board):
    system('cls')
    playerDict = {1:'X', -1:'O', 0:'*'}
    for i in range(3):
        print(playerDict[board[3*i+0]], end=',')
        print(playerDict[board[3*i+1]], end=',')
        print(playerDict[board[3*i+2]])

# determine if either player has won: returns 1 for player1, -1 for player2, and 0 otherwise
def isOver(board):
    for straight in straights:
        if sum([board[i] for i in straight])==3:
            return 1
        if sum([board[i] for i in straight])==-3:
            return -1
    return 0

# prompts the player to make a move and selects their choice on the board
def playerMove(board):
    move = input('Please enter the value of the space you would like to select [0-8]: ')
    while True:
        if move not in [str(i) for i in range(9)]:
            move=input('Invalid value: please enter a number [0-8]: ')
        else:
            if board[int(move)]!=0:
                move=input('Invalid value: space already occupied, please enter a value [0-8]: ')
            else:
                move = int(move)
                break
        
    board[move] = 1
    printBoard(board)

# performs the computer's move, uses algorithm from tict-tac-toe wikipedia strategy section 
def computerMove(board):
    ticTacToeMoves = [win, block, fork, blockFork, center, oppositeCorner, corner, side]

    performed=0
    index=0
    while not performed:
        performed=ticTacToeMoves[index](board)
        index+=1
    
    printBoard(board)

# runs a Tic-tac-toe game where the user makes the first move
def playerFirst():
    board = [0]*9
    printBoard(board)
    playerMove(board)
    system('pause')

    while 0 in board:
        computerMove(board)
        if isOver(board):
            break

        playerMove(board)
        system('pause')
        if isOver(board):
            break
    
    return isOver(board)

# runs a Tic-tac-toe game where the computer makes the first move
def computerFirst():
    board = [0]*9
    x=random()
    if x>.5:
        board[0]=-1
    else:
        board[4]=-1
    printBoard(board)

    while 0 in board:
        playerMove(board)
        if isOver(board):
            break
        system('pause')

        computerMove(board)
        if isOver(board):
            break

    return isOver(board)

# runs the game
def runGame():
    playChoice=''
    playChoice=input('Would you like to go first[1] or second[2]?\n')
    options1=['1', 'first', 'f']
    options2=['2', 'second', 's']

    while playChoice.lower() not in options1+options2:
        playChoice=input('Invalid choice: please enter "1" to go first or "2" to go second\n')
        
    if playChoice in options1:
        winner=playerFirst()
    else:
        winner=computerFirst()

    if winner==1:
        print('You win!')
    elif winner==-1:
        print('CPU wins!')
    elif winner==0:
        print('It was a tie game.')

def main():
    system('cls')
    print('Welcome to Tic-Tac-Toe')
    print('The spaces are labeled: \n0|1|2\n3|4|5\n6|7|8')
    
    while True:
        runGame()

        #Prompt user if they would like to play again
        replay = ['yes', 'y', '1', '"yes"']
        noReplay = ['no', 'n', '0', '"no"']
        replayGame=input('Would you like to play Again (yes/no)?\n')
        while replayGame.lower() not in replay+noReplay:
            replayGame=input('Invalid answer: Enter "yes" to play again or "no" to exit: ' )
        
        #Exit loop
        if replayGame in noReplay:
            print('Thank you for playing!')
            break
        
if __name__=='__main__':
    main()
        