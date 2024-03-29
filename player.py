import options


class Player(object):
    """ Player object.  This class is for human players.
    """

    type = None  # possible types are "Human" and "AI"
    name = None
    color = None

    def __init__(self, name, color):
        self.type = "Human"
        self.name = name
        self.color = color

    def setcolor(self, color):
        self.color = color

    def move(self, state):
        print("{0}'s turn.  {0} is {1}".format(self.name, self.color))
        column = None
        while column == None:
            try:
                choice = int(input("Enter a move (by column number): ")) - 1
            except ValueError:
                choice = None
            if 0 <= choice <= options.getCols():
                column = choice
            else:
                print("Invalid choice, try again")
        return column

    def __repr__(self):
        return "Player({},{})".format(self.name, self.color)

    def __str__(self):
        return "Player({},{})".format(self.name, self.color)
