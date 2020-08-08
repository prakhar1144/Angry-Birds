import pygame,sys, math

def projectile(angle):
    angle = math.radians(angle)
    global dt
    dt += 1/20

    h_velocity_o = velocity*math.cos(angle)
    v_velocity_o = (-velocity*math.sin(angle))

    x_displacement = (h_velocity_o*dt)
    y_displacement = (v_velocity_o*dt) + (0.5*gravity*(dt**2))

    Bird.rect.centerx = x + x_displacement

    Bird.rect.centery = y + y_displacement


def check_collision():
    for stone in stone_group.sprites():
        if pygame.sprite.collide_rect(Bird, stone):
            bird_destroyed.play()
            return False
    for enemy in enemy_group.sprites():
        if pygame.sprite.collide_rect(Bird, enemy):
            pig_destroyed.play()
            enemy.kill()
            return False

    if Bird.rect.centerx >= screen_width or Bird.rect.centerx <= 0:
        #brust figure
        bird_destroyed.play()
        return False
    if Bird.rect.centery >= screen_height - 120:
        bird_destroyed.play()
        return False

    return True

def restart():
    global  angle_input, Angle_setup, dt
    angle_input = 0
    Angle_setup = False
    dt = 0
    Bird.rect.center = (50, screen_height - 110)


def angle_representation():
    global Angle_setup, X_list, Y_list
    X_list, Y_list = [], []
    ddt = 0
    Angle = math.radians(angle_input)
    h_velocity_o = velocity*math.cos(Angle)
    print()
    v_velocity_o = (-velocity*math.sin(Angle))
    pygame.draw.line(screen, (0,0,0), (100, screen_height-160), (100 + 100*math.cos(Angle), screen_height-160-100*math.sin(Angle)))
    for p in range(70):
        ddt += 0.05
        x_Displacement = (h_velocity_o * ddt)
        y_Displacement = (v_velocity_o * ddt) + (0.5 * gravity * (ddt ** 2))
        X_list.append(x + x_Displacement)
        Y_list.append(y + y_Displacement)


class Stone(pygame.sprite.Sprite):
    def __init__(self, path, w, h, pos_x, pos_y):
        super().__init__()
        self.stone = pygame.image.load(path).convert_alpha()
        self.image = pygame.transform.scale(self.stone, (w, h))
        self.rect = self.image.get_rect()
        self.rect.center = (pos_x, pos_y)

class Enemy(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__()
        self.enemy = pygame.image.load('enemy.png').convert_alpha()
        self.image = pygame.transform.scale(self.enemy, (50, 50))
        self.rect = self.image.get_rect()
        self.rect.center = (pos_x, pos_y)

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.player = pygame.image.load('bird2.png').convert_alpha()
        self.image = pygame.transform.scale(self.player, (30, 30))
        self.rect = self.image.get_rect()
        self.rect.center = (50,screen_height-110)


pygame.mixer.pre_init(16000, -16, 2, 512)
pygame.init()
clock = pygame.time.Clock()
stage = "stage0"

dt = 0
gravity = 10
velocity = 100

Game_active = False
Angle_setup = False
angle_input = 0
X_list = []
Y_list = []

screen_width = 1240
screen_height = 697
screen = pygame.display.set_mode((screen_width,screen_height))
pygame.display.set_caption("Angry Birds")

background = pygame.image.load('background.jpg').convert()
background_scale = pygame.transform.scale(background,(1240,697))


Bird = Player()
Bird_group = pygame.sprite.Group()
Bird_group.add(Bird)
y = Bird.rect.y - 50
x = Bird.rect.x + 50

stone1 = Stone('stone.png', 55, 52, 760, screen_height - 120)
stone2 = Stone('stone2.png', 55, 218, 900, screen_height - 207)
stone3 = Stone('stone.png',55, 52, 1140, screen_height - 120)
stone_group = pygame.sprite.Group()
stone_group.add([stone1, stone2, stone3])


enemy1 = Enemy(850, screen_height-120)
enemy2 = Enemy(900, screen_height-339)
enemy3 = Enemy(1140, screen_height- 170)
enemy_group = pygame.sprite.Group()
enemy_group.add([enemy1, enemy2, enemy3])

sling_up = pygame.image.load('slingshot.png')
sling_scale_up = pygame.transform.scale(sling_up, (47, 81))
sling_rect_up = sling_scale_up.get_rect(center=(85, screen_height- 139))

flying = pygame.mixer.Sound('flying_sound.ogg')
bird_destroyed = pygame.mixer.Sound('bird-destroyed.ogg')
pig_destroyed = pygame.mixer.Sound('piglette-destroyed.ogg')
bg_music = pygame.mixer.Sound('bg_music.ogg')
bg_music.play(loops=-1)

Stage0 = pygame.image.load("stage0.jpg").convert()
Stage0_scaled = pygame.transform.scale(Stage0,(1240,697))
game_font = pygame.font.Font('angrybirds-regular.ttf',30)
angle_msg = game_font.render("Angle Control",True,(255,255,255))
power_msg = game_font.render("Shoot", True, (255, 255, 255))
info = game_font.render("Press any key to continue", True, (255, 255, 255))

key_1 = pygame.transform.scale(pygame.image.load('up.jpg'),(51,53))
key_2 = pygame.transform.scale(pygame.image.load('down.jpg'),(51,53))
key_3 = pygame.transform.scale(pygame.image.load('space.jpg'),(100,39))

while True:
    if stage == "stage0":
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                stage = "stage1"
        screen.blit(Stage0_scaled,(0,0))
        screen.blit(angle_msg,(100,512))
        screen.blit(power_msg, (1000, 512))
        screen.blit(info, (460, 597))
        screen.blit(key_1,(120,450))
        screen.blit(key_2, (193,450))
        screen.blit(key_3, (993, 450))
    elif stage == "stage1":
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    angle_input += 5
                    angle_representation()
                    Angle_setup = True
                if event.key == pygame.K_DOWN:
                    angle_representation()
                    Angle_setup = True
                    angle_input -= 1
                if event.key == pygame.K_SPACE:
                    Game_active = True
                    Angle_setup = False
                    flying.play()

        screen.blit(background_scale, (0, 0))

        screen.blit(sling_scale_up, sling_rect_up)

        Bird_group.draw(screen)
        stone_group.draw(screen)
        enemy_group.draw(screen)

        if Game_active:
            # rotated_player = rotate_player(player_scale)
            # screen.blit(rotated_player, player_rect)
            projectile(angle_input)
            Game_active = check_collision()
            if not Game_active:
                restart()
        if Angle_setup:
            # sling_shot stretch
            pygame.draw.circle(screen, (0, 0, 0), (int(X_list[0]),  int(Y_list[0])),2, 1)
            pygame.draw.circle(screen, (0, 0, 0), (int(X_list[5]),  int(Y_list[5])),2, 1)
            pygame.draw.circle(screen, (0, 0, 0), (int(X_list[10]), int(Y_list[10])),2, 1)
            pygame.draw.circle(screen, (0, 0, 0), (int(X_list[15]), int(Y_list[15])),2, 1)
            pygame.draw.circle(screen, (0, 0, 0), (int(X_list[21]), int(Y_list[21])),2, 1)
            pygame.draw.circle(screen, (0, 0, 0), (int(X_list[28]), int(Y_list[28])),2, 1)
            pygame.draw.circle(screen, (0, 0, 0), (int(X_list[36]), int(Y_list[36])),2, 1)
            pygame.draw.circle(screen, (0, 0, 0), (int(X_list[45]), int(Y_list[45])),2, 1)
            pygame.draw.circle(screen, (0, 0, 0), (int(X_list[55]), int(Y_list[55])),2, 1)
            pygame.draw.circle(screen, (0, 0, 0), (int(X_list[65]), int(Y_list[65])),2, 1)

    pygame.display.flip()
    clock.tick(100)