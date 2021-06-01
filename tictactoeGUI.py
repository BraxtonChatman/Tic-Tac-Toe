import tkinter as tk

root=tk.Tk()
root.title('Tic-Tac-Toe')

### Board ##################################################################################################
selectedSpace = -1
board = [0]*9
playerTurn=1


### Command Functions ######################################################################################

#clickReset clears the board to restart the game
def clickReset():
    global board
    global selectedSpace
    global buttonList
    global playerTurn
    global winLabel

    # reset the winLabel to be blank
    winLabel.grid_forget()
    winLabel=tk.Label(root)
    winLabel.grid(row=4, columnspan=3)

    # reset the board to be empty and the selectedSpace to be -1, and the space buttons to unselected
    board=[0]*9
    selectedSpace=-1
    for i in range(9):
        newButton=tk.Button(root, command=lambda i=i:clickSpace(i), padx=40, pady=40, borderwidth=3)
        newButton.grid(row=1+i//3, column=i%3, padx=1, pady=1)
        buttonList.append(newButton)
    
    # if player is gong second, have computer make a move
    if playerTurn==2:
        computerMove(board)

# clickSpace is the command function for the buttons in the tic-tac-toe grid. 
# it highlights and disables the selected button and reactivates the previously selected button
# the selected button is finalized with clickNext
def clickSpace(spaceIndex):
    global selectedSpace
    global buttonList
    global board

    if not isOver(board):
        # If selected button isn't already clicked
        if board[spaceIndex]==0:
            # After first click reset selected button to default state
            if selectedSpace!=-1: 
                buttonList[selectedSpace] = tk.Button(root, command=lambda x=selectedSpace:clickSpace(x), padx=40, pady=40, borderwidth=3)
                buttonList[selectedSpace].grid(row=1+selectedSpace//3, column=selectedSpace%3, padx=1, pady=1)
                board[selectedSpace]=0
            
            # Update selectedSpace and corresponding button
            selectedSpace=spaceIndex
            board[selectedSpace]=1

            buttonList[selectedSpace] = tk.Button(root, state='disabled', bg='red', padx=40, pady=40)
            buttonList[selectedSpace].grid(row=1+selectedSpace//3, column=selectedSpace%3, padx=1, pady=1)

# clickNext confirms the selection made in clickSpace
def clickNext():
    global selectedSpace
    global buttonList
    global board

    if selectedSpace!=-1:
        board[selectedSpace]=1
        selectedSpace=-1

        if 0 in board and not isOver(board):
            computerMove(board)

# clickFirst resets the game and has lets the player make the first move
def clickFirst():
    global playerFirstButton
    global playerTurn
    playerTurn=1
    clickReset()
    playerFirstButton.grid_forget()
    playerSecondButton=tk.Button(root, text='Go Second', command=clickSecond)
    playerSecondButton.grid(row=5, column=1)

# clickSecond resets the game and has the computer make a first move
def clickSecond():
    global playerSecondButton
    global playerTurn
    playerTurn=2
    clickReset()
    playerSecondButton.grid_forget()
    playerFirstButton=tk.Button(root, text='Go First',padx=9, command=clickFirst)
    playerFirstButton.grid(row=5, column=1)


### Tic-Tac-Toe Functions #################################################################################
from random import randint

# list of tuples of straights that can be achieved
straights = [(0,1,2), (3,4,5), (6,7,8), (0,3,6), (1,4,7), (2,5,8), (0,4,8), (2,4,6)]

# If there is any straight of two in a row for the computer with an empty third space, that space will be 
# selected and 1 will be returned. If this is not possible, 0 will be returned.
def win(board):
    global buttonList
    global winLabel

    for straight in straights:
        if sum([board[i] for i in straight])==-2:
            for i in straight:
                if board[i]==0:
                    board[i]=-1
                    buttonList[i] = tk.Button(root, state='disabled', bg='blue', padx=40, pady=40)
                    buttonList[i].grid(row=1+i//3, column=i%3, padx=1, pady=1)
                    winLabel = tk.Label(root, text='You Lose!')
                    winLabel.grid(row=4, columnspan=3)
                    return 1
    return 0

# If the Player has a straight of two with an empty third, the computer will select the third space and the 
# function will return 1. If the Player does not have a straight of two, the function will return 0.
def block(board):
    global buttonList
    for straight in straights:
        if sum([board[i] for i in straight])==2:
            for i in straight:
                if board[i]==0:
                    board[i]=-1
                    buttonList[i] = tk.Button(root, state='disabled', bg='blue', padx=40, pady=40)
                    buttonList[i].grid(row=1+i//3, column=i%3, padx=1, pady=1)
                    return 1
    return 0

# If there is any space that the computer can select to make a fork, it will be selected
# and the function will return 1. If no fork is possible, 0 will be returned.
def fork(board):
    global buttonList
    for i in range(9):
        if board[i]==0:
            board[i]=-1
            if [sum([board[i] for i in straight]) for straight in straights].count(-2) > 1:
                buttonList[i] = tk.Button(root, state='disabled', bg='blue', padx=40, pady=40)
                buttonList[i].grid(row=1+i//3, column=i%3, padx=1, pady=1)
                return 1
            board[i]=0
    return 0

# If there are any spaces that the player could select to make a fork, then the
# computer will select a space that blocks the fork or forces the Player to select a different space and return 1. If the Player does not have an
# if player1 can fork, blocks the fork and returns 1, returns 0 if player1 can't fork
def blockFork(board):
    global buttonList
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
                            buttonList[i] = tk.Button(root, state='disabled', bg='blue', padx=40, pady=40)
                            buttonList[i].grid(row=1+i//3, column=i%3, padx=1, pady=1)
                            return 1
            board[i]=0
    print('Error in blockFork')
                    
# if the center space is not occupied, select it and return 1. else return 0
def center(board):
    global buttonList
    if board[4]==0:
        board[4]=-1
        buttonList[4] = tk.Button(root, state='disabled', bg='blue', padx=40, pady=40)
        buttonList[4].grid(row=2, column=1, padx=1, pady=1)
        return 1
    return 0

# if player1 has marked a corner space, mark the opposite corner if it is empty
def oppositeCorner(board):
    global buttonList
    for i in [0,2,6,8]:
        if board[i]==1 and board[8-i]==0:
            board[8-i]=-1
            buttonList[8-i] = tk.Button(root, state='disabled', bg='blue', padx=40, pady=40)
            buttonList[8-i].grid(row=1+(8-i)//3, column=(8-i)%3, padx=1, pady=1)
            return 1
    return 0
        
# if there is an available corner, select one
def corner(board):
    global buttonList
    for i in [0,2,6,8]:
        if board[i]==0:
            board[i]=-1
            buttonList[i] = tk.Button(root, state='disabled', bg='blue', padx=40, pady=40)
            buttonList[i].grid(row=1+i//3, column=i%3, padx=1, pady=1)
            return 1
    return 0

# select a side
def side(board):
    global buttonList
    for i in [1,3,5,7]:
        if board[i]==0:
            board[i]=-1
            buttonList[i] = tk.Button(root, state='disabled', bg='blue', padx=40, pady=40)
            buttonList[i].grid(row=1+i//3, column=i%3, padx=1, pady=1)
            return 1
    print('Error: no side was selected')

# determine if either player has won: returns 1 for player1, -1 for player2, and 0 otherwise
def isOver(board):
    for straight in straights:
        if sum([board[i] for i in straight])==3:
            return 1
        if sum([board[i] for i in straight])==-3:
            return -1
    return 0

# performs the computer's move, uses algorithm from tict-tac-toe wikipedia strategy section 
def computerMove(board):
    ticTacToeMoves = [win, block, fork, blockFork, center, oppositeCorner, corner, side]

    # alternates the computer's first move between the middle and the corners
    if board==[0]*9:
        moves=[0,2,4,6,8]
        selection=moves[randint(0,4)]
        board[selection]=-1
        buttonList[selection] = tk.Button(root, state='disabled', bg='blue', padx=40, pady=40)
        buttonList[selection].grid(row=1+selection//3, column=selection%3, padx=1, pady=1)
    
    else:
        performed=0
        index=0
        while not performed:
            performed=ticTacToeMoves[index](board)
            index+=1

### Label   ################################################################################################
winLabel = tk.Label(root)
winLabel.grid(row=4, columnspan=3)

### Buttons ################################################################################################
buttonList = []
for i in range(9):
    newButton=tk.Button(root, command=lambda i=i:clickSpace(i), padx=40, pady=40, borderwidth=3)
    newButton.grid(row=1+i//3, column=i%3, padx=1, pady=1)
    buttonList.append(newButton)

# Button to confirm space selection
buttonNext = tk.Button(root, text='Next', padx=28, pady=10, command=clickNext)
buttonNext.grid(row=5, column=2, sticky='e')

# Button to clear the board
buttonReset = tk.Button(root, text='Reset', padx=24, pady=10, command=clickReset)
buttonReset.grid(row=5, column=0, padx=3,pady=3, sticky='w')

# Buttons to switch between going first or second
playerFirstButton=tk.Button(root)
playerSecondButton=tk.Button(root, text='Go Second', command=clickSecond)
playerSecondButton.grid(row=5, column=1)


root.mainloop()