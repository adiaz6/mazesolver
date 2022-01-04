from Vertex import Vertex
import queue


#  Create vertices from maze
def addVerts(maze, vertMaze):
    row = 0  # Initialize row and column values
    col = 0

    for i in range(len(maze)):
        if maze[i] == ' ':
            v = Vertex(row, col)
            vertMaze.append(v)  # Forms vertices from empty spaces in maze
        else:
            vertMaze.append(None)  # "Walls" are denoted by None type

        col += 1

        if maze[i] == '\n':  # Updates row and column when end of line is reached
            row += 1
            col = 0


# Adds neighbors of each vertex
# Neighbors are adjacent vertices (rows or columns are within 1 index of each other)
def addEdges(vertMaze):
    for i in range(len(vertMaze)):
        if vertMaze[i] is not None:
            for j in range(len(vertMaze)):
                if (vertMaze[j] is not None) and (vertMaze[j] != vertMaze[i]):
                    if vertMaze[i].col == vertMaze[j].col and vertMaze[i].row + 1 == vertMaze[j].row:
                        vertMaze[i].neighs.append(vertMaze[j])
                    if vertMaze[i].col == vertMaze[j].col and vertMaze[i].row - 1 == vertMaze[j].row:
                        vertMaze[i].neighs.append(vertMaze[j])
                    if vertMaze[i].row == vertMaze[j].row and vertMaze[i].col + 1 == vertMaze[j].col:
                        vertMaze[i].neighs.append(vertMaze[j])
                    if vertMaze[i].row == vertMaze[j].row and vertMaze[i].col - 1 == vertMaze[j].col:
                        vertMaze[i].neighs.append(vertMaze[j])

# Find openings
def findOpenings(maze):
    rowsize = 1
    s = 0
    t = 0
    num = 0

    i = 0
    while maze[i] != '\n':
        rowsize += 1
        i += 1

    numrows = len(maze) / rowsize

    i = 0
    while maze[i] != '\n':
        if maze[i] == ' ':
            if s != 0:
                t = i
            else:
                s = i
            num += 1
        i += 1

    i = len(maze) - rowsize
    while maze[i] != '\n':
        if maze[i] == ' ':
            if s != 0:
                t = i
            else:
                s = i
            num += 1

        i += 1

    i = rowsize
    while i <= len(maze) - 2 * rowsize:
        if maze[i] == ' ':
            if s != 0:
                t = i
            else:
                s = i
            num += 1

        i += rowsize

    i = (rowsize - 1) * 2
    while i <= len(maze) - rowsize - 2:
        if maze[i] == ' ':
            if s != 0:
                t = i
            else:
                s = i
            num += 1

        i += rowsize

    return s, t, num # Return number of openings to check eligibility of maze

# Runs breadthfirstsearch on maze
def breadthfirstsearch(s, vertMaze):
    Q = queue.Queue()
    marked = []
    breadcrumbs = {}

    S = vertMaze[s]

    marked.append(S)
    Q.put(S)

    while Q.qsize() != 0:
        x = Q.get()

        for i in range(len(x.neighs)):
            y = x.neighs[i]

            if y not in marked:
                marked.append(y)
                Q.put(y)

                breadcrumbs[y] = x

    return breadcrumbs

# Marks the path
def markPath(maze, breadcrumbs, start, end):
    output = list(maze)
    current = end
    rowsize = 1
    index = 0

    i = 0
    while maze[i] != '\n':
        rowsize += 1
        i += 1

    while current != start:
        index = current.row * rowsize + current.col
        output[index] = 'o'
        try:
            current = breadcrumbs[current]
        except KeyError:
            return "Error:  No path found."


    output[start.row * rowsize + start.col] = 'o'

    output = ''.join(output)
    return output

# Checks if a path exists
def pathexists(maze, breadcrumbs, start, end):
    return True

# Solves the maze
def solve(maze):
    vertMaze = []
    addVerts(maze, vertMaze)

    addEdges(vertMaze)

    s, t, num = findOpenings(maze)

    breadcrumbs = breadthfirstsearch(s, vertMaze)

    two_spaces = True
    if num != 2:
        two_spaces = False

    if not two_spaces:
        return "Error:  There must be two openings."
    elif two_spaces:
        output = markPath(maze, breadcrumbs, vertMaze[s], vertMaze[t])
        return output