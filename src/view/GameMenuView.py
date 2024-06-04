import pygame


class InGameMenuView:
    def __init__(self, screen, game_view):
        self.screen = screen
        self.game_view = game_view
        self.font = pygame.font.Font(None, 36)

    def draw_menu(self, menu_options):
        self.screen.fill((255, 255, 255))
        for i, option in enumerate(menu_options):
            text = self.font.render(option, True, (0, 0, 0))
            text_rect = text.get_rect(center=(self.screen.get_width() // 2, 200 + i * 50))
            self.screen.blit(text, text_rect)
        pygame.display.flip()

    def draw_load_popup(self, save_files):
        popup_width = 400
        popup_height = 300
        popup_x = (self.screen.get_width() - popup_width) // 2
        popup_y = (self.screen.get_height() - popup_height) // 2

        self.screen.fill((255, 255, 255))
        pygame.draw.rect(self.screen, (0, 0, 0), (popup_x, popup_y, popup_width, popup_height), 2)

        for i, save_file in enumerate(save_files):
            text = self.font.render(save_file, True, (0, 0, 0))
            text_rect = text.get_rect(center=(popup_x + popup_width // 2, popup_y + 50 + i * 40))
            self.screen.blit(text, text_rect)

        back_text = self.font.render("Back", True, (0, 0, 0))
        back_rect = back_text.get_rect(center=(popup_x + popup_width // 2, popup_y + popup_height - 30))
        self.screen.blit(back_text, back_rect)

        pygame.display.flip()

    def draw_help_popup(self):
        popup_width = 400
        popup_height = 300
        popup_x = (self.screen.get_width() - popup_width) // 2
        popup_y = (self.screen.get_height() - popup_height) // 2

        self.screen.fill((255, 255, 255))
        pygame.draw.rect(self.screen, (0, 0, 0), (popup_x, popup_y, popup_width, popup_height), 2)

        help_text = [
            "Movement: Arrow keys",
            "Save: Press 'S'",
            "Goal: Reach the exit"
        ]
        for i, line in enumerate(help_text):
            text = self.font.render(line, True, (0, 0, 0))
            text_rect = text.get_rect(center=(popup_x + popup_width // 2, popup_y + 50 + i * 40))
            self.screen.blit(text, text_rect)

        back_text = self.font.render("Back", True, (0, 0, 0))
        back_rect = back_text.get_rect(center=(popup_x + popup_width // 2, popup_y + popup_height - 30))
        self.screen.blit(back_text, back_rect)

        pygame.display.flip()

        return back_rect

    def get_clicked_option(self, pos):
        for i, option in enumerate(["Save", "Load", "Help", "Back", "Main Menu", "Exit Game"]):
            text = self.font.render(option, True, (0, 0, 0))
            text_rect = text.get_rect(center=(self.screen.get_width() // 2, 200 + i * 50))
            if text_rect.collidepoint(pos):
                return option
        return None

    def get_clicked_save_file(self, pos, save_files):
        popup_width = 400
        popup_height = 300
        popup_x = (self.screen.get_width() - popup_width) // 2
        popup_y = (self.screen.get_height() - popup_height) // 2

        for i, save_file in enumerate(save_files):
            text = self.font.render(save_file, True, (0, 0, 0))
            text_rect = text.get_rect(center=(popup_x + popup_width // 2, popup_y + 50 + i * 40))
            if text_rect.collidepoint(pos):
                return save_file

        back_text = self.font.render("Back", True, (0, 0, 0))
        back_rect = back_text.get_rect(center=(popup_x + popup_width // 2, popup_y + popup_height - 30))
        if back_rect.collidepoint(pos):
            return "Back"

        return None
