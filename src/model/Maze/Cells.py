from enum import Enum
import random


class Cells:

    def generator(self, cx, cy, grid):
        grid[cy, cx] = 0.5
        if cx < 0 or cx >= grid.shape[1] or cy < 0 or cy >= grid.shape[0]:
            return

        if (
                cy - 2 >= 0 and grid[cy - 2, cx] == 0.5 and
                cy + 2 < grid.shape[0] and grid[cy + 2, cx] == 0.5 and
                cx - 2 >= 0 and grid[cy, cx - 2] == 0.5 and
                cx + 2 < grid.shape[1] and grid[cy, cx + 2] == 0.5
        ):
            pass
        else:
            li = [1, 2, 3, 4]
            while len(li) > 0:
                dir = random.choice(li)
                li.remove(dir)

                if dir == _Directions.UP.value:
                    ny = cy - 2
                    my = cy - 1
                elif dir == _Directions.DOWN.value:
                    ny = cy + 2
                    my = cy + 1
                else:
                    ny = cy
                    my = cy

                if dir == _Directions.LEFT.value:
                    nx = cx - 2
                    mx = cx - 1
                elif dir == _Directions.RIGHT.value:
                    nx = cx + 2
                    mx = cx + 1
                else:
                    nx = cx
                    mx = cx

                if (
                        0 <= ny < grid.shape[0] and
                        0 <= nx < grid.shape[1] and
                        0 <= my < grid.shape[0] and
                        0 <= mx < grid.shape[1] and
                        grid[ny, nx] != 0.5
                ):
                    grid[my, mx] = 0.5
                    self.generator(nx, ny, grid)


class _Directions(Enum):
    UP = 1
    DOWN = 2
    LEFT = 3
    RIGHT = 4