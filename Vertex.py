#  Vertex class

class Vertex:
    def __init__(self, row, col):
        self.row = row
        self.col = col
        self.neighs = []  # List of neighbors