import pygame

#class menu for my game over and start menu
class Menu():
    def __init__(self):
        super().__init__()
        self.input_active = False
        self.player_name = ''
        self.cursor_timer = 0
        self.cursor_visible = True
        self.input_box = pygame.Rect(200, 250, 400, 50)
        self.font = pygame.font.SysFont("monospace", 16)

    #handle when input is pressed
    def check_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.input_box.collidepoint(event.pos):
                self.input_active = not self.input_active
            else:
                self.input_active = False
        #get the name of the player when written and store it
        if event.type == pygame.KEYDOWN:
            if self.input_active:
                if event.key == pygame.K_BACKSPACE:
                    self.player_name = self.player_name[:-1]
                elif event.key != pygame.K_SPACE and event.unicode.isalnum():
                    self.player_name += event.unicode 

    #handle cursor
    def update(self):
        self.cursor_timer += pygame.time.Clock().get_time()
        if self.cursor_timer >= 500:
            self.cursor_visible = not self.cursor_visible
            self.cursor_timer = 0

    #menu content and how it displays
    def display(self, screen):
        screen.fill([255, 255, 255])

        text_surface = self.font.render("Press space to start", True, (0, 0, 0))
        text_rect = text_surface.get_rect(center=(screen.get_width() // 2, screen.get_height() // 2 - 50))
        screen.blit(text_surface, text_rect)

        enter_name_txt = self.font.render(">", True, (0, 0, 0))
        txt_surface = self.font.render(self.player_name, True, (0, 0, 0))
    
        input_y_position = text_rect.bottom + 30  
        screen.blit(enter_name_txt, (screen.get_width() // 2 - 100, input_y_position))
        screen.blit(txt_surface, (screen.get_width() // 2 - 80, input_y_position))

        if self.input_active and self.cursor_visible:
            cursor_x = screen.get_width() // 2 - 80 + txt_surface.get_width()
            cursor_y = input_y_position
            cursor_height = txt_surface.get_height()
            pygame.draw.line(screen, (0, 0, 0), (cursor_x, cursor_y), (cursor_x, cursor_y + cursor_height), 2)

        width = max(400, txt_surface.get_width() + 10)
        self.input_box.w = width
