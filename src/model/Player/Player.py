class Position:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __add__(self, other):
        return Position(self.x + other.x, self.y + other.y)

    def is_valid(self, maze):
        return 0 <= self.x < maze.width and 0 <= self.y < maze.height

    def is_walkable(self, maze):
        return maze.is_walkable(self)

class Player:
    def __init__(self, position):
        self.position = position

    def move(self, direction, maze):
        new_position = Position(self.position.x + direction.x, self.position.y + direction.y)
        if new_position.is_valid(maze) and new_position.is_walkable(maze):
            self.position = new_position