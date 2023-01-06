import pygame, sys

pygame.init()

SCREEN_WIDTH = 1920
SCREEN_HEIGHT = 1080

SCREEN = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

PATH_INDENT = -12

background = pygame.image.load("Resources/Textures/menu_background.png")

class Button():
    def __init__(self, image, image_path, pos):
        self.image = image
        self.image_path = image_path
        self.x_pos = pos[0]
        self.y_pos = pos[1]
        self.rect = self.image.get_rect(center=(self.x_pos, self.y_pos))

    def update(self, screen):
        if self.image is not None:
            screen.blit(self.image, self.rect)

    def checkForInput(self, position):
        if position[0] in range(self.rect.left, self.rect.right) and position[1] in range(self.rect.top,
                                                                                          self.rect.bottom):
            return True
        return False

    def changeCondition(self, position):
        if position[0] in range(self.rect.left, self.rect.right) and position[1] in range(self.rect.top,
                                                                                          self.rect.bottom):
            self.image_path = self.image_path[:PATH_INDENT] + "_enabled.png"
            self.image = pygame.image.load(self.image_path)
        else:
            self.image_path = self.image_path[:PATH_INDENT] + "disabled.png"
            self.image = pygame.image.load(self.image_path)


def get_font(size):
    return pygame.font.Font("Resources/Textures/font.ttf", size)


def play():
    while True:
        play_mouse_pos = pygame.mouse.get_pos()

        SCREEN.fill("black")

        PLAY_TEXT = get_font(45).render("This is the PLAY screen.", True, "White")
        PLAY_RECT = PLAY_TEXT.get_rect(center=(960, 380))
        SCREEN.blit(PLAY_TEXT, PLAY_RECT)

        return_to_main_menu_P = Button(image = pygame.image.load("Resources/Textures/return_button_disabled.png"), image_path = "Resources/Textures/return_button_disabled.png", pos = (960, 600))

        return_to_main_menu_P.changeCondition(play_mouse_pos)
        return_to_main_menu_P.update(SCREEN)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if return_to_main_menu_P.checkForInput(play_mouse_pos):
                    main_menu()

        pygame.display.update()


def options():
    while True:
        options_mouse_pos = pygame.mouse.get_pos()

        SCREEN.fill("black")

        OPTIONS_TEXT = get_font(45).render("This is the OPTIONS screen.", True, "White")
        OPTIONS_RECT = OPTIONS_TEXT.get_rect(center=(960, 380))
        SCREEN.blit(OPTIONS_TEXT, OPTIONS_RECT)

        return_to_main_menu_O = Button(image = pygame.image.load("Resources/Textures/return_button_disabled.png"), image_path = "Resources/Textures/return_button_disabled.png", pos = (960, 600))

        return_to_main_menu_O.changeCondition(options_mouse_pos)
        return_to_main_menu_O.update(SCREEN)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if return_to_main_menu_O.checkForInput(options_mouse_pos):
                    main_menu()

        pygame.display.update()


def main_menu():
    while True:
        SCREEN.blit(background, (240, 0))

        menu_mouse_pos = pygame.mouse.get_pos()

        menu_text = get_font(100).render("GRAND BATTLE", True, "#b68f40")
        menu_rect = menu_text.get_rect(center=(960, 200))

        play_button = Button(image = pygame.image.load("Resources/Textures/play_button_disabled.png"), image_path = "Resources/Textures/play_button_disabled.png", pos = (960, 400))
        options_button = Button(image = pygame.image.load("Resources/Textures/options_button_disabled.png"), image_path = "Resources/Textures/options_button_disabled.png", pos = (960, 600))
        quit_button = Button(image = pygame.image.load("Resources/Textures/quit_button_disabled.png"), image_path = "Resources/Textures/quit_button_disabled.png", pos = (960, 800))

        SCREEN.blit(menu_text, menu_rect)

        for button in [play_button, options_button, quit_button]:
            button.changeCondition(menu_mouse_pos)
            button.update(SCREEN)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if play_button.checkForInput(menu_mouse_pos):
                    play()
                if options_button.checkForInput(menu_mouse_pos):
                    options()
                if quit_button.checkForInput(menu_mouse_pos):
                    pygame.quit()
                    sys.exit()
        pygame.display.update()


main_menu()
