import pygame
import sys
from random import choice, randint

# settings
WIDTH = 840  # ширена экрана
HEIGHT = 640  # высота экрана
exit_in_menu_int = 0
FPS = 90
energy_eat = 30
teme_eat_update = 100 # прамежутки времени между поевлением еды
teme_eat_update_cash = 0
max_age = 800
energy_reproduction = 800  # энергия для диления
int_mutation = 5  # количество мутацый при дилении
start_papulation = 5
int_population = 0

# color
Brown = (165, 42, 42)
Silver = (192, 192, 192)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
DarkYellow = (120, 120, 0)
LiteDarkYellow = (230, 230, 0)
Gold = (255, 215, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
ForestGreen = (34, 139, 34)
DarkSlateGray = (47, 79, 79)
DimGray = (105, 105, 105)

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()

class Ant(pygame.sprite.Sprite):
    def __init__(self, x, y, glav_gen, start_energy):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.surface.Surface((20, 20))
        self.image.fill(LiteDarkYellow)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.gen = glav_gen
        self.gen_pos = 0  # позицыя выполняймого гена
        self.speed = 20
        self.energy_del = 0.5
        self.energy = start_energy
        self.energy_reproduction = energy_reproduction  # + (randint(-20, 20)) if energy_reproduction > 300 else energy_reproduction
        self.angle = 0  # угол зрения, 0-верх, 90-право,  180-вниз, 270-лево
        X_gen_cash = None
        self.max_age = max_age + (randint(-50, 50))
        self.age_cash = 0

    def update(self):
        self.gen_pos = 0 if self.gen_pos == len(self.gen) - 1 else self.gen_pos + 1

        X_gen_cash = self.gen[self.gen_pos]
        if X_gen_cash == "LEFT":
            self.angle = 270 if self.angle == 0 else self.angle - 90
        elif X_gen_cash == "RIGHT":
            self.angle = 0 if self.angle == 270 else self.angle + 90
        elif X_gen_cash == "GO":
            if self.angle == 0:
                self.rect.y -= self.speed
            elif self.angle == 270:
                self.rect.y += self.speed
            elif self.angle == 90:
                self.rect.x += self.speed
            else:
                self.rect.x -= self.speed

        elif X_gen_cash == "STOP":
            self.energy += self.energy_del//2

        # выход за экран
        if self.rect.right == 0:
            self.rect.left = WIDTH
        elif self.rect.left == WIDTH:
            self.rect.right = 0
        if self.rect.bottom == 0:
            self.rect.top = HEIGHT
        elif self.rect.top == HEIGHT:
            self.rect.bottom = 0

        # еда
        if pygame.sprite.groupcollide(All_sprites, sprites_eat_kaliz, False, True):
            self.energy += energy_eat

        self.proverk()

    def proverk(self):
        global int_population
        self.energy -= self.energy_del
        if self.energy <= 0:
            if int_population > 1:
                print("death")
                self.kill()
                int_population -= 1
            elif int_population == 1:
                self.repraduktion_p(2)
        elif self.energy >= self.energy_reproduction:
            self.repraduktion_p()
            self.energy -= (self.energy//2) + 50

        self.age_cash += 1
        if self.age_cash == self.max_age:
            if int_population > 1:
                print("death-age")
                self.kill()
                int_population -= 1
            elif int_population == 1:
                self.repraduktion_p(2)

    def repraduktion_p(self, x=1):
        global int_population, int_mutation
        if x == 1:
            print("reproduction")
            now_gen = self.gen
            int_mutation = randint(0, int_mutation)
            for i in range(int_mutation):
                now_gen[randint(0, 39)] = choice(("LEFT", "RIGHT", "GO", "STOP"))
            ant = Ant((self.rect.x - self.speed), (self.rect.y - self.speed), now_gen, (self.energy_reproduction // 2) - 20)
            All_sprites.add(ant)
            int_population += 1
            self.energy -= (self.energy // 2) + 50
        elif x == 2:  # режим создания новай папуляцыи
            print("dnhebvh11111")
            for i in range(start_papulation):
                now_gen = self.gen
                int_mutation = randint(0, int_mutation)
                for j in range(int_mutation*4):
                    now_gen[randint(0, 39)] = choice(("LEFT", "RIGHT", "GO", "STOP"))
                ant = Ant((20 * randint(0, 42)), (20 * randint(0, 32)), now_gen,
                          (self.energy_reproduction // 2) - 20)
                All_sprites.add(ant)
                int_population += 1
                self.energy -= (self.energy // 2) + 50

            print("death-end")
            self.kill()
            int_population -= 1



class Eat(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.surface.Surface((20, 20))
        self.image.fill(ForestGreen)
        self.rect = self.image.get_rect()
        self.rect.x = 20 * randint(0, 42)
        self.rect.y = 20 * randint(0, 32)


sprites_eat_kaliz = pygame.sprite.Group()  # спрайты еды для кализии
All_sprites = pygame.sprite.Group()  # спрайты всего

for i in range(start_papulation):
    ant = Ant((20 * randint(0, 42)), (20 * randint(0, 32)), [choice(("LEFT", "RIGHT", "GO", "STOP")) for i in range(40)],
              randint(80, 120))
    All_sprites.add(ant)
    int_population += 1

def eat_update():
    for i in range(40):
        eat = Eat()
        sprites_eat_kaliz.add(eat)

for i in range(10):
    eat_update()

def Main_window():
    global exit_in_menu_int, teme_eat_update, teme_eat_update_cash, int_population
    if exit_in_menu_int == 0:  # если игрок зашол в игру в первые за сэсию то это отмечяется
        exit_in_menu_int = 1
    running_main_win = True  # главный цикл
    # цикл главного экрана
    while running_main_win:
        clock.tick(FPS)
        pygame.display.set_caption(str(int_population))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:  # проверка на нажатие крестика для выхода
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_e:
                    eat_update()
                if event.key == pygame.K_i:
                    print(len(All_sprites))
                if event.key == pygame.K_y:
                    for i in range(2):
                        ant = Ant((20 * randint(0, 42)), (20 * randint(0, 32)),
                                  [choice(("LEFT", "RIGHT", "GO", "STOP")) for i in range(40)],
                                  randint(80, 120))
                        All_sprites.add(ant)
                        int_population += 1

        if teme_eat_update != teme_eat_update_cash:
            teme_eat_update_cash += 1
        else:
            teme_eat_update_cash = 0
            eat_update()
        # Обновление
        sprites_eat_kaliz.update()
        All_sprites.update()
        # Отрисовка
        screen.fill(BLACK)
        sprites_eat_kaliz.draw(screen)
        All_sprites.draw(screen)
        pygame.display.flip()

Main_window()
