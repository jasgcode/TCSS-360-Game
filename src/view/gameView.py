import pygame
from src.model.GameModel import GameModel
from src.model.Player.Player import Position


class GameView:
    def __init__(self, window_width, window_height, cell_size):
        self.model = GameModel()
        self.window_width = window_width
        self.window_height = window_height
        self.cell_size = cell_size
        pygame.font.init()  # Initialize Pygame's font subsystem
        self.font = pygame.font.Font(None, 36)
        self.color_bg = (0, 0, 0)
        self.color_wall = (255, 255, 255)
        self.color_player = (255, 0, 0)
        self.color_text = (0, 0, 0)

    def run(self):
        pygame.init()
        screen = pygame.display.set_mode((self.window_width, self.window_height))
        pygame.display.set_caption("Python Trivia Maze Game")
        clock = pygame.time.Clock()

        self.model.set_difficulty_level("Easy")  # Set the difficulty level before initializing the game
        self.model.initialize_game(self.window_width // self.cell_size, self.window_height // self.cell_size,
                                   self.cell_size)

        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP:
                        self.model.move_player(Position(0, -1))
                    elif event.key == pygame.K_DOWN:
                        self.model.move_player(Position(0, 1))
                    elif event.key == pygame.K_LEFT:
                        self.model.move_player(Position(-1, 0))
                    elif event.key == pygame.K_RIGHT:
                        self.model.move_player(Position(1, 0))

            screen.fill(self.color_bg)
            self.draw_maze(screen)
            self.draw_player(screen)
            self.draw_score(screen)

            pygame.display.flip()
            clock.tick(60)

            self.model.update_game_state()

            if self.model.is_game_over():
                running = False

        pygame.quit()

    def draw_maze(self, screen):
        for y in range(self.model.maze.height):
            for x in range(self.model.maze.width):
                if self.model.maze.maze[y, x] == 1:  # Check if the cell is a wall
                    pygame.draw.rect(screen, self.color_wall,
                                     (x * self.cell_size, y * self.cell_size,
                                      self.cell_size, self.cell_size))

    def draw_player(self, screen):
        x, y = self.model.player.position.x, self.model.player.position.y
        pygame.draw.circle(screen, self.color_player,
                           (x * self.cell_size + self.cell_size // 2, y * self.cell_size + self.cell_size // 2),
                           self.cell_size // 2)

    def draw_score(self, screen):
        text = self.font.render(f"Score: {self.model.score}", True, self.color_text)
        screen.blit(text, (10, 10))


if __name__ == "__main__":
    window_width, window_height = 800, 600
    cell_size = 20  # Adjust the cell size as needed
    view = GameView(window_width, window_height, cell_size)
    view.run()
