from src.model.Entity.Entity import Entity


class Player(Entity):
    def __init__(self, position):
        """
        Initialize the player with a position.
        """
        super().__init__(position)
        self.x = position.x
        self.y = position.y

