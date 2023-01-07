# Типы объектов: Игрок, ландшафт, пуля (вражескую, собственная), турели, боссы, (ящики с баффами)
# Типы взаимодействий: Игрок - ландшафт (и турели), игрок - вражеская пуля, пуля - ландшафт, ящики с баффами - ландшафт, пуля - боссы
import pygame, sys

pygame.init()

SCREEN_WIDTH = 1920
SCREEN_HEIGHT = 1080
OOB = (10000, 10000)

SCREEN = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

PATH_INDENT = -12

background = pygame.image.load("Resources/Textures/menu_background.png")

class Button():
    def __init__(self, image, image_path, pos, difficulty_button = 0):
        self.image = image
        self.image_path = image_path
        self.x_pos = pos[0]
        self.y_pos = pos[1]
        self.rect = self.image.get_rect(center=(self.x_pos, self.y_pos))
        self.difficulty_button = difficulty_button

    def update(self, screen):
        if self.image is not None:
            screen.blit(self.image, self.rect)

    def checkForInput(self, position):
        if position[0] in range(self.rect.left, self.rect.right) and position[1] in range(self.rect.top,
                                                                                          self.rect.bottom):
            return True
        return False

    def changeCondition(self, position):
        if not self.difficulty_button:
            if position[0] in range(self.rect.left, self.rect.right) and position[1] in range(self.rect.top,
                                                                                          self.rect.bottom):
                self.image_path = self.image_path[:PATH_INDENT] + "_enabled.png"
                self.image = pygame.image.load(self.image_path)
            else:
                self.image_path = self.image_path[:PATH_INDENT] + "disabled.png"
                self.image = pygame.image.load(self.image_path)
        else:
            if position[0] in range(self.rect.left, self.rect.right) and position[1] in range(self.rect.top,
                                                                                          self.rect.bottom):
                self.image_path = self.image_path[:PATH_INDENT] + "_enabled.png"
                self.image = pygame.image.load(self.image_path)
                difficulty_description = pygame.image.load("Resources/Textures/difficulty_description_label.png")
                SCREEN.blit(difficulty_description, (400, 400))
                if self.difficulty_button == 1:
                    description_text_part01 = get_font(10).render("Beginner difficulty (I'm Too Young to Die):" , True, "#605b00")
                    description_rect_part01 = description_text_part01.get_rect(center=(672, 418))
                    SCREEN.blit(description_text_part01, description_rect_part01)
                    description_text_part02 = get_font(10).render("   - Guaranted drop from every enemy" , True, "#605b00")
                    description_rect_part02 = description_text_part02.get_rect(center=(690, 450))
                    SCREEN.blit(description_text_part02, description_rect_part02)
                    description_text_part03 = get_font(10).render("   - 3 additional lifes in every attempt" , True, "#605b00")
                    description_rect_part03 = description_text_part03.get_rect(center=(710, 485))
                    SCREEN.blit(description_text_part03, description_rect_part03)
                    description_text_part04 = get_font(10).render("   - Slow turrets and bullets" , True, "#605b00")
                    description_rect_part04 = description_text_part04.get_rect(center=(655, 520))
                    SCREEN.blit(description_text_part04, description_rect_part04)
                    beginner_difficulty = pygame.image.load("Resources/Textures/beginner_difficulty_icon.png")
                    SCREEN.blit(beginner_difficulty, (420, 450))
                if self.difficulty_button == 2:
                    description_text_part01 = get_font(10).render("Medium difficulty (Hurt Me Plenty):" , True, "#605b00")
                    description_rect_part01 = description_text_part01.get_rect(center=(672, 418))
                    SCREEN.blit(description_text_part01, description_rect_part01)
                    description_text_part02 = get_font(10).render("   - 70% chance of drop from every enemy" , True, "#605b00")
                    description_rect_part02 = description_text_part02.get_rect(center=(710, 450))
                    SCREEN.blit(description_text_part02, description_rect_part02)
                    description_text_part03 = get_font(10).render("   - 2 additional lifes in every attempt" , True, "#605b00")
                    description_rect_part03 = description_text_part03.get_rect(center=(710, 485))
                    SCREEN.blit(description_text_part03, description_rect_part03)
                    description_text_part04 = get_font(10).render("   - Normal reaction of" , True, "#605b00")
                    description_rect_part04 = description_text_part04.get_rect(center=(625, 520))
                    SCREEN.blit(description_text_part04, description_rect_part04)
                    description_text_part05 = get_font(10).render("turrets and bullets speed" , True, "#605b00")
                    description_rect_part05 = description_text_part05.get_rect(center=(665, 555))
                    SCREEN.blit(description_text_part05, description_rect_part05)
                    medium_difficulty = pygame.image.load("Resources/Textures/medium_difficulty_icon.png")
                    SCREEN.blit(medium_difficulty, (420, 450))
                if self.difficulty_button == 3:
                    description_text_part01 = get_font(10).render("Hard difficulty (Ultra Violence):" , True, "#605b00")
                    description_rect_part01 = description_text_part01.get_rect(center=(672, 418))
                    SCREEN.blit(description_text_part01, description_rect_part01)
                    description_text_part02 = get_font(10).render("   - 35% chance of drop from every enemy" , True, "#605b00")
                    description_rect_part02 = description_text_part02.get_rect(center=(710, 450))
                    SCREEN.blit(description_text_part02, description_rect_part02)
                    description_text_part03 = get_font(10).render("   - 1 additional lifes in every attempt" , True, "#605b00")
                    description_rect_part03 = description_text_part03.get_rect(center=(710, 485))
                    SCREEN.blit(description_text_part03, description_rect_part03)
                    description_text_part04 = get_font(10).render("   - Very fast reaction of" , True, "#605b00")
                    description_rect_part04 = description_text_part04.get_rect(center=(640, 520))
                    SCREEN.blit(description_text_part04, description_rect_part04)
                    description_text_part05 = get_font(10).render("turrets and bullets speed" , True, "#605b00")
                    description_rect_part05 = description_text_part05.get_rect(center=(665, 555))
                    SCREEN.blit(description_text_part05, description_rect_part05)
                    hard_difficulty = pygame.image.load("Resources/Textures/hard_difficulty_icon.png")
                    SCREEN.blit(hard_difficulty, (420, 450))
                if self.difficulty_button == 4:
                    description_text_part01 = get_font(10).render("Insane difficulty (Nightmare):" , True, "#605b00")
                    description_rect_part01 = description_text_part01.get_rect(center=(672, 418))
                    SCREEN.blit(description_text_part01, description_rect_part01)
                    description_text_part02 = get_font(10).render("   - Any drop is absent" , True, "#605b00")
                    description_rect_part02 = description_text_part02.get_rect(center=(625, 450))
                    SCREEN.blit(description_text_part02, description_rect_part02)
                    description_text_part03 = get_font(10).render("   - Additional lifes is absent" , True, "#605b00")
                    description_rect_part03 = description_text_part03.get_rect(center=(665, 480))
                    SCREEN.blit(description_text_part03, description_rect_part03)
                    description_text_part04 = get_font(10).render("   - Perfect reaction of" , True, "#605b00")
                    description_rect_part04 = description_text_part04.get_rect(center=(630, 510))
                    SCREEN.blit(description_text_part04, description_rect_part04)
                    description_text_part05 = get_font(10).render("turrets and bullets speed" , True, "#605b00")
                    description_rect_part05 = description_text_part05.get_rect(center=(665, 540))
                    SCREEN.blit(description_text_part05, description_rect_part05)
                    description_text_part06 = get_font(10).render("   - No hope..." , True, "#605b00")
                    description_rect_part06 = description_text_part06.get_rect(center=(585, 570))
                    SCREEN.blit(description_text_part06, description_rect_part06)
                    insane_difficulty = pygame.image.load("Resources/Textures/insane_difficulty_icon.png")
                    SCREEN.blit(insane_difficulty, (420, 450))
            else:
                self.image_path = self.image_path[:PATH_INDENT] + "disabled.png"
                self.image = pygame.image.load(self.image_path)



def get_font(size):
    return pygame.font.Font("Resources/Textures/font.ttf", size)


def difficulty_list(return_to_main_menu_P, choose_difficulty):
    difficulty_list_opened = True
    while difficulty_list_opened:
        diffculty_list_mouse_pos = pygame.mouse.get_pos()

        choose_difficulty.changeCondition(diffculty_list_mouse_pos)
        choose_difficulty.update(SCREEN)

        return_to_main_menu_P.changeCondition(diffculty_list_mouse_pos)
        return_to_main_menu_P.update(SCREEN)
        
        beginner_difficulty = Button(image = pygame.image.load("Resources/Textures/Difficulty buttons/beginner_difficulty_button_disabled.png"), image_path = "Resources/Textures/Difficulty buttons/beginner_difficulty_button_disabled.png", pos = (1500, 300), difficulty_button = 1)
    
        beginner_difficulty.changeCondition(diffculty_list_mouse_pos)
        beginner_difficulty.update(SCREEN)

        medium_difficulty = Button(image = pygame.image.load("Resources/Textures/Difficulty buttons/medium_difficulty_button_disabled.png"), image_path = "Resources/Textures/Difficulty buttons/medium_difficulty_button_disabled.png", pos = (1500, 400), difficulty_button = 2)

        medium_difficulty.changeCondition(diffculty_list_mouse_pos)
        medium_difficulty.update(SCREEN)

        hard_difficulty = Button(image = pygame.image.load("Resources/Textures/Difficulty buttons/hard_difficulty_button_disabled.png"), image_path = "Resources/Textures/Difficulty buttons/hard_difficulty_button_disabled.png", pos = (1500, 500), difficulty_button = 3)

        hard_difficulty.changeCondition(diffculty_list_mouse_pos)
        hard_difficulty.update(SCREEN)

        insane_difficulty = Button(image = pygame.image.load("Resources/Textures/Difficulty buttons/insane_difficulty_button_disabled.png"), image_path = "Resources/Textures/Difficulty buttons/insane_difficulty_button_disabled.png", pos = (1500, 600), difficulty_button = 4)

        insane_difficulty.changeCondition(diffculty_list_mouse_pos)
        insane_difficulty.update(SCREEN)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if return_to_main_menu_P.checkForInput(diffculty_list_mouse_pos):
                    main_menu() 
                if choose_difficulty.checkForInput(diffculty_list_mouse_pos):
                    difficulty_list_opened = False
        pygame.display.update()
    pygame.display.update()


def play():
    while True:
        play_mouse_pos = pygame.mouse.get_pos()

        SCREEN.fill("#121212")

        choose_difficulty = Button(image = pygame.image.load("Resources/Textures/Difficulty buttons/difficulty_button_disabled.png"), image_path = "Resources/Textures/Difficulty buttons/difficulty_button_disabled.png", pos = (1500, 200))

        choose_difficulty.changeCondition(play_mouse_pos)
        choose_difficulty.update(SCREEN)

        return_to_main_menu_P = Button(image = pygame.image.load("Resources/Textures/return_button_disabled.png"), image_path = "Resources/Textures/return_button_disabled.png", pos = (310, 900))

        return_to_main_menu_P.changeCondition(play_mouse_pos)
        return_to_main_menu_P.update(SCREEN)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if return_to_main_menu_P.checkForInput(play_mouse_pos):
                    main_menu()
                if choose_difficulty.checkForInput(play_mouse_pos):
                    difficulty_list(return_to_main_menu_P, choose_difficulty)
        pygame.display.update()

def level_01():
    pass

def level_02():
    pass

def level_03():
    pass

def options():
    while True:
        options_mouse_pos = pygame.mouse.get_pos()

        SCREEN.fill("#121212")

        return_to_main_menu_O = Button(image = pygame.image.load("Resources/Textures/return_button_disabled.png"), image_path = "Resources/Textures/return_button_disabled.png", pos = (310, 900))

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
