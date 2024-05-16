    class Maze:
    def __init__(self, layout):
        self.layout = layout
        self.height = len(layout)
        self.width = len(layout[0])

    def is_wall(self, x, y):
        return self.layout[y][x] == '#'

    def is_valid_move(self, x, y):
        return 0 <= x < self.width and 0 <= y < self.height and not self.is_wall(x, y)

    def get_neighbors(self, x, y):
        neighbors = []
        for dx, dy in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
            nx, ny = x + dx, y + dy
            if self.is_valid_move(nx, ny):
                neighbors.append((nx, ny))
        return neighbors

    def find_path(self, start_x, start_y, end_x, end_y):
        visited = [[False] * self.width for _ in range(self.height)]
        path = []

        def dfs(x, y):
            if x == end_x and y == end_y:
                path.append((x, y))
                return True
            visited[y][x] = True
            for nx, ny in self.get_neighbors(x, y):
                if not visited[ny][nx]:
                    if dfs(nx, ny):
                        path.append((x, y))
                        return True
            return False

        dfs(start_x, start_y)
        path.reverse()
        return path

    def __str__(self):
        return '\n'.join(''.join(row) for row in self.layout)