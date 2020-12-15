from graphics import *


class Board(GraphWin):

    def __init__(self, rows, columns, linelength, winHeight, winWidth):
        self.rows = rows
        self.columns = columns
        self.linelength = linelength
        self.winHeight = winHeight
        self.winWidth = winWidth
        self.board = []
        self.draw_values = []
        self.alt_values = []

        self.radius = 4
        self.pcolor = "black"

        self.square_count1 = 0
        self.square_count2 = 0
        self.game_complete = False

        self.xclick = 250
        self.yclick = 250

        self.move = 0
        self.square_found = False
        self.click_completed = False

    def draw(self, window, row_value, column_value):
        if self.draw_values[row_value][column_value] == False:
            self.board[row_value][column_value].draw(window)
            self.draw_values[row_value][column_value] = True

    def alt_draw(self, window, row_value, column_value):
        if self.draw_values[row_value][column_value] == False and self.alt_values[row_value][column_value] == False:
            self.alt_values[row_value][column_value] = True

    def clear_alts(self, window):
        for j in range(self.rows + 1):
            for i in range(self.columns + 1):
                if self.alt_values[j][i]:
                    self.alt_values[j][i] = False


    def build_board(self, window):

        for row in range(self.rows + 1):
            self.board.append([])
            self.draw_values.append([])
            self.alt_values.append([])

        self.win = window

        for y in range(self.rows + 1):
            py = (self.winHeight / 4.5) + (self.linelength / 2) * y
            for x in range(self.columns + 1):
                px = (self.winWidth / 4.5) + (self.linelength / 2) * x

                if x % 2 == 0 and y % 2 == 0:
                    dot = Circle(Point(px, py), self.radius)
                    dot.draw(window)
                    dot.setFill(self.pcolor)
                    self.board[y].append(dot)
                    self.draw_values[y].append(True)
                    self.alt_values[y].append(True)

                elif  x % 2 != 0 and  y % 2 == 0:
                    self.hline = Line(Point(px - self.linelength/2, py), Point(px + self.linelength/2, py))
                    self.hline.setWidth(3)
                    self.board[y].append(self.hline)
                    self.draw_values[y].append(False)
                    self.alt_values[y].append(False)

                elif  x % 2 == 0 and  y % 2 != 0:
                    self.vline = Line(Point(px, py - self.linelength/2), Point(px, py + self.linelength/2))
                    self.vline.setWidth(3)
                    self.board[y].append(self.vline)
                    self.draw_values[y].append(False)
                    self.alt_values[y].append(False)


                else:
                    self.square = Polygon(Point(px - round(self.linelength/2 - 2), py - round(self.linelength/2 -2)),
                                            Point(px + round(self.linelength/2 -2), py - round(self.linelength/2 -2)),
                                            Point(px + round(self.linelength/2 -2), py + round(self.linelength/2 -2)),
                                            Point(px - round(self.linelength/2 -2), py + round(self.linelength/2 -2)))
                    self.board[y].append(self.square)
                    self.draw_values[y].append(False)
                    self.alt_values[y].append(False)

    def click(self,window):
        while True:
            clickPoint = window.getMouse()
            self.xclick = clickPoint.getX()
            self.yclick = clickPoint.getY()
            for j in range(len(self.board)):
                row = self.board[j]
                for i in range(len(row)):
                    if i % 2 != 0 and j % 2 == 0:
                        if (self.board[j][i].getCenter().getX() - self.linelength / 3
                        <= self.xclick <= self.board[j][i].getCenter().getX() + self.linelength / 3
                        and self.board[j][i].getCenter().getY() - self.linelength / 5
                        <= self.yclick <= self.board[j][i].getCenter().getY() + self.linelength / 5
                        and not self.draw_values[j][i]):
                            self.draw(window, j, i)
                            return
                    elif i % 2 == 0 and j % 2 != 0:
                        if (self.board[j][i].getCenter().getX() - self.linelength / 5
                        <= self.xclick <= self.board[j][i].getCenter().getX() + self.linelength / 5
                        and self.board[j][i].getCenter().getY() - self.linelength / 3
                        <= self.yclick <= self.board[j][i].getCenter().getY() + self.linelength / 3
                        and not self.draw_values[j][i]):
                            self.draw(window, j, i)
                            return

    def check_square(self, window, color):
        for j in range(len(self.board)):
            row = self.board[j]
            for i in range(len(row)):
                if (i % 2) != 0 and (j % 2) != 0:
                    if self.draw_values[j][i] == False:
                        if ((self.draw_values[j - 1][i] == True) and (self.draw_values[j][i-1] == True)
                            and (self.draw_values[j +1][i] == True) and (self.draw_values[j][i+1] == True)):
                            self.board[j][i].setFill(color)
                            self.board[j][i].setOutline(color)
                            self.draw(window, j, i)
                            self.square_found = True
                            if self.move == 0:
                                self.square_count1 += 1
                            else:
                                self.square_count2 += 1

        if self.square_found == False:
            if self.move == 0:
                self.move = 1
            else:
                self.move = 0
        else:
            self.square_found = False



    def find_neighbors(self, window, j, i):
        neighbors = []
        if j == 0:
            neighbors.append([self.draw_values[j+2][i], self.draw_values[j+1][i-1], self.draw_values[j+1][i+1],
            self.alt_values[j+2][i], self.alt_values[j+1][i-1], self.alt_values[j+1][i+1]])
        elif j == self.rows:
            neighbors.append([self.draw_values[j-2][i], self.draw_values[j-1][i-1], self.draw_values[j-1][i+1],
            self.alt_values[j-2][i], self.alt_values[j-1][i-1], self.alt_values[j-1][i+1]])
        elif j % 2 == 0:
            neighbors.append([self.draw_values[j-2][i], self.draw_values[j-1][i-1], self.draw_values[j-1][i+1],
            self.alt_values[j-2][i], self.alt_values[j-1][i-1], self.alt_values[j-1][i+1]])
            neighbors.append([self.draw_values[j+2][i], self.draw_values[j+1][i-1], self.draw_values[j+1][i+1],
            self.alt_values[j+2][i], self.alt_values[j+1][i-1], self.alt_values[j+1][i+1]])
        elif i == 0:
            neighbors.append([self.draw_values[j][i+2], self.draw_values[j+1][i+1], self.draw_values[j-1][i+1],
            self.alt_values[j][i+2], self.alt_values[j+1][i+1], self.alt_values[j-1][i+1]])
        elif i == self.columns:
            neighbors.append([self.draw_values[j][i-2], self.draw_values[j+1][i-1], self.draw_values[j-1][i-1],
            self.alt_values[j][i-2], self.alt_values[j+1][i-1], self.alt_values[j-1][i-1]])
        elif i % 2 == 0:
            neighbors.append([self.draw_values[j][i-2], self.draw_values[j-1][i-1], self.draw_values[j+1][i-1],
            self.alt_values[j][i-2], self.alt_values[j-1][i-1], self.alt_values[j+1][i-1]])
            neighbors.append([self.draw_values[j][i+2], self.draw_values[j-1][i+1], self.draw_values[j+1][i+1],
            self.alt_values[j][i+2], self.alt_values[j-1][i+1], self.alt_values[j+1][i+1]])
        return neighbors


    def game_finished(self):
        self.game_complete = True
        for j in range(len(self.board)):
            row = self.board[j]
            for i in range(len(row)):
                if (i % 2) != 0 and (j % 2) != 0:
                    if self.draw_values[j][i] == False:
                        self.game_complete = False




def testModule(): 

    winHeight = 500
    winWidth = 500
    win = GraphWin('Board Module Test', winWidth, winHeight)
    win.setBackground("white")

    board = Board(6, 6, 50, winHeight, winWidth)
    board.build_board(win)


    print('Board test.')
    while win.winfo_exists():
        board.click(win)
        board.check_square(win, 'red')
        win.update()

if __name__ == '__main__':
   testModule()
