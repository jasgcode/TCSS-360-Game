import pygame

class MazeEndView:
    def __init__(self, screen, width, height):
        self.screen = screen
        self.width = width
        self.height = height
        # Load the 8-bit font
        self.font = pygame.font.Font("PressStart2P-Regular.ttf", 24)
        self.button_font = pygame.font.Font("PressStart2P-Regular.ttf", 24)
        self.congrats_text = self.font.render("Congratulations!", True, (0, 0, 0))
        self.end_text = self.font.render("Unfortunately, you didn't pass your sobriety tests.", True, (0, 0, 0))
        self.button_text = self.button_font.render("Main Menu", True, (0, 0, 0))
        self.button_rect = pygame.Rect(self.width // 2 - 100, self.height // 2 + 50, 200, 50)

    def draw(self):
        self.screen.fill((240, 240, 220))  # Fill screen with gray
        self.screen.blit(self.congrats_text,
                         (self.width // 2 - self.congrats_text.get_width() // 2, self.height // 2 - 100))
        pygame.draw.rect(self.screen, (240, 240, 220), self.button_rect)
        self.screen.blit(self.button_text,
                         (self.button_rect.x + (self.button_rect.width - self.button_text.get_width()) // 2,
                          self.button_rect.y + (self.button_rect.height - self.button_text.get_height()) // 2))
        pygame.display.flip()

    def draw_end(self):
        self.screen.fill((240, 240, 220))  # Fill screen with gray
        self.screen.blit(self.end_text,
                         (self.width // 2 - self.end_text.get_width() // 2, self.height // 2 - 100))
        pygame.draw.rect(self.screen, (240, 240, 220), self.button_rect)
        self.screen.blit(self.button_text,
                         (self.button_rect.x + (self.button_rect.width - self.button_text.get_width()) // 2,
                          self.button_rect.y + (self.button_rect.height - self.button_text.get_height()) // 2))
        pygame.display.flip()

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.button_rect.collidepoint(event.pos):
                return "main_menu"
        return None

