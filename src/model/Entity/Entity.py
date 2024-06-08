class Entity:
    def __init__(self, position):
        """
        Initialize the entity with a position.
        """
        self.position = position

    def move(self, direction, maze):
        """
        Move the entity in the specified direction if the new position is valid and walkable.
        """
        new_position = Position(self.position.x + direction.x, self.position.y + direction.y)
        if new_position.is_valid(maze) and new_position.is_walkable(maze):
            self.position = new_position


class Position:
    def __init__(self, x, y):
        """
        Initialize the position with x and y coordinates.
        """
        self.x = x
        self.y = y

    def __add__(self, other):
        return Position(self.x + other.x, self.y + other.y)

    def is_valid(self, maze):
        """
        Check if the position is within the maze boundaries.
        """
        return 0 < self.x < maze.width - 1 and 0 < self.y < maze.height - 1

    def is_walkable(self, maze):
        """
        Check if the position is walkable (not a wall) in the maze.
        """
        return maze.is_walkable(self)
