import tkinter as tk
import tkinter.font as tkFont
import glob
from solve import *
from PIL import Image, ImageTk


# Class for the save prompt
class savePrompt:
    def saveToFile(self):
        self.nameMaze = self.entr.get()
        file = open(self.nameMaze + ".txt", 'w')
        file.write(self.mazetext)
        file.close()
        self.win.destroy()

    def __init__(self, win, mazetext):
        self.txt = tk.Label(win, text="Enter name for maze", font=fontStyle)
        self.entr = tk.Entry(win)
        self.button = tk.Button(win, text="Save", font=fontStyle, command=self.saveToFile)
        self.txt.pack()
        self.entr.pack()
        self.button.pack()
        self.mazetext = mazetext
        self.win = win

#v------Button On-Click Functions ----------------------------------------------v

# Gets square being clicked
def getSquareClicked(event):
    row = int(event.y / 22)
    col = int(event.x / 22)
    fillSquare(row, col)


# Allows user to choose a presaved maze from new window, then draws the selected Maze on the canvas
def loadMaze(event=None):
    warning['text'] = ''
    choiceWindow = tk.Toplevel(window)
    choiceWindow.title("Select Maze")
    choiceWindow.geometry("500x300" + "+" + str(int(winWidth/2 - 300/2)) + "+" + str(int(winHeight/2 - 300/2)))
    allMazeFiles = getAllSavedMazes()

    # Initialize list of buttons
    mazeButtons = []

    # Create a button for each txt file found in project folder
    for mazes in allMazeFiles:
        mazeButtons.append(tk.Button(choiceWindow, text=mazes[:len(mazes)-4],
                                     font=fontStyle,
                                     command=lambda selectedMaze=mazes: drawMaze(choiceWindow, selectedMaze)))

    # Pack each button in mazeButton list
    for button in mazeButtons:
        button.pack()


# Will save the maze as a text file
def saveMaze(event=None):
    warning['text'] = ''
    mazeTemplate = "#" * 40 * 18
    allSquares = canv.find_withtag('square')

    # Get coordinates of each blank square
    for blankSquares in allSquares:
        x1, y1, x2, y2 = canv.coords(blankSquares)
        row = int(y1 / 22)
        col = int(x1 / 22)
        mazeTemplate = mazeTemplate[:row * 40 + col] + " " + mazeTemplate[row * 40 + col + 1:]

    mazeTemplate = list(mazeTemplate)
    for i in range(39, len(mazeTemplate), 41):
        mazeTemplate.insert(i + 1, '\n')
    mazeTemplate.append('\n')
    mazeTemplate = ''.join(mazeTemplate)

    saveWindow = tk.Toplevel(window)
    saveWindow.title("Select Maze")
    saveWindow.geometry("300x100" + "+" + str(int(winWidth / 2 - 300 / 2)) + "+" + str(int(winHeight / 2 - 300 / 2)))
    savePrompt(saveWindow, mazeTemplate)


# loadMaze will call this function for each square
def fillSquare(row, col):
    warning['text'] = ''
    x0 = (col+1)*2 + col*20
    y0 = (row+1)*2 + row*20
    canv.create_rectangle(x0, y0, x0+19, y0+19, tag='square', fill="white", outline="white")


# fills square to show correct solution path
def fillSquare_green(row, col):
    x0 = (col+1)*2 + col*20
    y0 = (row+1)*2 + row*20
    canv.create_rectangle(x0, y0, x0+19, y0+19, tag='greensquare', fill="green", outline="green")


# Draws lines on canvas and calls fillSquare to reset square color to black
def drawBlankMaze(event=None):
    warning['text'] = ''
    # Get current width of canvas
    w = canv.winfo_width()

    # Get current height of canvas
    h = canv.winfo_height()
    canv.delete("square")
    canv.delete('grid_line')
    canv.delete('greensquare')

    # Creates vertical lines at intervals of 22
    for i in range(1, w, 22):
        canv.create_line([(i, 0), (i, h)], tag='grid_line', fill="white", width=2)

    # Creates horizontal lines at intervals of 22
    for i in range(1, h, 22):
        canv.create_line([(0, i), (w, i)], tag='grid_line', fill="white", width=2)


# Function to return all Maze txt files in project folder
def getAllSavedMazes():
    mazeFiles = glob.glob('*.txt')
    return mazeFiles


# Draws selected maze onto canvas
def drawMaze(selectWindow, selection):
    # Close selection window after choosing Maze
    selectWindow.destroy()
    drawBlankMaze()

    file = open(selection, "r")
    mazeText = file.read().splitlines()
    mazeText = ''.join(mazeText)

    # Read blank spaces in maze file
    for i in range(18):
        for j in range(40):
            if mazeText[i * 40 + j] == " ":
                fillSquare(i, j)


# Reads maze from canvas
def readMaze():
    mazeTemplate = "#" * 40 * 18
    allSquares = canv.find_withtag('square')

    # Get coordinates of each blank square
    for blankSquares in allSquares:
        x1, y1, x2, y2 = canv.coords(blankSquares)
        row = int(y1 / 22)
        col = int(x1 / 22)
        mazeTemplate = mazeTemplate[:row * 40 + col] + " " + mazeTemplate[row * 40 + col + 1:]

    mazeTemplate = list(mazeTemplate)
    for i in range(39, len(mazeTemplate), 41):
        mazeTemplate.insert(i + 1, '\n')
    mazeTemplate.append('\n')
    mazeTemplate = ''.join(mazeTemplate)
    return mazeTemplate


# updates maze to show solution
def updateMaze(solution):
    # Read blank spaces in maze file
    for i in range(18):
        for j in range(40):
            if solution[i * 40 + j + i] == "o":
                fillSquare_green(i, j)
                canv.after(1000, lambda: print(".", end=""))


# Solves the maze
def solveMaze(event):
    warning['text'] = ''
    canv.delete("greensquare")

    maze = readMaze()
    try:
        solution = solve(maze)
    except AttributeError:
        solution = "Error:  Maze is empty."
    if solution == "Error:  Maze is empty." or solution == "Error:  There must be two openings." or solution == "Error:  No path found.":
        warning['text'] = solution
    else:
        updateMaze(solution)
        warning['text'] = 'Maze solved!'
        warning['fg'] = 'green'


#^------------------------------------------------------------------------------^


#v------Configuring Window Size and Size of Frames------------------------------v
window = tk.Tk()
window.title("Maze Solver")
winWidth = window.winfo_screenwidth()
winHeight = window.winfo_screenheight()

sizeWidth = 1200
sizeHeight = 600
window.geometry(str(sizeWidth) + "x" + str(sizeHeight) + "+" + str(int(winWidth/2 - sizeWidth/2)) +
                "+" + str(int(winHeight/2 - sizeHeight/2)))

fontStyle = tkFont.Font(family="FreeSans", size=20, weight="bold")
#^-------------------------------------------------------------------------------^

# If you want to print value to row/column to pycharm console and other info
debug = False

#v------Left Frame/Buttons-------------------------------------------------------v
lFrameWidth = 0.25*sizeWidth
lFrame = tk.LabelFrame(window, width=lFrameWidth, height=700, padx=10, pady=10, bg="gray")
lFrame.pack(side="left", expand=True, fill="both")

# Height and Width of the buttons
# If you want to change size of buttons, adjust these
bWidth = int(sizeWidth*0.25*2/3)
bHeight = int(sizeHeight/10)

# Changed from 60
buttonPadY = 30

b1Image = ImageTk.PhotoImage(Image.open("drawgridbutton.jpg").resize((bWidth, bHeight), Image.ANTIALIAS))
b2Image = ImageTk.PhotoImage(Image.open("loadmazebutton.jpg").resize((bWidth, bHeight), Image.ANTIALIAS))
b3Image = ImageTk.PhotoImage(Image.open("solvemazebutton.jpg").resize((bWidth, bHeight), Image.ANTIALIAS))
b4Image = ImageTk.PhotoImage(Image.open('savebutton.jpg').resize((bWidth, bHeight), Image.ANTIALIAS))

b1 = tk.Button(lFrame, image=b1Image, padx=10, pady=10, bg="gray", highlightthickness=0, borderwidth=0)
b1.pack(pady=buttonPadY)
b1.bind("<Button 1>", drawBlankMaze)

b2 = tk.Button(lFrame, image=b2Image, padx=10, pady=10, bg="gray", highlightthickness=0, borderwidth=0)
b2.pack(pady=buttonPadY)
b2.bind("<Button 1>", loadMaze)

b4 = tk.Button(lFrame, image=b4Image, padx=10, pady=10, bg="gray", highlightthickness=0, borderwidth=0)
b4.pack(pady=buttonPadY)
b4.bind("<Button 1>", saveMaze)

b3 = tk.Button(lFrame, image=b3Image, padx=10, pady=10, bg="gray", highlightthickness=0, borderwidth=0)
b3.pack(pady=buttonPadY)
b3.bind("<Button 1>", solveMaze)
#^-----------------------------------------------------------------------------------^

#v------Right Frame/Canvas-----------------------------------------------------------v
rFrameWidth = 0.75*sizeWidth
rFrame = tk.LabelFrame(window, width=rFrameWidth, height=700, padx=10, pady=10, bg="gray")
rFrame.pack(side="right", expand=True, fill="both")

welcome = tk.Label(text = 'Welcome to the Maze Solver!', font=fontStyle, fg='white', bg='gray')
welcome.place(x=280, y=40, anchor='w')

welcome2 = tk.Label(text = 'Draw or load a maze to begin.', font=('Lucida Console', 10), fg='white', bg='gray')
welcome2.place(relx=0.75, y=40, anchor='w')

canv = tk.Canvas(rFrame, height=398, width=882, bg="black", highlightthickness=0, borderwidth=0)
canvPadX = int((rFrameWidth - 882)/2)
canvPadY = int((sizeHeight-398 - 30)/2)
canv.pack(padx=canvPadX, pady=canvPadY)
canv.bind("<Configure>", drawBlankMaze)
canv.bind('<Button-1>', getSquareClicked)

warning = tk.Label(font=('Lucida Console', 10), fg='red', bg='gray')
warning.place(relx=0.75, y=70, anchor='w')
#^-----------------------------------------------------------------------------------^
tk.mainloop()