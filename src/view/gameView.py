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
        self.color_text = (0, 255, 0)

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
        pygame.draw.circle(screen, self.color_mob,
                           (x * self.cell_size + self.cell_size // 2, y * self.cell_size + self.cell_size // 2),
                           self.cell_size // 2)

    def draw_score(self, screen, score):
        text = self.font.render(f"Score: {score}", True, self.color_text)
        text_rect = text.get_rect()
        text_rect.topright = (self.window_width - 10, 10)  # Position at the top right with a 10-pixel margin
        screen.blit(text, text_rect)

    def show_question_popup(self, screen, question, choices, correct_choice):
        popup_width = 400
        popup_height = 300
        popup_x = (self.window_width - popup_width) // 2
        popup_y = (self.window_height - popup_height) // 2

        choice_rects = []
        choice_spacing = 50
        for i, choice in enumerate(choices):
            choice_text = self.font.render(choice, True, (0, 0, 0))
            choice_rect = choice_text.get_rect(center=(popup_x + popup_width // 2, popup_y + 100 + i * choice_spacing))
            choice_rects.append(choice_rect)

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:  # Left mouse button
                        for i, choice_rect in enumerate(choice_rects):
                            if choice_rect.collidepoint(event.pos):
                                if i == correct_choice:
                                    return True
                                else:
                                    return False

            screen.fill(self.color_bg)
            pygame.draw.rect(screen, (255, 255, 255), (popup_x, popup_y, popup_width, popup_height))
            pygame.draw.rect(screen, (0, 0, 0), (popup_x, popup_y, popup_width, popup_height), 2)

            question_text = self.font.render(question, True, (0, 0, 0))
            question_rect = question_text.get_rect(center=(popup_x + popup_width // 2, popup_y + 50))
            screen.blit(question_text, question_rect)

            for i, choice in enumerate(choices):
                choice_text = self.font.render(choice, True, (0, 0, 0))
                choice_rect = choice_text.get_rect(
                    center=(popup_x + popup_width // 2, popup_y + 100 + i * choice_spacing))
                screen.blit(choice_text, choice_rect)

            pygame.display.flip()

    @staticmethod
    def get_user_input():
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "quit"
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return "show_in_game_menu"
                elif event.key == pygame.K_UP:
                    return "up"
                elif event.key == pygame.K_DOWN:
                    return "down"
                elif event.key == pygame.K_LEFT:
                    return "left"
                elif event.key == pygame.K_RIGHT:
                    return "right"
        return None



