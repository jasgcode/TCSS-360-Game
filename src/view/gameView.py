import pygame


class GameView:
    def __init__(self, window_width, window_height, cell_size):
        """
        Initialize the GameView with window dimensions and cell size.
        """
        self.window_width = window_width
        self.window_height = window_height
        self.cell_size = cell_size
        pygame.font.init()  # Initialize Pygame's font subsystem
        self.font = pygame.font.Font(None, 30)
        self.color_bg = (255, 255, 255)
        self.color_text = (0, 0, 0)
        self.screen = pygame.display.set_mode((self.window_width, self.window_height))

        # Load images
        self.barrel_image = self.load_and_scale_image("../images/barrel.webp")
        self.player_image = self.load_and_scale_image("../images/alcoholic.webp")
        self.mob_image = self.load_and_scale_image("../images/police_officer.webp")
        self.blue_portal_image = self.load_and_scale_image("../images/blue_portal.png")
        self.orange_portal_image = self.load_and_scale_image("../images/orange_portal.png")

    def load_and_scale_image(self, path):
        """
        Load and scale an image from the specified path.
        """
        try:
            image = pygame.image.load(path).convert_alpha()  # Load the image with transparency
            image = pygame.transform.scale(image, (self.cell_size, self.cell_size))  # Scale it to cell size
            print(f"Image loaded successfully from {path}")
            return image
        except pygame.error as e:
            print(f"Failed to load image from {path}: {e}")
            return None

    def draw(self, game_model):
        """
        Draw the game view based on the current game model state.
        """
        print("Drawing game view...")  # Debug statement to verify method call
        self.screen.fill(self.color_bg)  # Fill screen with gray before drawing
        for y in range(game_model.maze.height):
            for x in range(game_model.maze.width):
                cell = game_model.maze.get_cell(x, y)
                if cell.is_wall:
                    pygame.draw.rect(self.screen, self.color_bg,
                                     (x * self.cell_size, y * self.cell_size, self.cell_size, self.cell_size))
                elif cell.value == 0.75:
                    self.screen.blit(self.blue_portal_image,
                                     (x * self.cell_size, y * self.cell_size))  # Draw blue portal
                    print(f"Drawing blue portal at: ({x}, {y})")  # Debug statement
                elif cell.value == 0.6:
                    self.screen.blit(self.orange_portal_image,
                                     (x * self.cell_size, y * self.cell_size))  # Draw orange portal
                    print(f"Drawing orange portal at: ({x}, {y})")  # Debug statement
                else:
                    pygame.draw.rect(self.screen, self.color_bg,
                                     (x * self.cell_size, y * self.cell_size, self.cell_size, self.cell_size))
        pygame.display.flip()

    def draw_maze(self, screen, maze, maze_number):
        """
        Draw the maze on the screen.
        """
        screen.fill(self.color_bg)  # Fill the screen with the background color
        for y in range(maze.height):
            for x in range(maze.width):
                if maze.maze[y, x] == 0:  # Check if the cell is a wall
                    screen.blit(self.barrel_image, (x * self.cell_size, y * self.cell_size))
                elif maze.maze[y, x] == 0.75:
                    screen.blit(self.blue_portal_image, (x * self.cell_size, y * self.cell_size))
                elif maze.maze[y, x] == 0.6:
                    screen.blit(self.orange_portal_image, (x * self.cell_size, y * self.cell_size))

        self.draw_maze_number(screen, maze_number)  # Draw the maze number

    def draw_maze_number(self, screen, maze_number):
        """
        Draw the maze number on the screen.
        """
        text = self.font.render(f"Level: {maze_number}", True, self.color_text)
        text_rect = text.get_rect()
        text_rect.topleft = (10, 10)  # Position at the top left with a 10-pixel margin
        screen.blit(text, text_rect)

    def draw_player(self, screen, player):
        """
        Draw the player on the screen.
        """
        x, y = player.position.x, player.position.y
        if self.player_image:
            screen.blit(self.player_image, (x * self.cell_size, y * self.cell_size))
        else:
            pygame.draw.circle(screen, (0, 0, 255),
                               (x * self.cell_size + self.cell_size // 2, y * self.cell_size + self.cell_size // 2),
                               self.cell_size // 2)

    def draw_enemy(self, screen, mob):
        """
        Draw the enemy (mob) on the screen.
        """
        x, y = mob.position.x, mob.position.y
        if self.mob_image:
            screen.blit(self.mob_image, (x * self.cell_size, y * self.cell_size))
        else:
            pygame.draw.circle(screen, (255, 0, 0),
                               (x * self.cell_size + self.cell_size // 2, y * self.cell_size + self.cell_size // 2),
                               self.cell_size // 2)

    def draw_score(self, screen, score):
        """
        Draw the player's score on the screen.
        """
        text = self.font.render(f"Score: {score}", True, self.color_text)
        text_rect = text.get_rect()
        text_rect.topright = (self.window_width - 10, 10)  # Position at the top right with a 10-pixel margin
        screen.blit(text, text_rect)

    def draw_lives(self, screen, lives):
        """
        Draw the player's remaining lives on the screen.
        """
        text = self.font.render(f"Lives: {lives}", True, self.color_text)
        text_rect = text.get_rect()
        text_rect.bottomright = (self.window_width - 10, self.window_height-10)  # Position at the top right with a 10-pixel margin
        screen.blit(text, text_rect)

    def show_question_popup(self, screen, question, choices, correct_choice):
        """
        Show a popup with a trivia question and handle user input for answering the question.
        """
        popup_width = 900
        popup_height = 600
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
        """
        Get the user's input from the keyboard and handle specific key events.
        """
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
                elif event.key == pygame.K_w:
                    return "up"
                elif event.key == pygame.K_s:
                    return "down"
                elif event.key == pygame.K_d:
                    return "right"
                elif event.key == pygame.K_a:
                    return "left"
                elif event.key == pygame.K_x:
                    return "x"
                elif event.key == pygame.K_c:
                    print("'c' key pressed")  # Debug statement
                    return "c"
        return None
