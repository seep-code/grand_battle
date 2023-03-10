# Типы объектов: Игрок, ландшафт, пуля (вражескую, собственная), турели, боссы, (ящики с баффами)
# Типы взаимодействий: Игрок - ландшафт (и турели), игрок - вражеская пуля, пуля - ландшафт, ящики с баффами - ландшафт, пуля - боссы
import pygame, sys

pygame.init()

SCREEN_WIDTH = 1920
SCREEN_HEIGHT = 1080
SCREEN = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

OOB = (10000, 10000)

PATH_INDENT = -12

DESCRIPTION_FONT_SIZE = 10

LEVEL_STATUS_FONT_SIZE = 24

background = pygame.image.load("Resources/Textures/menu_background.png")

background_theme = pygame.mixer.Sound("Resources/Sounds/background_theme.mp3")
boss_theme = pygame.mixer.Sound("Resources/Sounds/boss_theme.mp3")
button_click_sound = pygame.mixer.Sound("Resources/Sounds/button_click_sound.mp3")
credits_theme = pygame.mixer.Sound("Resources/Sounds/credits_theme.mp3")
destruction_sound = pygame.mixer.Sound("Resources/Sounds/destruction_sound.mp3")
game_over_sound = pygame.mixer.Sound("Resources/Sounds/game_over_sound.mp3")
jump_sound = pygame.mixer.Sound("Resources/Sounds/jump_sound.mp3")
shot_sound = pygame.mixer.Sound("Resources/Sounds/shot_sound.mp3")
victory_sound = pygame.mixer.Sound("Resources/Sounds/victory_sound.mp3")

info = open('Resources/Other/info.txt')
data = info.readlines()

SONG_VOLUME = 0
SOUNDS_VOLUME = 0

for i in range(16, 26):
    if data[i][:2] == "on":
        SONG_VOLUME += 10
for i in range(27, 37):
    if data[i][:2] == "on":
        SOUNDS_VOLUME += 10

background_theme.play(-1)
background_theme.set_volume(SONG_VOLUME / 100)

CHOSEN_DIFFICULTY = 'beginner'

#0 - ничего, T - турель (центр), P - платформа
MAP_MATRIX = []
for i in range(18):
    MAP_MATRIX.append([])
    for j in range(120):
        if i == 0 or i == 17 or j == 0 or j == 119:
            MAP_MATRIX[len(MAP_MATRIX) - 1].append('P')
        else:
            MAP_MATRIX[len(MAP_MATRIX) - 1].append('0')

class Button():
    def __init__(self, image, image_path, pos, difficulty_button = 0, level_button = 0):
        self.image = image
        self.image_path = image_path
        self.x_pos = pos[0]
        self.y_pos = pos[1]
        self.rect = self.image.get_rect(center=(self.x_pos, self.y_pos))
        self.difficulty_button = difficulty_button
        self.level_button = level_button

    def update(self, screen):
        if self.image is not None:
            screen.blit(self.image, self.rect)

    def checkForInput(self, position):
        if position[0] in range(self.rect.left, self.rect.right) and position[1] in range(self.rect.top,
                                                                                          self.rect.bottom):
            return True
        return False

    def changeCondition(self, position):
        global data
        global CHOSEN_DIFFICULTY
        c_d = 0
        if CHOSEN_DIFFICULTY == 'medium':
            c_d = 1
        if CHOSEN_DIFFICULTY == 'hard':
            c_d = 2
        if CHOSEN_DIFFICULTY == 'insane':
            c_d = 3
        if position[0] in range(self.rect.left, self.rect.right) and position[1] in range(self.rect.top,
                                                                                    self.rect.bottom):
            self.image_path = self.image_path[:PATH_INDENT] + "_enabled.png"
            self.image = pygame.image.load(self.image_path)
        else:
            self.image_path = self.image_path[:PATH_INDENT] + "disabled.png"
            self.image = pygame.image.load(self.image_path)
        if self.level_button:
            if position[0] in range(self.rect.left, self.rect.right) and position[1] in range(self.rect.top,
                                                                                          self.rect.bottom):
                l_b = self.level_button - 1
                status = data[c_d * 4 + l_b][0] + " stars"
                time = data[38 + c_d * 12 + l_b * 4][0:2] + " hr " + data[39 + c_d * 12 + l_b * 4][0:2] + " min " + data[40 + c_d * 12 + l_b * 4][0:2] + " sec"
                if data[c_d * 4 + l_b][0:2] == '00':
                    status = "not completed"
                if data[38 + c_d * 12 + l_b * 4][0:2] == "00" and data[39 + c_d * 12 + l_b * 4][0:2] == "00" and data[40 + c_d * 12 + l_b * 4][0:2] == "00":
                    time = "-"
                level_status_text = get_font(LEVEL_STATUS_FONT_SIZE).render("Status: " + status, True, "#b68f40")
                level_status_rect = level_status_text.get_rect(center=(1000, 800))
                level_time_text = get_font(LEVEL_STATUS_FONT_SIZE).render("Time: " + time, True, "#b68f40")
                level_time_rect = level_time_text.get_rect(center=(1000, 830))
                SCREEN.blit(level_status_text, level_status_rect)
                SCREEN.blit(level_time_text, level_time_rect)
        if self.difficulty_button:
            if position[0] in range(self.rect.left, self.rect.right) and position[1] in range(self.rect.top,
                                                                                          self.rect.bottom):
                level01_icon_path = "Resources/Textures/Level buttons/level01_button_stars-" + data[(self.difficulty_button - 1) * 4][0] + "_disabled.png"
                level02_icon_path = "Resources/Textures/Level buttons/level02_button_stars-" + data[(self.difficulty_button - 1) * 4 + 1][0] + "_disabled.png"
                level03_icon_path = "Resources/Textures/Level buttons/level03_button_stars-" + data[(self.difficulty_button - 1) * 4 + 2][0] + "_disabled.png"
                level01_icon = pygame.image.load(level01_icon_path)
                level02_icon = pygame.image.load(level02_icon_path)
                level03_icon = pygame.image.load(level03_icon_path)
                SCREEN.blit(level01_icon, (250, 150))
                SCREEN.blit(level02_icon, (600, 150))
                SCREEN.blit(level03_icon, (950, 150))
                difficulty_description = pygame.image.load("Resources/Textures/difficulty_description_label.png")
                SCREEN.blit(difficulty_description, (400, 500))
                if self.difficulty_button == 1:
                    description_text_part01 = get_font(DESCRIPTION_FONT_SIZE).render("Beginner difficulty (I'm Too Young to Die):" , True, "#605b00")
                    description_rect_part01 = description_text_part01.get_rect(center=(672, 518))
                    SCREEN.blit(description_text_part01, description_rect_part01)
                    description_text_part02 = get_font(DESCRIPTION_FONT_SIZE).render("   - Guaranted drop from every enemy" , True, "#605b00")
                    description_rect_part02 = description_text_part02.get_rect(center=(690, 550))
                    SCREEN.blit(description_text_part02, description_rect_part02)
                    description_text_part03 = get_font(DESCRIPTION_FONT_SIZE).render("   - 3 additional lifes in every attempt" , True, "#605b00")
                    description_rect_part03 = description_text_part03.get_rect(center=(710, 585))
                    SCREEN.blit(description_text_part03, description_rect_part03)
                    description_text_part04 = get_font(DESCRIPTION_FONT_SIZE).render("   - Slow turrets and bullets" , True, "#605b00")
                    description_rect_part04 = description_text_part04.get_rect(center=(655, 620))
                    SCREEN.blit(description_text_part04, description_rect_part04)
                    beginner_difficulty = pygame.image.load("Resources/Textures/beginner_difficulty_icon.png")
                    SCREEN.blit(beginner_difficulty, (420, 550))
                if self.difficulty_button == 2:
                    description_text_part01 = get_font(DESCRIPTION_FONT_SIZE).render("Medium difficulty (Hurt Me Plenty):" , True, "#605b00")
                    description_rect_part01 = description_text_part01.get_rect(center=(672, 518))
                    SCREEN.blit(description_text_part01, description_rect_part01)
                    description_text_part02 = get_font(DESCRIPTION_FONT_SIZE).render("   - 70% chance of drop from every enemy" , True, "#605b00")
                    description_rect_part02 = description_text_part02.get_rect(center=(710, 550))
                    SCREEN.blit(description_text_part02, description_rect_part02)
                    description_text_part03 = get_font(DESCRIPTION_FONT_SIZE).render("   - 2 additional lifes in every attempt" , True, "#605b00")
                    description_rect_part03 = description_text_part03.get_rect(center=(710, 585))
                    SCREEN.blit(description_text_part03, description_rect_part03)
                    description_text_part04 = get_font(DESCRIPTION_FONT_SIZE).render("   - Normal reaction of" , True, "#605b00")
                    description_rect_part04 = description_text_part04.get_rect(center=(625, 620))
                    SCREEN.blit(description_text_part04, description_rect_part04)
                    description_text_part05 = get_font(DESCRIPTION_FONT_SIZE).render("turrets and bullets speed" , True, "#605b00")
                    description_rect_part05 = description_text_part05.get_rect(center=(665, 655))
                    SCREEN.blit(description_text_part05, description_rect_part05)
                    medium_difficulty = pygame.image.load("Resources/Textures/medium_difficulty_icon.png")
                    SCREEN.blit(medium_difficulty, (420, 550))
                if self.difficulty_button == 3:
                    description_text_part01 = get_font(DESCRIPTION_FONT_SIZE).render("Hard difficulty (Ultra Violence):" , True, "#605b00")
                    description_rect_part01 = description_text_part01.get_rect(center=(672, 518))
                    SCREEN.blit(description_text_part01, description_rect_part01)
                    description_text_part02 = get_font(DESCRIPTION_FONT_SIZE).render("   - 35% chance of drop from every enemy" , True, "#605b00")
                    description_rect_part02 = description_text_part02.get_rect(center=(710, 550))
                    SCREEN.blit(description_text_part02, description_rect_part02)
                    description_text_part03 = get_font(DESCRIPTION_FONT_SIZE).render("   - 1 additional lifes in every attempt" , True, "#605b00")
                    description_rect_part03 = description_text_part03.get_rect(center=(710, 585))
                    SCREEN.blit(description_text_part03, description_rect_part03)
                    description_text_part04 = get_font(DESCRIPTION_FONT_SIZE).render("   - Very fast reaction of" , True, "#605b00")
                    description_rect_part04 = description_text_part04.get_rect(center=(640, 620))
                    SCREEN.blit(description_text_part04, description_rect_part04)
                    description_text_part05 = get_font(DESCRIPTION_FONT_SIZE).render("turrets and bullets speed" , True, "#605b00")
                    description_rect_part05 = description_text_part05.get_rect(center=(665, 655))
                    SCREEN.blit(description_text_part05, description_rect_part05)
                    hard_difficulty = pygame.image.load("Resources/Textures/hard_difficulty_icon.png")
                    SCREEN.blit(hard_difficulty, (420, 550))
                if self.difficulty_button == 4:
                    description_text_part01 = get_font(DESCRIPTION_FONT_SIZE).render("Insane difficulty (Nightmare):" , True, "#605b00")
                    description_rect_part01 = description_text_part01.get_rect(center=(672, 518))
                    SCREEN.blit(description_text_part01, description_rect_part01)
                    description_text_part02 = get_font(DESCRIPTION_FONT_SIZE).render("   - Any drop is absent" , True, "#605b00")
                    description_rect_part02 = description_text_part02.get_rect(center=(625, 550))
                    SCREEN.blit(description_text_part02, description_rect_part02)
                    description_text_part03 = get_font(DESCRIPTION_FONT_SIZE).render("   - Additional lifes is absent" , True, "#605b00")
                    description_rect_part03 = description_text_part03.get_rect(center=(665, 580))
                    SCREEN.blit(description_text_part03, description_rect_part03)
                    description_text_part04 = get_font(DESCRIPTION_FONT_SIZE).render("   - Perfect reaction of" , True, "#605b00")
                    description_rect_part04 = description_text_part04.get_rect(center=(630, 610))
                    SCREEN.blit(description_text_part04, description_rect_part04)
                    description_text_part05 = get_font(DESCRIPTION_FONT_SIZE).render("turrets and bullets speed" , True, "#605b00")
                    description_rect_part05 = description_text_part05.get_rect(center=(665, 640))
                    SCREEN.blit(description_text_part05, description_rect_part05)
                    description_text_part06 = get_font(DESCRIPTION_FONT_SIZE).render("   - No hope..." , True, "#605b00")
                    description_rect_part06 = description_text_part06.get_rect(center=(585, 670))
                    SCREEN.blit(description_text_part06, description_rect_part06)
                    insane_difficulty = pygame.image.load("Resources/Textures/insane_difficulty_icon.png")
                    SCREEN.blit(insane_difficulty, (420, 550))
            else:
                self.image_path = self.image_path[:PATH_INDENT] + "disabled.png"
                self.image = pygame.image.load(self.image_path)



def get_font(size):
    return pygame.font.Font("Resources/Textures/font.ttf", size)


def difficulty_list(return_to_main_menu_P, choose_difficulty):
    global SOUNDS_VOLUME
    global SONG_VOLUME
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
                    button_click_sound.play()
                    main_menu() 
                if choose_difficulty.checkForInput(diffculty_list_mouse_pos):
                    button_click_sound.play()
                    button_click_sound.set_volume(SOUNDS_VOLUME / 100)
                    difficulty_list_opened = False
                if beginner_difficulty.checkForInput(diffculty_list_mouse_pos):
                    button_click_sound.play()
                    button_click_sound.set_volume(SOUNDS_VOLUME / 100)
                    return 'beginner'
                if medium_difficulty.checkForInput(diffculty_list_mouse_pos):
                    button_click_sound.play()
                    button_click_sound.set_volume(SOUNDS_VOLUME / 100)
                    return 'medium'
                if hard_difficulty.checkForInput(diffculty_list_mouse_pos):
                    button_click_sound.play()
                    button_click_sound.set_volume(SOUNDS_VOLUME / 100)
                    return 'hard'
                if insane_difficulty.checkForInput(diffculty_list_mouse_pos):
                    button_click_sound.play()
                    button_click_sound.set_volume(SOUNDS_VOLUME / 100)
                    return 'insane'
        pygame.display.update()
    pygame.display.update()


def play():
    global CHOSEN_DIFFICULTY
    global SOUNDS_VOLUME
    global SONG_VOLUME
    while True:
        chosen_diff = 0
        if CHOSEN_DIFFICULTY == 'beginner':
            chosen_diff = 0
        if CHOSEN_DIFFICULTY == 'medium':
            chosen_diff = 1
        if CHOSEN_DIFFICULTY == 'hard':
            chosen_diff = 2
        if CHOSEN_DIFFICULTY == 'insane':
            chosen_diff = 3

        play_mouse_pos = pygame.mouse.get_pos()

        SCREEN.fill("#121212")

        choose_difficulty = Button(image = pygame.image.load("Resources/Textures/Difficulty buttons/difficulty_button_disabled.png"), image_path = "Resources/Textures/Difficulty buttons/difficulty_button_disabled.png", pos = (1500, 200))

        choose_difficulty.changeCondition(play_mouse_pos)
        choose_difficulty.update(SCREEN)

        level01_button_path = "Resources/Textures/Level buttons/level01_button_stars-" + data[chosen_diff * 4][0] + "_disabled.png"
        level01_button = Button(image = pygame.image.load(level01_button_path), image_path = level01_button_path, pos = (400, 300), level_button = 1)

        level01_button.changeCondition(play_mouse_pos)
        level01_button.update(SCREEN)

        level02_button_path = "Resources/Textures/Level buttons/level02_button_stars-" + data[chosen_diff * 4 + 1][0] + "_disabled.png"
        level02_button = Button(image = pygame.image.load(level02_button_path), image_path = level02_button_path, pos = (750, 300), level_button = 2)

        level02_button.changeCondition(play_mouse_pos)
        level02_button.update(SCREEN)

        level03_button_path = "Resources/Textures/Level buttons/level03_button_stars-" + data[chosen_diff * 4 + 2][0] + "_disabled.png"
        level03_button = Button(image = pygame.image.load(level03_button_path), image_path = level03_button_path, pos = (1100, 300), level_button = 3)

        level03_button.changeCondition(play_mouse_pos)
        level03_button.update(SCREEN)

        return_to_main_menu_P = Button(image = pygame.image.load("Resources/Textures/return_button_disabled.png"), image_path = "Resources/Textures/return_button_disabled.png", pos = (310, 900))

        return_to_main_menu_P.changeCondition(play_mouse_pos)
        return_to_main_menu_P.update(SCREEN)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if return_to_main_menu_P.checkForInput(play_mouse_pos):
                    button_click_sound.play()
                    button_click_sound.set_volume(SOUNDS_VOLUME / 100)
                    main_menu()
                if choose_difficulty.checkForInput(play_mouse_pos):
                    button_click_sound.play()
                    button_click_sound.set_volume(SOUNDS_VOLUME / 100)
                    CHOSEN_DIFFICULTY = difficulty_list(return_to_main_menu_P, choose_difficulty)
                if level01_button.checkForInput(play_mouse_pos):
                    button_click_sound.play()
                    button_click_sound.set_volume(SOUNDS_VOLUME / 100)
                    level_01()
                if level02_button.checkForInput(play_mouse_pos):
                    button_click_sound.play()
                    button_click_sound.set_volume(SOUNDS_VOLUME / 100)
                    level_02()
                if level03_button.checkForInput(play_mouse_pos):
                    button_click_sound.play()
                    button_click_sound.set_volume(SOUNDS_VOLUME / 100)
                    level_03()
        pygame.display.update()

def level_01():
    global CHOSEN_DIFFICULTY
    DROP_CHANCE = 0
    ADDITIONAL_LIFES = 0
    BULLET_SPEED = 0
    CHARACTER_SPEED = 0
    if CHOSEN_DIFFICULTY == 'beginner':
        DROP_CHANCE = 100
        ADDITIONAL_LIFES = 3
        BULLET_SPEED = 6
    if CHOSEN_DIFFICULTY == 'medium':
        DROP_CHANCE = 70
        ADDITIONAL_LIFES = 2
        BULLET_SPEED = 7
    if CHOSEN_DIFFICULTY == 'hard':
        DROP_CHANCE = 35
        ADDITIONAL_LIFES = 1
        BULLET_SPEED = 8
    if CHOSEN_DIFFICULTY == 'insane':
        DROP_CHANCE = 0
        ADDITIONAL_LIFES = 0
        BULLET_SPEED = 10
        
    MAP_MATRIX[4][15] = 'T'
    MAP_MATRIX[15][19] = 'T'
    MAP_MATRIX[7][30] = 'T'
    MAP_MATRIX[15][35] = 'T'
    MAP_MATRIX[2][47] = 'T'
    MAP_MATRIX[15][45] = 'T'
    MAP_MATRIX[8][53] = 'T'
    MAP_MATRIX[15][53] = 'T'
    MAP_MATRIX[10][74] = 'T'
    MAP_MATRIX[5][83] = 'T'
    MAP_MATRIX[5][86] = 'T'
    MAP_MATRIX[11][89] = 'T'
    MAP_MATRIX[7][113] = 'T'
    
    for i in range(18):
        for j in range(120):
            if i == 0 or i == 17 or j == 0 or j == 119:
                MAP_MATRIX[i][j] = 'P'
            else:
                MAP_MATRIX[i][j] = '0'
            
    for i in range(6, 8):
        for j in range(9, 23):
            MAP_MATRIX[i][j] = 'P'
    for i in range(12, 14):
        for j in range(8, 13):
            MAP_MATRIX[i][j] = 'P'
    for i in range(12, 14):
        for j in range(21, 25):
            MAP_MATRIX[i][j] = 'P'
    for i in range(11, 17):
        for j in range(29, 31):
            MAP_MATRIX[i][j] = 'P'
    for i in range(9, 11):
        for j in range(29, 38):
            MAP_MATRIX[i][j] = 'P'
    for i in range(4, 6):
        for j in range(42, 53):
            MAP_MATRIX[i][j] = 'P'
    for i in range(12, 17):
        for j in range(41, 44):
            MAP_MATRIX[i][j] = 'P'
    for i in range(10, 12):
        for j in range(47, 58):
            MAP_MATRIX[i][j] = 'P'
    for i in range(4, 6):
        for j in range(59, 63):
            MAP_MATRIX[i][j] = 'P'
    for i in range(9, 17):
        for j in range(63, 71):
            MAP_MATRIX[i][j] = 'P'
    for i in range(12, 14):
        for j in range(73, 77):
            MAP_MATRIX[i][j] = 'P'
    for i in range(7, 9):
        for j in range(80, 89):
            MAP_MATRIX[i][j] = 'P'
    for i in range(13, 15):
        for j in range(80, 90):
            MAP_MATRIX[i][j] = 'P'
    for i in range(9, 11):
        for j in range(94, 119):
            MAP_MATRIX[i][j] = 'P'
    for i in range(9, 17):
        for j in range(94, 96):
            MAP_MATRIX[i][j] = 'P'
                               
    clock1 = pygame.time.get_ticks()
    #########################################################
    #--------------------Игровой процесс--------------------#
    #########################################################
    ticks=pygame.time.get_ticks() - clock1
    seconds=int(ticks/1000 % 60)
    minutes=int(ticks/60000 % 60)
    hours=int(ticks/3600000 % 24)
    if seconds < 10:
        seconds = '0' + str(seconds)
    if minutes < 10:
        minutes = '0' + str(minutes)
    if hours < 10:
        hours = '0' + str(hours)
    c_d = 0
    if CHOSEN_DIFFICULTY == 'medium':
        c_d = 1
    if CHOSEN_DIFFICULTY == 'hard':
        c_d = 2
    if CHOSEN_DIFFICULTY == 'insane':
        c_d = 3
    data[38 + c_d * 12 + 0] = str(hours) + '\n'
    data[39 + c_d * 12 + 0] = str(minutes) + '\n'
    data[40 + c_d * 12 + 0] = str(seconds) + '\n'
    info_copy = open('Resources/Other/info.txt', 'w')
    for i in data:
        info_copy.write(i)
    info_copy.close()
    
def level_02():
    global CHOSEN_DIFFICULTY
    DROP_CHANCE = 0
    ADDITIONAL_LIFES = 0
    BULLET_SPEED = 0
    CHARACTER_SPEED = 0
    if CHOSEN_DIFFICULTY == 'beginner':
        DROP_CHANCE = 100
        ADDITIONAL_LIFES = 3
        BULLET_SPEED = 6
    if CHOSEN_DIFFICULTY == 'medium':
        DROP_CHANCE = 70
        ADDITIONAL_LIFES = 2
        BULLET_SPEED = 7
    if CHOSEN_DIFFICULTY == 'hard':
        DROP_CHANCE = 35
        ADDITIONAL_LIFES = 1
        BULLET_SPEED = 8
    if CHOSEN_DIFFICULTY == 'insane':
        DROP_CHANCE = 0
        ADDITIONAL_LIFES = 0
        BULLET_SPEED = 10

    for i in range(18):
        for j in range(120):
            if i == 0 or i == 17 or j == 0 or j == 119:
                MAP_MATRIX[i][j] = 'P'
            else:
                MAP_MATRIX[i][j] = '0'
        
    MAP_MATRIX[10][17] = 'T'
    MAP_MATRIX[15][25] = 'T'
    MAP_MATRIX[4][23] = 'T'
    MAP_MATRIX[9][33] = 'T'
    MAP_MATRIX[4][43] = 'T'
    MAP_MATRIX[15][46] = 'T'
    MAP_MATRIX[10][50] = 'T'
    MAP_MATRIX[4][60] = 'T'
    MAP_MATRIX[4][66] = 'T'
    MAP_MATRIX[11][62] = 'T'
    MAP_MATRIX[6][85] = 'T'
    MAP_MATRIX[11][113] = 'T'
    
    for i in range(6, 8):
        for j in range(9, 17):
            MAP_MATRIX[i][j] = 'P'
    for i in range(12, 14):
        for j in range(8, 23):
            MAP_MATRIX[i][j] = 'P'
    for i in range(6, 8):
        for j in range(22, 26):
            MAP_MATRIX[i][j] = 'P'
    for i in range(11, 17):
        for j in range(28, 38):
            MAP_MATRIX[i][j] = 'P'
    for i in range(6, 8):
        for j in range(40, 47):
            MAP_MATRIX[i][j] = 'P'
    for i in range(13, 17):
        for j in range(41, 45):
            MAP_MATRIX[i][j] = 'P'
    for i in range(12, 17):
        for j in range(48, 55):
            MAP_MATRIX[i][j] = 'P'
    for i in range(13, 15):
        for j in range(57, 69):
            MAP_MATRIX[i][j] = 'P'
    for i in range(6, 8):
        for j in range(58, 69):
            MAP_MATRIX[i][j] = 'P'
    for i in range(9, 13):
        for j in range(73, 79):
            MAP_MATRIX[i][j] = 'P'
    for i in range(13, 17):
        for j in range(73, 77):
            MAP_MATRIX[i][j] = 'P'
    for i in range(8, 12):
        for j in range(83, 89):
            MAP_MATRIX[i][j] = 'P'
    for i in range(11, 13):
        for j in range(92, 97):
            MAP_MATRIX[i][j] = 'P'
    for i in range(13, 17):
        for j in range(98, 119):
            MAP_MATRIX[i][j] = 'P'

    clock2 = pygame.time.get_ticks()
    #########################################################
    #--------------------Игровой процесс--------------------#
    #########################################################
    ticks=pygame.time.get_ticks() - clock2
    seconds=int(ticks/1000 % 60)
    minutes=int(ticks/60000 % 60)
    hours=int(ticks/3600000 % 24)
    if seconds < 10:
        seconds = '0' + str(seconds)
    if minutes < 10:
        minutes = '0' + str(minutes)
    if hours < 10:
        hours = '0' + str(hours)
    c_d = 0
    if CHOSEN_DIFFICULTY == 'medium':
        c_d = 1
    if CHOSEN_DIFFICULTY == 'hard':
        c_d = 2
    if CHOSEN_DIFFICULTY == 'insane':
        c_d = 3
    data[38 + c_d * 12 + 4] = str(hours) + '\n'
    data[39 + c_d * 12 + 4] = str(minutes) + '\n'
    data[40 + c_d * 12 + 4] = str(seconds) + '\n'
    info_copy = open('Resources/Other/info.txt', 'w')
    for i in data:
        info_copy.write(i)
    info_copy.close()

def level_03():
    global CHOSEN_DIFFICULTY
    DROP_CHANCE = 0
    ADDITIONAL_LIFES = 0
    BULLET_SPEED = 0
    CHARACTER_SPEED = 0
    if CHOSEN_DIFFICULTY == 'beginner':
        DROP_CHANCE = 100
        ADDITIONAL_LIFES = 3
        BULLET_SPEED = 6
    if CHOSEN_DIFFICULTY == 'medium':
        DROP_CHANCE = 70
        ADDITIONAL_LIFES = 2
        BULLET_SPEED = 7
    if CHOSEN_DIFFICULTY == 'hard':
        DROP_CHANCE = 35
        ADDITIONAL_LIFES = 1
        BULLET_SPEED = 8
    if CHOSEN_DIFFICULTY == 'insane':
        DROP_CHANCE = 0
        ADDITIONAL_LIFES = 0
        BULLET_SPEED = 10
    
    for i in range(18):
        for j in range(120):
            if i == 0 or i == 17 or j == 0 or j == 119:
                MAP_MATRIX[i][j] = 'P'
            else:
                MAP_MATRIX[i][j] = '0'
    
    MAP_MATRIX[7][9] = 'T'
    MAP_MATRIX[15][19] = 'T'
    MAP_MATRIX[7][20] = 'T'
    MAP_MATRIX[10][30] = 'T'
    MAP_MATRIX[15][42] = 'T'
    MAP_MATRIX[3][55] = 'T'
    MAP_MATRIX[9][55] = 'T'
    MAP_MATRIX[3][60] = 'T'
    MAP_MATRIX[9][60] = 'T'
    MAP_MATRIX[6][74] = 'T'
    MAP_MATRIX[4][87] = 'T'
    MAP_MATRIX[6][95] = 'T'
    MAP_MATRIX[12][100] = 'T'

    for i in range(9, 11):
        for j in range(8, 12):
            MAP_MATRIX[i][j] = 'P'
    for i in range(9, 11):
        for j in range(18, 22):
            MAP_MATRIX[i][j] = 'P'
    for i in range(14, 16):
        for j in range(10, 14):
            MAP_MATRIX[i][j] = 'P'
    for i in range(14, 16):
        for j in range(23, 27):
            MAP_MATRIX[i][j] = 'P'
    for i in range(12, 17):
        for j in range(28, 32):
            MAP_MATRIX[i][j] = 'P'
    for i in range(10, 17):
        for j in range(34, 39):
            MAP_MATRIX[i][j] = 'P'
    for i in range(11, 17):
        for j in range(45, 50):
            MAP_MATRIX[i][j] = 'P'
    for i in range(11, 13):
        for j in range(52, 62):
            MAP_MATRIX[i][j] = 'P'
    for i in range(5, 7):
        for j in range(52, 62):
            MAP_MATRIX[i][j] = 'P'
    for i in range(9, 11):
        for j in range(65, 69):
            MAP_MATRIX[i][j] = 'P'
    for i in range(8, 10):
        for j in range(71, 78):
            MAP_MATRIX[i][j] = 'P'
    for i in range(10, 17):
        for j in range(75, 78):
            MAP_MATRIX[i][j] = 'P'
    for i in range(6, 9):
        for j in range(83, 90):
            MAP_MATRIX[i][j] = 'P'
    for i in range(13, 17):
        for j in range(83, 89):
            MAP_MATRIX[i][j] = 'P'
    for i in range(8, 11):
        for j in range(93, 99):
            MAP_MATRIX[i][j] = 'P'
    for i in range(14, 16):
        for j in range(99, 102):
            MAP_MATRIX[i][j] = 'P'
    for i in range(11 , 17):
        for j in range(103, 119):
            MAP_MATRIX[i][j] = 'P'

    clock3 = pygame.time.get_ticks()
    #########################################################
    #--------------------Игровой процесс--------------------#
    #########################################################
    ticks=pygame.time.get_ticks() - clock3
    seconds=int(ticks/1000 % 60)
    minutes=int(ticks/60000 % 60)
    hours=int(ticks/3600000 % 24)
    if seconds < 10:
        seconds = '0' + str(seconds)
    if minutes < 10:
        minutes = '0' + str(minutes)
    if hours < 10:
        hours = '0' + str(hours)
    c_d = 0
    if CHOSEN_DIFFICULTY == 'medium':
        c_d = 1
    if CHOSEN_DIFFICULTY == 'hard':
        c_d = 2
    if CHOSEN_DIFFICULTY == 'insane':
        c_d = 3
    data[38 + c_d * 12 + 8] = str(hours) + '\n'
    data[39 + c_d * 12 + 8] = str(minutes) + '\n'
    data[40 + c_d * 12 + 8] = str(seconds) + '\n'
    info_copy = open('Resources/Other/info.txt', 'w')
    for i in data:
        info_copy.write(i)
    info_copy.close()

def options():
    global SOUNDS_VOLUME
    global SONG_VOLUME
    while True:
        options_mouse_pos = pygame.mouse.get_pos()

        SCREEN.fill("#121212")

        return_to_main_menu_O = Button(image = pygame.image.load("Resources/Textures/return_button_disabled.png"), image_path = "Resources/Textures/return_button_disabled.png", pos = (310, 900))

        return_to_main_menu_O.changeCondition(options_mouse_pos)
        return_to_main_menu_O.update(SCREEN)

        song_on_off_button = Button(image = pygame.image.load("Resources/Textures/music_en_dis_button_disabled.png"), image_path = "Resources/Textures/music_en_dis_button_disabled.png", pos = (530, 300))
        song_on_off_button.changeCondition(options_mouse_pos)
        song_on_off_button.update(SCREEN)
        
        sounds_on_off_button = Button(image = pygame.image.load("Resources/Textures/volume_en_dis_button_disabled.png"), image_path = "Resources/Textures/volume_en_dis_button_disabled.png", pos = (530, 600))
        sounds_on_off_button.changeCondition(options_mouse_pos)
        sounds_on_off_button.update(SCREEN)
        
        song_volume_buttons = []
        for i in range(10):
            song_vol_button_condition = ""
            if data[i + 16][:2] == "of":
                song_vol_button_condition = "off"
            else:
                song_vol_button_condition = "on"
            song_volume_button_path = "Resources/Textures/volume_button_" + song_vol_button_condition + "_disabled.png"
            song_volume_buttons.append(Button(image = pygame.image.load(song_volume_button_path), image_path = song_volume_button_path, pos = (800 + i * 70, 300)))
        for i in range(10):
            song_volume_buttons[i].changeCondition(options_mouse_pos)
            song_volume_buttons[i].update(SCREEN)

        sounds_volume_buttons = []
        for i in range(10):
            sounds_vol_button_condition = ""
            if data[i + 27][:2] == "of":
                sounds_vol_button_condition = "off"
            else:
                sounds_vol_button_condition = "on"
            sounds_volume_button_path = "Resources/Textures/volume_button_" + sounds_vol_button_condition + "_disabled.png"
            sounds_volume_buttons.append(Button(image = pygame.image.load(sounds_volume_button_path), image_path = sounds_volume_button_path, pos = (800 + i * 70, 600)))
        for i in range(10):
            sounds_volume_buttons[i].changeCondition(options_mouse_pos)
            sounds_volume_buttons[i].update(SCREEN)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if return_to_main_menu_O.checkForInput(options_mouse_pos):
                    button_click_sound.play()
                    button_click_sound.set_volume(SOUNDS_VOLUME / 100)
                    main_menu()
                if song_on_off_button.checkForInput(options_mouse_pos):
                    button_click_sound.play()
                    button_click_sound.set_volume(SOUNDS_VOLUME / 100)
                    if not SONG_VOLUME:
                        SONG_VOLUME = 10
                        data[16] = "on"
                    else:
                        SONG_VOLUME = 0
                        data[16] = "off"
                    for i in range(17, 26):
                        data[i] = "off"

                if sounds_on_off_button.checkForInput(options_mouse_pos):
                    button_click_sound.play()
                    button_click_sound.set_volume(SOUNDS_VOLUME / 100)
                    if not SOUNDS_VOLUME:
                        SOUNDS_VOLUME = 10
                        data[27] = "on"
                    else:
                        SOUNDS_VOLUME = 0
                        data[27] = "off"
                    for i in range(28, 37):
                        data[i] = "off"
                    
                for i in range(10):
                    if song_volume_buttons[i].checkForInput(options_mouse_pos):
                        SONG_VOLUME = i * 10 + 10
                        button_click_sound.play()
                        button_click_sound.set_volume(SOUNDS_VOLUME / 100)
                        for j in range(16, 17 + i):
                            data[j] = "on"
                        for j in range(17 + i, 26):
                            data[j] = "off"
                info_copy = open('Resources/Other/info.txt', 'w')
                for j in data:
                    w_str = j
                    if j in ["on", "off"]:
                        w_str += '\n'
                    info_copy.write(w_str)
                info_copy.close()
                background_theme.set_volume(SONG_VOLUME / 100)

                for i in range(10):
                    if sounds_volume_buttons[i].checkForInput(options_mouse_pos):
                        SOUNDS_VOLUME = i * 10 + 10
                        button_click_sound.play()
                        button_click_sound.set_volume(SOUNDS_VOLUME / 100)
                        for j in range(27, 28 + i):
                            data[j] = "on"
                        for j in range(28 + i, 37):
                            data[j] = "off"
                info_copy = open('Resources/Other/info.txt', 'w')
                for j in data:
                    w_str = j
                    if j in ["on", "off"]:
                        w_str += '\n'
                    info_copy.write(w_str)
                info_copy.close()

        pygame.display.update()


def main_menu():
    global SOUNDS_VOLUME
    global SONG_VOLUME
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
                    button_click_sound.play()
                    button_click_sound.set_volume(SOUNDS_VOLUME / 100)
                    play()
                if options_button.checkForInput(menu_mouse_pos):
                    button_click_sound.play()
                    button_click_sound.set_volume(SOUNDS_VOLUME / 100)
                    options()
                if quit_button.checkForInput(menu_mouse_pos):
                    button_click_sound.play()
                    button_click_sound.set_volume(SOUNDS_VOLUME / 100)
                    pygame.quit()
                    sys.exit()
        pygame.display.update()


main_menu()
