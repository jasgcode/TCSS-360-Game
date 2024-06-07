import pygame

class MenuView:
    def __init__(self, screen, model):
        self.screen = screen
        self.model = model
        # Load the 8-bit font
        self.font_title = pygame.font.Font("PressStart2P-Regular.ttf", 48)
        self.font_options = pygame.font.Font("PressStart2P-Regular.ttf", 36)
        self.font_about = pygame.font.Font("PressStart2P-Regular.ttf", 18)
        self.background_image = pygame.image.load("../images/MainMenu.JPG").convert()  # Load the background image
        self.background_image = pygame.transform.scale(self.background_image,
                                                       (self.screen.get_width(), self.screen.get_height()))

    def draw_menu(self, show_difficulty_options=False, show_save_files=False, scroll_offset=0):
        self.screen.blit(self.background_image, (0, 0))

        # Draw the title
        title_text = self.font_title.render("Escape The Seven Seas", True, (255, 255, 255))
        title_rect = title_text.get_rect(center=(self.screen.get_width() // 2, 100))
        self.screen.blit(title_text, title_rect)

        if not show_difficulty_options and not show_save_files:
            # Draw the "New Game", "Load Game", and "About" options
            new_game_text = self.font_options.render("New Game", True, (255, 255, 255))
            new_game_rect = new_game_text.get_rect(center=(self.screen.get_width() // 2, 200))
            self.screen.blit(new_game_text, new_game_rect)

            load_game_text = self.font_options.render("Load Game", True, (255, 255, 255))
            load_game_rect = load_game_text.get_rect(center=(self.screen.get_width() // 2, 250))
            self.screen.blit(load_game_text, load_game_rect)

            about_text = self.font_options.render("About", True, (255, 255, 255))
            about_rect = about_text.get_rect(center=(self.screen.get_width() // 2, 300))
            self.screen.blit(about_text, about_rect)
        else:
            # Draw the "Back" button
            back_text = self.font_options.render("Back", True, (255, 255, 255))
            back_rect = back_text.get_rect(topleft=(50, 50))
            self.screen.blit(back_text, back_rect)

        if show_difficulty_options:
            # Draw the difficulty options
            difficulty_options = ["Easy", "Medium", "Hard"]
            for i, option in enumerate(difficulty_options):
                text = self.font_options.render(option, True, (255, 255, 255))
                text_rect = text.get_rect(center=(self.screen.get_width() // 2, 350 + i * 50))
                self.screen.blit(text, text_rect)

        if show_save_files:
            # Draw the available save files as clickable rectangles
            for i, save_file in enumerate(self.model.save_files[scroll_offset:scroll_offset + 5]):
                text = self.font_options.render(save_file, True, (0, 0, 0))
                text_rect = text.get_rect(center=(self.screen.get_width() // 2, 350 + i * 50))
                pygame.draw.rect(self.screen, (200, 200, 200), text_rect, 2)
                self.screen.blit(text, text_rect)

            # Draw scroll arrows if there are more save files
            if len(self.model.save_files) > 5:
                up_arrow_rect = pygame.Rect(self.screen.get_width() // 2 - 50, 300, 100, 30)
                down_arrow_rect = pygame.Rect(self.screen.get_width() // 2 - 50, 550, 100, 30)
                pygame.draw.rect(self.screen, (200, 200, 200), up_arrow_rect)
                pygame.draw.rect(self.screen, (200, 200, 200), down_arrow_rect)
                up_arrow_text = self.font_options.render("Up", True, (0, 0, 0))
                down_arrow_text = self.font_options.render("Down", True, (0, 0, 0))
                self.screen.blit(up_arrow_text, up_arrow_rect)
                self.screen.blit(down_arrow_text, down_arrow_rect)

        pygame.display.flip()

    def get_selected_option(self, pos, show_difficulty_options=False, show_save_files=False, scroll_offset=0):
        if not show_difficulty_options and not show_save_files:
            # Check if "New Game" is clicked
            new_game_text = self.font_options.render("New Game", True, (0, 0, 0))
            new_game_rect = new_game_text.get_rect(center=(self.screen.get_width() // 2, 200))
            if new_game_rect.collidepoint(pos):
                return 'new_game'

            # Check if "Load Game" is clicked
            load_game_text = self.font_options.render("Load Game", True, (0, 0, 0))
            load_game_rect = load_game_text.get_rect(center=(self.screen.get_width() // 2, 250))
            if load_game_rect.collidepoint(pos):
                return 'load_game'

            # Check if "About" is clicked
            about_text = self.font_options.render("About", True, (0, 0, 0))
            about_rect = about_text.get_rect(center=(self.screen.get_width() // 2, 300))
            if about_rect.collidepoint(pos):
                return 'About'

        else:
            # Check if "Back" is clicked
            back_text = self.font_options.render("Back", True, (0, 0, 0))
            back_rect = back_text.get_rect(topleft=(50, 50))
            if back_rect.collidepoint(pos):
                return 'back'

        if show_difficulty_options:
            # Check if a difficulty option is clicked
            difficulty_options = ["Easy", "Medium", "Hard"]
            for i, option in enumerate(difficulty_options):
                text = self.font_options.render(option, True, (0, 0, 0))
                text_rect = text.get_rect(center=(self.screen.get_width() // 2, 350 + i * 50))
                if text_rect.collidepoint(pos):
                    return option
        if show_save_files:
            # Check if a save file rectangle is clicked
            for i, save_file in enumerate(self.model.save_files[scroll_offset:scroll_offset + 5]):
                text = self.font_options.render(save_file, True, (0, 0, 0))
                text_rect = text.get_rect(center=(self.screen.get_width() // 2, 350 + i * 50))
                if text_rect.collidepoint(pos):
                    return save_file

            # Check if scroll arrows are clicked
            if len(self.model.save_files) > 5:
                up_arrow_rect = pygame.Rect(self.screen.get_width() // 2 - 50, 300, 100, 30)
                down_arrow_rect = pygame.Rect(self.screen.get_width() // 2 - 50, 550, 100, 30)
                if up_arrow_rect.collidepoint(pos):
                    return 'scroll_up'
                elif down_arrow_rect.collidepoint(pos):
                    return 'scroll_down'

        return None

    def show_about_popup(self):
        popup_width = 1280
        popup_height = 720
        popup_rect = pygame.Rect((self.screen.get_width() - popup_width) // 2,
                                 (self.screen.get_height() - popup_height) // 2, popup_width, popup_height)

        while True:
            self.screen.fill((0, 0, 0))

            # Draw the popup background
            pygame.draw.rect(self.screen, (255, 255, 255), popup_rect)

            # Draw the popup title
            title_font = pygame.font.Font("PressStart2P-Regular.ttf", 24)
            title_text = title_font.render("About Escape The Seven Seas", True, (0, 0, 0))
            title_rect = title_text.get_rect(midtop=(popup_rect.centerx, popup_rect.top + 20))
            self.screen.blit(title_text, title_rect)

            # Draw the game information
            info = [
                "Escape The Seven Seas is a thrilling maze game",
                "where you navigate through treacherous mazes",
                "filled with mobs and challenges. Your goal is",
                "to reach the end of each maze while answering",
                "trivia questions correctly to progress. Can",
                "you escape all the mazes and emerge victorious?"
            ]
            info_font = pygame.font.Font("PressStart2P-Regular.ttf", 16)
            for i, line in enumerate(info):
                text = info_font.render(line, True, (0, 0, 0))
                text_rect = text.get_rect(topleft=(popup_rect.left + 20, popup_rect.top + 80 + i * 30))
                self.screen.blit(text, text_rect)

            # Draw the close button
            close_font = pygame.font.Font("PressStart2P-Regular.ttf", 18)
            close_text = close_font.render("Close", True, (0, 0, 0))
            close_rect = close_text.get_rect(midbottom=(popup_rect.centerx, popup_rect.bottom - 20))
            pygame.draw.rect(self.screen, (200, 200, 200), close_rect, 2)
            self.screen.blit(close_text, close_rect)

            pygame.display.flip()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    return
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if close_rect.collidepoint(event.pos):
                        return