from enum import Enum
import random


class Cells:

    def generator(self, cx, cy, grid):
        if cy < 0 or cy >= grid.shape[0] or cx < 0 or cx >= grid.shape[1]:
            return

        grid[cy, cx] = 0.5

        if (
                0 <= cy - 2 < grid.shape[0] and grid[cy - 2, cx] == 0.5 and
                0 <= cy + 2 < grid.shape[0] and grid[cy + 2, cx] == 0.5 and
                0 <= cx - 2 < grid.shape[1] and grid[cy, cx - 2] == 0.5 and
                0 <= cx + 2 < grid.shape[1] and grid[cy, cx + 2] == 0.5
        ):
            pass
        else:
            li = [1, 2, 3, 4]
            while len(li) > 0:
                direction = random.choice(li)
                li.remove(direction)

                if direction == _Directions.UP.value:
                    ny = cy - 2
                    my = cy - 1
                elif direction == _Directions.DOWN.value:
                    ny = cy + 2
                    my = cy + 1
                else:
                    ny = cy
                    my = cy

                if direction == _Directions.LEFT.value:
                    nx = cx - 2
                    mx = cx - 1
                elif direction == _Directions.RIGHT.value:
                    nx = cx + 2
                    mx = cx + 1
                else:
                    nx = cx
                    mx = cx

                if 0 <= ny < grid.shape[0] and 0 <= nx < grid.shape[1] and grid[ny, nx] != 0.5:
                    grid[my, mx] = 0.5
                    self.generator(nx, ny, grid)


class _Directions(Enum):
    UP = 1
    DOWN = 2
    LEFT = 3
    RIGHT = 4
