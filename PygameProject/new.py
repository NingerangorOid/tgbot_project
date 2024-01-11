import pygame
import os
import sys
import pygame.sprite

pygame.init()
clock = pygame.time.Clock()
size = width, height = 800, 800
screen = pygame.display.set_mode(size)
coordinats = [0, 0]
all_sprites = pygame.sprite.Group()
hero_sprites = pygame.sprite.Group()
doing = [0]

def load_image(pers, do, number, xsize, ysize, isleft=False, colorkey=None):
    fullname = os.path.join(f'data\{pers}\{do}', f'{str(number)}.png')
    # если файл не существует, то выходим
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()
    image = pygame.image.load(fullname)
    image1 = pygame.transform.scale(image, (xsize, ysize))
    if isleft:
        image2 = pygame.transform.flip(image1, 1, 0)
        return image2
    else:
        return image1

class AnimatedSprite(pygame.sprite.Sprite):
    def __init__(self, pers, x, y, do='стоит'):
        super().__init__(all_sprites)
        self.frames = []
        self.mirror_frames = []
        self.isleft = False
        self.x = x
        self.y = y
        self.coordinats = [0, 0]
        self.cut_sheet(pers, do)
        self.cur_frame = 0
        self.image = self.frames[self.cur_frame]
        self.framecount = 0


    def cut_sheet(self, pers, do):
        self.frames = [load_image(pers, do, i, 50, 70, self.isleft) for i in
                       range(1, len([name for name in os.listdir(f'data\{pers}\{do}')]) + 1)]
        self.mirror_frames = [load_image(pers, do, i, 50, 70, self.isleft) for i in
                              range(1, len([name for name in os.listdir(f'data\{pers}\{do}')]) + 1)]
        self.rect = pygame.Rect(self.x + self.coordinats[0], self.y + self.coordinats[1],
                                self.frames[0].get_width(), self.frames[0].get_height())

    def update(self):
        if self.framecount % 20 == 0:
            if not self.isleft:
                self.cur_frame = (self.cur_frame + 1) % len(self.frames)
                self.image = self.frames[self.cur_frame]

            else:
                self.cur_frame = (self.cur_frame + 1) % len(self.mirror_frames)
                self.image = self.mirror_frames[self.cur_frame]
        self.rect = pygame.Rect(self.x + self.coordinats[0], self.y + self.coordinats[1],
                                self.frames[0].get_width(), self.frames[0].get_height())
        self.framecount += 1


class Hero(AnimatedSprite):
    def __init__(self, pers, x, y, do='стоит'):
        super().__init__(pers, x, y)
        self.frames = []
        self.pers = pers
        self.x = x
        self.y = y
        self.mirror_frames = []
        self.isleft = False
        self.cut_sheet(self.pers, do)
        self.cur_frame = 0
        self.image = self.frames[self.cur_frame]
        self.rect = self.rect.move(x, y)
        self.framecount = 0
        self.coordinats = [0, 0]

class Boss(AnimatedSprite):
    def __init__(self, pers, x, y, do='стоит'):
        super().__init__(pers, x, y)
        self.frames = []
        self.pers = pers
        self.x = x
        self.do = do
        self.y = y
        self.mirror_frames = []
        self.isleft = False
        self.cut_sheet(self.pers, do)
        self.cur_frame = 0
        self.image = self.begin_frames[self.cur_frame]
        self.rect = self.rect.move(x, y)
        self.framecount = 0
        self.coordinats = [0, 0]

    def cut_sheet(self, pers, do):
        self.frames = [load_image(pers, do, i, 50, 70, self.isleft) for i in
                       range(1, len([name for name in os.listdir(f'data\{pers}\{do}')]) + 1)]
        self.mirror_frames = [load_image(pers, do, i, 50, 70, self.isleft) for i in
                              range(1, len([name for name in os.listdir(f'data\{pers}\{do}')]) + 1)]
        self.rect = pygame.Rect(self.x + self.coordinats[0], self.y + self.coordinats[1],
                                self.frames[0].get_width(), self.frames[0].get_height())
        if do == 'идёт':
            self.begin_frames = self.frames[:4]
            self.landing_frames = self.begin_frames[::-1]
            self.fly_frames = [*self.frames[4:], *self.frames[4::-1]]
            self.begin_frames_left = self.frames[:4]
            self.landing_frames_left = self.begin_frames_left[::-1]
            self.fly_frames_left = [*self.mirror_frames[4:], *self.mirror_frames[4::-1]]

    def update(self):
        if self.framecount % 20 == 0:
            if not self.isleft:
                if self.do == 'идёт':
                    if self.cur_frame < 4:
                        self.image = self.begin_frames[self.cur_frame]
                    else:
                        self.cur_frame = 0
                        self.image = self.fly_frames[self.cur_frame]
                if self.cur_frame < 4:
                    self.image = self.begin_frames[self.cur_frame]
            else:
                if self.do == 'идёт':
                    if self.cur_frame < 4:
                        self.image = self.begin_frames_left[self.cur_frame]
                    else:
                        self.cur_frame = 0
                        self.image = self.fly_frames_left[self.cur_frame]
        self.rect = pygame.Rect(self.x + self.coordinats[0], self.y + self.coordinats[1],
                                self.frames[0].get_width(), self.frames[0].get_height())
        self.framecount += 1

class Enemy(AnimatedSprite):
    pass

fps = 100
running = True
asd = Hero('мечник', 50, 10)
hero_sprites.add(asd)
all_sprites.add(hero_sprites)

while running:

    screen.fill((0,0,0))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT or event.key == pygame.K_a:
                asd.x -= 10
                asd.isleft = True
                doing[0] = 1
                asd.cut_sheet(asd.pers, 'идёт')
            if event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                asd.x += 100
                asd.isleft = False
                doing[0] = 1
                asd.cut_sheet(asd.pers, 'идёт')
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_a:
                asd.x += 10
                asd.cut_sheet(asd.pers, 'стоит')
                doing[0] = 0
            if event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                asd.x -= 100
                asd.cut_sheet(asd.pers, 'стоит')
                doing[0] = 0
        if doing[0] == 0:
            asd.cut_sheet(asd.pers, 'стоит')
        elif doing[0] == 1:
            asd.cut_sheet(asd.pers, 'идёт')
    all_sprites.draw(screen)
    all_sprites.update()
    pygame.display.flip()
    clock.tick(fps)
    print(asd.coordinats)
pygame.quit()