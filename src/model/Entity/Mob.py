from src.model.Entity.Entity import Entity, Position
from queue import PriorityQueue


class Mob(Entity):
    def __init__(self, position):
        super().__init__(position)
        self.path = []
        self.fight = True

    def find_path_to_player(self, maze, player_position):
        distance = [[float('inf')] * maze.width for _ in range(maze.height)]
        distance[self.position.y][self.position.x] = 0

        pq = PriorityQueue()
        pq.put((0, self.position))

        while not pq.empty():
            current_distance, current_position = pq.get()

            if current_position == player_position:
                break

            for direction in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                new_position = Position(current_position.x + direction[0], current_position.y + direction[1])

                if new_position.is_valid(maze) and new_position.is_walkable(maze):
                    new_distance = current_distance + 1

                    if new_distance < distance[new_position.y][new_position.x]:
                        distance[new_position.y][new_position.x] = new_distance
                        pq.put((new_distance, new_position))

        path = []
        current_position = player_position
        while current_position != self.position:
            min_distance = float('inf')
            next_position = None

            for direction in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                new_position = Position(current_position.x + direction[0], current_position.y + direction[1])

                if new_position.is_valid(maze) and new_position.is_walkable(maze):
                    if distance[new_position.y][new_position.x] < min_distance:
                        min_distance = distance[new_position.y][new_position.x]
                        next_position = new_position

            path.append(next_position)
            current_position = next_position

        path.reverse()
        return path

    def move_along_path(self, maze):
        if len(self.path) > 0:
            next_position = self.path.pop(0)
            direction = Position(next_position.x - self.position.x, next_position.y - self.position.y)
            self.move(direction, maze)
