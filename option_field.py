import pygame

class OptionField:
    def __init__(self, ai_game, x_position, y_position, options, placeholder):
        # set screen to the alien invasion game screen
        self.screen = ai_game.screen
        
        # create rect with 200 width and 30 height
        self.rect = pygame.Rect(x_position, y_position, 200,30)
        self.options = options
        self.selected_option = None
        self.show_options = False
        self.font = pygame.font.Font(None, 24)
        self.placeholder = placeholder

    def draw_button(self):
        border_thickness = 2  # Thickness of the border in pixels

        # Draw dropdown box
        pygame.draw.rect(self.screen, (0, 135, 0), self.rect)

        # Draw selected option or placeholder
        text = self.selected_option if self.selected_option else self.placeholder
        text_surface = self.font.render(text, True, (255, 255, 255))
        text_rect = text_surface.get_rect(center=self.rect.center)
        self.screen.blit(text_surface, text_rect.topleft)

        # Draw the options if the dropdown is open
        if self.show_options:
            for i, option in enumerate(self.options):
                option_rect = pygame.Rect(
                    self.rect.x, 
                    self.rect.y + (i + 1) * self.rect.height,
                    self.rect.width,
                    self.rect.height
                )
                pygame.draw.rect(self.screen, (0, 135, 0), option_rect)

                # Draw white border inside the option rectangle
                inner_rect = option_rect.inflate(-border_thickness, -border_thickness)
                pygame.draw.rect(self.screen, (255, 255, 255), inner_rect, border_thickness)

                option_surface = self.font.render(option, True, (255, 255, 255))
                option_text_rect = option_surface.get_rect(center=option_rect.center)
                self.screen.blit(
                    option_surface,
                    option_text_rect.topleft
                )



    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1: # Left mouse click
                if self.rect.collidepoint(event.pos):
                    self.show_options = not self.show_options
                elif self.show_options:
                    for i, option in enumerate(self.options):
                        option_rect = pygame.Rect(
                            self.rect.x, 
                            self.rect.y + (i + 1) * self.rect.height,
                            self.rect.width, 
                            self.rect.height
                        )
                        if option_rect.collidepoint(event.pos):
                            self.selected_option = option
                            self.show_options = False
