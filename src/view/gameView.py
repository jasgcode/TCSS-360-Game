import pygame
from src.model import GameModel


class gameView:
    def __init__(self, width, height):
        self.model = GameModel()
        self.width = width
        self.height = height
        self.cell_size = 40
        self.font = pygame.font.Font(None, 36)
        self.color_bg = (255, 255, 255)
        self.color_wall = (0, 0, 0)
        self.color_player = (255, 0, 0)
        self.color_text = (0, 0, 0)

    def run(self):
        pygame.init()
        screen = pygame.display.set_mode((self.width * self.cell_size, self.height * self.cell_size))
        pygame.display.set_caption("Python Trivia Maze Game")
        clock = pygame.time.Clock()

        self.model.initialize_game()

        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP:
                        self.model.move_player("up")
                    elif event.key == pygame.K_DOWN:
                        self.model.move_player("down")
                    elif event.key == pygame.K_LEFT:
                        self.model.move_player("left")
                    elif event.key == pygame.K_RIGHT:
                        self.model.move_player("right")

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
                if not self.model.maze.is_walkable((x, y)):
                    pygame.draw.rect(screen, self.color_wall,
                                     (x * self.cell_size, y * self.cell_size, self.cell_size, self.cell_size))

    def draw_player(self, screen):
        x, y = self.model.player.position.x, self.model.player.position.y
        pygame.draw.circle(screen, self.color_player,
                           (x * self.cell_size + self.cell_size // 2, y * self.cell_size + self.cell_size // 2),
                           self.cell_size // 2)

    def draw_score(self, screen):
        text = self.font.render(f"Score: {self.model.score}", True, self.color_text)
        screen.blit(text, (10, 10))


if __name__ == "__main__":
    view = gameView(20, 20)
    view.run()