import pygame


class GameView:

    def __init__(self, window_width, window_height, cell_size):
        self.window_width = window_width
        self.window_height = window_height
        self.cell_size = cell_size
        pygame.font.init()  # Initialize Pygame's font subsystem
        self.font = pygame.font.Font(None, 36)
        self.color_bg = (255, 255, 255)
        self.color_wall = (0, 0, 0)
        self.color_player = (0, 0, 255)
        self.color_mob = (255, 0, 0)
        self.color_text = (0, 0, 0)

    def draw_maze(self, screen, maze):
        for y in range(maze.height):
            for x in range(maze.width):
                if maze.maze[y, x] == 0:  # Check if the cell is a wall
                    pygame.draw.rect(screen, self.color_wall,
                                     (x * self.cell_size, y * self.cell_size,
                                      self.cell_size, self.cell_size))

    def draw_player(self, screen, player):
        x, y = player.position.x, player.position.y
        pygame.draw.circle(screen, self.color_player,
                           (x * self.cell_size + self.cell_size // 2, y * self.cell_size + self.cell_size // 2),
                           self.cell_size // 2)

    def draw_enemy(self, screen, mob):
        x, y = mob.position.x, mob.position.y
        pygame.draw.circle(screen, self.color_mob,(x * self.cell_size + self.cell_size // 2, y * self.cell_size + self.cell_size // 2),
                           self.cell_size // 2)

    def draw_score(self, screen, score):
        text = self.font.render(f"Score: {score}", True, self.color_text)
        screen.blit(text, (10, 10))

    @staticmethod
    def get_user_input():
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "quit"
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    return "up"
                elif event.key == pygame.K_DOWN:
                    return "down"
                elif event.key == pygame.K_LEFT:
                    return "left"
                elif event.key == pygame.K_RIGHT:
                    return "right"
        return None
