'''
    game1.py
    created by Sam Terwilliger
    This is version of the game dots and boxes. A human player plays against the computer.
    At the beginning, the user is asked to input the number of boxes in a column and a row
    of the gameboard, and then the game begins. When it is over you click to exit.

'''
from board import *
from graphics import *
import time
import random


def find_move(gameboard, win):
    '''This function loops through the elements in the board and checks if it is a line
        that has not been drawn. It then calls complete_square to see if it can complete a square. Otherwise
        it finds the line with the least number of neighbors drawn.
    '''
    min = 4 #set to 4 initially so that even 3 neighbors will trigger the line to be drawn
    i_min = 0
    j_min = 1
    forced_choices = [] #when the minimum is 2 neighbors a list of the potential places is used
    noNeighbors = []
    oneNeighbors = []
    twoNeighbors = []
    for j in range(len(gameboard.board)):
        row = gameboard.board[j]
        for i in range(len(row)):
            #Checks if it is a line
            if (i % 2 == 0 and j % 2 != 0) or (i % 2 != 0 and j % 2 == 0):
                #Checks if it is drawn
                if gameboard.draw_values[j][i] == False:
                    #Checks if drawing it will complete a square
                    if complete_square(gameboard, win, j, i):
                        if double_cross_check(gameboard, win, j, i) and double_cross_play(gameboard, win, j, i):
                            return
                        else:
                            gameboard.draw(win, j, i)
                            return
                    else:
                        localmin = neighbor_count(gameboard, win, j, i)
                        #This checks if the number of neighbor lines of this line is less than the minimum so far
                        if localmin < min:
                            min = localmin
                            i_min = i
                            j_min = j
                        if localmin == 0:
                            noNeighbors.append([j,i])
                        elif localmin == 1:
                            oneNeighbors.append([j,i])
                        else:
                            twoNeighbors.append([j,i])
    #for minimum neighbors of 0 or 1 we pick a random place to draw line
    if min == 0:
        index = random.randint(0,len(noNeighbors)-1)
        j_min = noNeighbors[index][0]
        i_min = noNeighbors[index][1]
    elif min == 1:
        index = random.randint(0,len(oneNeighbors)-1)
        j_min = oneNeighbors[index][0]
        i_min = oneNeighbors[index][1]
    #Finds move where human completes the least squares when human will complete at least 1
    elif min == 2:
        optimal = forced_move(gameboard, win, twoNeighbors)
        j_min = optimal[0]
        i_min = optimal[1]
    gameboard.draw(win, j_min, i_min)
    return

def double_cross_check(gameboard, win, j, i):
    '''Checks to see whether a double_cross move is appropriate. This is when there
        are two boxes remaining in the chain, and the next chain is larger than 2.
    '''
    nextChain = 0
    gameboard.alt_draw(win, j, i)
    numComplete = 1 #set to one since we already drew one line in alt_draw list
    while calc_routes(gameboard, win, False, 0, 0):
        numComplete += 1
    #Loop through board and see what the size of largest remaining chain is
    for j in range(len(gameboard.board)):
        row = gameboard.board[j]
        for i in range(len(row)):
            #Checks if it is a line
            if (i % 2 == 0 and j % 2 != 0) or (i % 2 != 0 and j % 2 == 0):
                #Checks if it is drawn
                if gameboard.draw_values[j][i] == False:
                    #Checks if it will be 3rd side of square
                    if neighbor_count(gameboard, win, j, i) == 2:
                        #checks how long the chain is
                        gameboard.alt_draw(win, j, i)
                        length = 0
                        while calc_routes(gameboard, win, False, 0, 0):
                            length += 1
                        if length > nextChain:
                            nextChain = length
    gameboard.clear_alts(win)
    #We want there to be only two boxes left in the chain and the next chain to be greater than 2
    if nextChain > 2 and numComplete == 2:
        return True
    return False

def double_cross_play(gameboard, win, j_check, i_check):
    '''Finds the location where the double-cross move should be played, which
        sacrifices two squares to the opponent. If it is not possible to double-cross
        then it returns False
    '''
    for j in range(len(gameboard.board)):
        row = gameboard.board[j]
        for i in range(len(row)):
            #Checks if it is a line
            if (i % 2 == 0 and j % 2 != 0) or (i % 2 != 0 and j % 2 == 0):
                #Checks if it is drawn
                if gameboard.draw_values[j][i] == False:
                    #Checks if it will be 3rd side of square
                    if neighbor_count(gameboard, win, j, i) == 2:
                        #checks if this is current chain
                        if calc_routes(gameboard, win, True, j, i):
                            gameboard.draw(win, j, i)
                            gameboard.clear_alts(win)
                            return True
            gameboard.clear_alts(win)
    gameboard.clear_alts(win)
    return False

def forced_move(gameboard, win, forced_choices):
    '''loops through the options and selects the one that will give the human
        the least number of complete squares.
    '''
    best_pair = forced_choices[0]
    minComplete = -1 #set to negative 1 so it will always be beaten initially
    for pair in forced_choices:
        gameboard.alt_draw(win,pair[0],pair[1])
        numComplete = 0
        while calc_routes(gameboard, win, False, 0, 0):
            numComplete += 1
        if numComplete < minComplete or minComplete < 0:
            minComplete = numComplete
            best_pair = pair
        #clears the alt_values since the analysis of the board is complete
        gameboard.clear_alts(win)
    return best_pair

def calc_routes(gameboard, win, cross, cross_j, cross_i):
    '''This function is ran to see how many boxes a player will be able to
        complete next if a choice is taken
        The cross, cross_j, and cross_i parameters are only used when using
        double cross strategy, otherwise they are set to False, 0, 0
    '''
    for j in range(len(gameboard.board)):
        row = gameboard.board[j]
        for i in range(len(row)):
            #Checks if it is a line
            if (i % 2 == 0 and j % 2 != 0) or (i % 2 != 0 and j % 2 == 0):
                #Checks if it is drawn
                if gameboard.draw_values[j][i] == False and gameboard.alt_values[j][i] == False:
                    #Checks if drawing it will complete a square
                    #when double crossing theis means that it was the obvious move
                    if complete_square(gameboard, win, j, i):
                        gameboard.alt_draw(win, j, i)
                        #If double crossing we want to see if the potential double cross spot would
                        #be able to complete a square if the obvious choice was filled in
                        if cross and complete_square(gameboard, win, cross_j, cross_i):
                            return True
                        if not cross:
                            return True
    return False

def complete_square(gameboard, win, j, i):
    '''This function returns whether a move will complete a square by looping through the list of
        a lines neighbors to see how many are drawn.
    '''
    count = 0
    neighbors = gameboard.find_neighbors(win, j, i)
    for neighbor in neighbors:
        for drawvalue in neighbor:
             if drawvalue == True:
                count += 1
        if count == 3:
            return True
        count = 0
    return False



def neighbor_count(gameboard, win, j, i):
    '''Looks at the neighbor lines for a specific line and returns the number of
        neighbor lines that are drawn. If the line has two sets of neighbors (it is not an
        edge line), then it returns the higher number of the two sets.
    '''
    counts = []
    neighbors = gameboard.find_neighbors(win, j, i)
    for neighbor in neighbors:
        count = 0
        for value in neighbor:
            if value == True:
                count += 1
        counts.append(count)
    return max(counts)


def display_result(win, gameboard, winHeight, winWidth):
    '''This function desplays the score at the end of the game. It prints a phrase
        stating who the winner is and then it prints the scores of the human and the
        computer.
    '''
    if gameboard.square_count1 > gameboard.square_count2:
        result = Text(Point(winWidth / 2, 10), "YOU ARE THE WINNER!!!")
        result.setTextColor("purple")
        result.draw(win)
    elif gameboard.square_count1 < gameboard.square_count2:
        result = Text(Point(winWidth / 2, 10),  "THE COMPUTER BEAT YOU!")
        result.setTextColor("purple")
        result.draw(win)
    else:

        result = Text(Point(winWidth / 2, 10), "WOW YOU TIED WITH THE COMPUTER!")
        result.setTextColor("purple")
        result.draw(win)

    your_score = Text(Point(winWidth / 2, 30), "Your Score: " + str(gameboard.square_count1))
    comp_score = Text(Point(winWidth / 2, 50), "The Computer's Score: " + str(gameboard.square_count2))
    your_score.setTextColor("red")
    comp_score.setTextColor("blue")
    your_score.draw(win)
    comp_score.draw(win)

    print("Game has concluded! Click to Exit.")


def main():
    '''This input command asks the user for how many boxes they want in a row
        and multiplies that number by 2(because of the way the array is set up,
        containing boxes, dots, and lines) to get the correct row value. A gameboard with
        rows of length greater than 12 or columns of length greater than 25
        do not fit the display window well. Decimal values will be converted to an integer.
    '''
    rows = int(input("How many boxes in a column do you want (whole number between 2 and 12): ")) * 2
    columns = int(input("How many boxes in a row do you want( whole number between 2 and 25): ")) * 2

    if rows > 24 or columns > 50:
        print("your gameboard is too big for the screen")

    #This scales the width and height of the window depending on the size of the playing grid
    winHeight = 40 * rows + 200
    winWidth = 40 * columns + 200
    win = GraphWin('Dots and Boxes', winWidth, winHeight)
    win.setBackground("white")

    #This displays the players and their color value for when the complete a square
    guide1 = Text(Point(25, 10), "You: Red")
    guide1.setTextColor("red")
    guide1.draw(win)
    guide2 = Text(Point(40, 30), "Computer: Blue")
    guide2.setTextColor("blue")
    guide2.draw(win)

    # make a board and draw it in the window(we give 50 for the number of pixels between dots)
    gameboard = Board(rows, columns, 50, winHeight, winWidth)
    gameboard.build_board(win)

    while win.winfo_exists():
        #when gameboard.move = 0 it is the human's turn
        if gameboard.move == 0:
            gameboard.click(win)
            gameboard.check_square(win, 'red')
        time.sleep(0.2)

        #when gameboard.move = 1 it is the computer's turn
        if gameboard.move == 1:
            find_move(gameboard, win)
            gameboard.check_square(win, 'blue')
        time.sleep(0.2)

        #checks if the game is finished
        gameboard.game_finished()
        if gameboard.game_complete == True:
            display_result(win, gameboard, winHeight, winWidth)
            win.getMouse()
            break


if __name__ == '__main__':
    main()
