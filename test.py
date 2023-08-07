import pygame
import sys

class DropdownSelector:
    def __init__(self, x, y, width, height, options, placeholder):
        self.rect = pygame.Rect(x, y, width, height)
        self.options = options
        self.selected_option = None
        self.show_options = False
        self.font = pygame.font.Font(None, 24)
        self.placeholder = placeholder

    def draw(self, screen):
        # Draw the dropdown box
        pygame.draw.rect(screen, (255, 255, 255), self.rect, 2)

        # Draw the currently selected option or the placeholder
        text = self.selected_option if self.selected_option else self.placeholder
        text_surface = self.font.render(text, True, (255, 255, 255))
        screen.blit(text_surface, (self.rect.x + 5, self.rect.y + 5))

        # Draw the options if the dropdown is open
        if self.show_options:
            for i, option in enumerate(self.options):
                option_rect = pygame.Rect(self.rect.x, self.rect.y + (i + 1) * self.rect.height,
                                          self.rect.width, self.rect.height)
                pygame.draw.rect(screen, (255, 255, 255), option_rect, 2)

                option_surface = self.font.render(option, True, (255, 255, 255))
                screen.blit(option_surface, (option_rect.x + 5, option_rect.y + 5))

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:  # Left mouse button
                if self.rect.collidepoint(event.pos):
                    self.show_options = not self.show_options
                elif self.show_options:
                    for i, option in enumerate(self.options):
                        option_rect = pygame.Rect(self.rect.x, self.rect.y + (i + 1) * self.rect.height,
                                                  self.rect.width, self.rect.height)
                        if option_rect.collidepoint(event.pos):
                            self.selected_option = option
                            self.show_options = False

if __name__ == "__main__":
    pygame.init()
    screen = pygame.display.set_mode((400, 300))
    pygame.display.set_caption("Dropdown Selector")

    options = ["Slow", "Medium", "Fast"]
    placeholder = "Select an Alien Speed"
    dropdown = DropdownSelector(50, 50, 200, 30, options, placeholder)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            dropdown.handle_event(event)

        screen.fill((0, 0, 0))
        dropdown.draw(screen)
        pygame.display.flip()
