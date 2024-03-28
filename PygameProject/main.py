import pygame
import os
import sys
from mapFile import level1, Border, Platform, level2, level3
import random
from DieWin_qt import lose, win
all_sprites = pygame.sprite.Group()
enemy_sprites = pygame.sprite.Group()
new_to_do = 'стоит'
MOVE_SPEED_enemy = 1
MOVE_SPEED = 5
coordinats_enemy = []
JUMP = 10
GRAVITY = 0.35
bgs = ['data/фон/forest.jpg', 'data/фон/desert.jpg', 'data/фон/nest.jpg']

def drawMap():
    x = y = 0

    for row in level:
        for col in row:
            if col != 0:
                pf = Platform(x, y, 40 * abs(col), col)
                all_sprites.add(pf)
                platforms.append(pf)
            x += 40
        y += 24
        x = 0
    sizes = [(-1, 0, 1, 768), (1280, -1, 1, 768), (0, -1, 1280, 1)]
    for ll in sizes:
        br = Border(ll[0], ll[1], ll[2], ll[3])
        all_sprites.add(br)
        platforms.append(br)

def load_image(pers, do, number, xsize, ysize, isleft=False, colorkey=None):
    fullname = os.path.join(f'data\{pers}\{do}', f'{str(number)}.png')

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

class Archer(pygame.sprite.Sprite):
    def __init__(self, x, y, pers='лучник', do='стоит'):
        super().__init__(all_sprites)
        self.yvel = 0
        self.onGround = False
        self.xvel = 0
        self.hp = 120
        self.damage = 20
        self.startX = x
        self.startY = y
        self.cur_frame = 0
        self.pers = pers
        self.x = x
        self.do = do
        self.y = y
        self.frames = []
        self.mirror_frames = []
        self.isleft = False
        self.cut_sheet(self.pers, do)
        self.framecount = 0
        self.blockcount = 0

    def cut_sheet(self, pers, do):
        self.frames = [load_image(pers, do, i, 50, 70, False) for i in
                       range(1, len([name for name in os.listdir(f'data\{pers}\{do}')]) + 1)]
        self.mirror_frames = [load_image(pers, do, i, 50, 70, True) for i in
                              range(1, len([name for name in os.listdir(f'data\{pers}\{do}')]) + 1)]
        self.rect = pygame.Rect(self.x, self.y, self.frames[0].get_width(), self.frames[0].get_height())
        if not self.isleft:
            self.cur_frame = 0
            self.image = self.frames[self.cur_frame]
        else:
            self.cur_frame = 0
            self.image = self.mirror_frames[self.cur_frame]

    def update(self, left, right, up, platforms, new_do):
        global new_to_do
        if self.do != new_do:
            self.do = new_do
            self.cut_sheet(self.pers, new_do)
        if left:
            self.xvel = -MOVE_SPEED
            self.isleft = True
        if right:
            self.xvel = MOVE_SPEED
            self.isleft = False
        if not (left or right) or self.do in ['стоит', 'бьёт']:
            self.xvel = 0
        if up:
            if self.onGround:
                self.yvel = -JUMP
        if not self.onGround:
            self.yvel += GRAVITY
        self.onGround = False
        self.rect.y += self.yvel
        self.collide(0, self.yvel, platforms)
        self.rect.x += self.xvel
        self.collide(self.xvel, 0, platforms)
        if self.framecount % 9 == 0:
            if not self.isleft:
                if self.do == 'тыкает':
                    if self.blockcount < 4:
                        self.image = self.frames[self.cur_frame]
                        self.cur_frame = (self.cur_frame + 1) % len(self.frames)
                        self.blockcount += 1
                    if self.blockcount == 4:
                        self.blockcount = 0
                        new_to_do = 'нетыкает'
                elif self.do == 'нетыкает':
                    if self.blockcount <= 4:
                        self.image = self.frames[self.cur_frame]
                        self.cur_frame = (self.cur_frame + 1) % len(self.frames)
                        self.blockcount += 1
                    if self.blockcount == 5:
                        self.blockcount = 0
                        new_to_do = 'стоит'
                elif self.do == 'смерть':
                    if self.blockcount <= 6:
                        self.image = self.frames[self.cur_frame]
                        self.cur_frame = (self.cur_frame + 1) % len(self.frames)
                        self.blockcount += 1
                        self.xvel = 0
                    if self.blockcount == 6:
                        self.blockcount = 0
                        self.rect = pygame.Rect(0, 0, 0, 0)
                        self.kill()
                        lose()
                elif self.do == 'урон':
                    if self.blockcount <= 4:
                        self.image = self.frames[self.cur_frame]
                        self.cur_frame = (self.cur_frame + 1) % len(self.frames)
                        self.blockcount += 1
                    if self.blockcount == 4:
                        self.blockcount = 0
                        new_to_do = 'стоит'
                elif self.do == 'бьёт':
                    if self.blockcount <= 10:
                        self.image = self.frames[self.cur_frame]
                        self.cur_frame = (self.cur_frame + 1) % len(self.frames)
                        self.blockcount += 1
                    if self.blockcount == 8:
                        arrow_sprites.add(Arrow(self.rect.centerx + 10, self.rect.centery - 10, False, 'лучник'))
                    if self.blockcount == 10:
                        self.blockcount = 0
                        new_to_do = 'стоит'
                else:
                    self.blockcount = 0
                    self.image = self.frames[self.cur_frame]
                    self.cur_frame = (self.cur_frame + 1) % len(self.frames)
            else:
                if self.do == 'тыкает':
                    if self.blockcount < 4:
                        self.image = self.mirror_frames[self.cur_frame]
                        self.cur_frame = (self.cur_frame + 1) % len(self.frames)
                        self.blockcount += 1
                    if self.blockcount == 4:
                        self.blockcount = 0
                        new_to_do = 'нетыкает'
                elif self.do == 'нетыкает':
                    if self.blockcount <= 4:
                        self.image = self.mirror_frames[self.cur_frame]
                        self.cur_frame = (self.cur_frame + 1) % len(self.frames)
                        self.blockcount += 1
                    if self.blockcount == 5:
                        self.blockcount = 0
                        new_to_do = 'стоит'
                elif self.do == 'урон':
                    if self.blockcount <= 4:
                        self.image = self.mirror_frames[self.cur_frame]
                        self.cur_frame = (self.cur_frame + 1) % len(self.frames)
                        self.blockcount += 1
                    if self.blockcount == 4:
                        self.blockcount = 0
                        new_to_do = 'стоит'
                elif self.do == 'смерть':
                    if self.blockcount <= 9:
                        self.image = self.mirror_frames[self.cur_frame]
                        self.cur_frame = (self.cur_frame + 1) % len(self.frames)
                        self.blockcount += 1
                        self.xvel = 0
                    if self.blockcount == 9:
                        self.blockcount = 0
                        self.rect = pygame.Rect(0, 0, 0, 0)
                        self.kill()
                        lose()
                elif self.do == 'бьёт':
                    if self.blockcount <= 10:
                        self.image = self.mirror_frames[self.cur_frame]
                        self.cur_frame = (self.cur_frame + 1) % len(self.frames)
                        self.blockcount += 1
                    if self.blockcount == 8:
                        arrow_sprites.add(Arrow(self.rect.centerx - 20, self.rect.centery - 10, True, 'лучник'))
                    if self.blockcount == 10:
                        self.blockcount = 0
                        new_to_do = 'стоит'
                else:
                    self.blockcount = 0
                    self.image = self.mirror_frames[self.cur_frame]
                    self.cur_frame = (self.cur_frame + 1) % len(self.frames)
        self.x = self.rect.x
        self.y = self.rect.y
        self.framecount += 1

    def collide(self, xvel, yvel, platforms):
        global new_to_do, highscore
        for p in platforms:
            if pygame.sprite.collide_rect(self, p):
                if xvel > 0:
                    self.rect.right = p.rect.left
                if xvel < 0:
                    self.rect.left = p.rect.right
                if yvel > 0:
                    self.rect.bottom = p.rect.top
                    self.onGround = True
                    self.yvel = 0
                if yvel < 0:
                    self.rect.top = p.rect.bottom
                    self.yvel = 0
        for e in enemies:
            if pygame.sprite.collide_rect(self, e):
                if self.do == 'тыкает':
                    e.hp -= self.damage
                    e.enemy_to_do = 'урон'
                    e.xvel = 0
                    e.a += 1
                elif e.do == 'бьёт':
                    if self.do not in ['урон', 'бьёт', 'тыкает']:
                        self.hp -= e.damage
                        new_to_do = 'урон'
                        self.xvel = 0
                if e.hp <= 0:
                    e.enemy_to_do = 'смерть'
                    highscore += 100
            if self.hp <= 0:
                new_to_do = 'смерть'


class Mage(pygame.sprite.Sprite):
    def __init__(self, x, y, pers='маг', do='стоит'):
        super().__init__(all_sprites)
        self.yvel = 0
        self.onGround = False
        self.xvel = 0
        self.startX = x
        self.hp = 90
        self.damage = 40
        self.startY = y
        self.cur_frame = 0
        self.pers = pers
        self.x = x
        self.do = do
        self.y = y
        self.frames = []
        self.mirror_frames = []
        self.isleft = False
        self.cut_sheet(self.pers, do)
        self.framecount = 0
        self.blockcount = 0

    def cut_sheet(self, pers, do):
        self.frames = [load_image(pers, do, i, 50, 70, False) for i in
                       range(1, len([name for name in os.listdir(f'data\{pers}\{do}')]) + 1)]
        self.mirror_frames = [load_image(pers, do, i, 50, 70, True) for i in
                              range(1, len([name for name in os.listdir(f'data\{pers}\{do}')]) + 1)]
        self.rect = pygame.Rect(self.x, self.y, self.frames[0].get_width(), self.frames[0].get_height())
        if not self.isleft:
            self.cur_frame = 0
            self.image = self.frames[self.cur_frame]
        else:
            self.cur_frame = 0
            self.image = self.mirror_frames[self.cur_frame]

    def update(self, left, right, up, platforms, new_do):
        global new_to_do
        if self.do != new_do:
            self.do = new_do
            self.cut_sheet(self.pers, new_do)
        if left:
            self.xvel = -MOVE_SPEED
            self.isleft = True
        if right:
            self.xvel = MOVE_SPEED
            self.isleft = False
        if not (left or right) or self.do in ['стоит', 'бьёт']:
            self.xvel = 0
        if up:
            if self.onGround:
                self.yvel = -JUMP
        if not self.onGround:
            self.yvel += GRAVITY
        self.onGround = False
        self.rect.y += self.yvel
        self.collide(0, self.yvel, platforms)
        self.rect.x += self.xvel
        self.collide(self.xvel, 0, platforms)
        if self.framecount % 10 == 0:
            if not self.isleft:
                if self.do == 'бьёт':
                    if self.blockcount <= 5:
                        self.image = self.frames[self.cur_frame]
                        self.cur_frame = (self.cur_frame + 1) % len(self.frames)
                        self.blockcount += 1

                    if self.blockcount == 5:
                        self.blockcount = 0
                        arrow_sprites.add(Arrow(self.rect.centerx + 10, self.rect.centery - 10, False, 'маг'))
                        new_to_do = 'стоит'
                elif self.do == 'урон':

                    if self.blockcount <= 4:
                        self.image = self.frames[self.cur_frame]
                        self.cur_frame = (self.cur_frame + 1) % len(self.frames)
                        self.blockcount += 1

                    if self.blockcount == 4:
                        self.blockcount = 0
                        new_to_do = 'стоит'
                elif self.do == 'смерть':

                    if self.blockcount <= 9:
                        self.image = self.frames[self.cur_frame]
                        self.cur_frame = (self.cur_frame + 1) % len(self.frames)
                        self.blockcount += 1
                        self.xvel = 0

                    if self.blockcount == 9:
                        self.blockcount = 0
                        self.rect = pygame.Rect(0, 0, 0, 0)
                        self.kill()
                        lose()
                else:
                    self.blockcount = 0

                    self.image = self.frames[self.cur_frame]
                    self.cur_frame = (self.cur_frame + 1) % len(self.frames)
            else:
                if self.do == 'бьёт':

                    if self.blockcount <= 5:
                        self.image = self.mirror_frames[self.cur_frame]
                        self.cur_frame = (self.cur_frame + 1) % len(self.frames)
                        self.blockcount += 1

                    if self.blockcount == 5:
                        self.blockcount = 0
                        arrow_sprites.add(Arrow(self.rect.centerx - 20, self.rect.centery - 10, True, 'маг'))
                        new_to_do = 'стоит'

                elif self.do == 'урон':

                    if self.blockcount <= 4:
                        self.image = self.mirror_frames[self.cur_frame]
                        self.cur_frame = (self.cur_frame + 1) % len(self.frames)
                        self.blockcount += 1

                    if self.blockcount == 4:
                        self.blockcount = 0
                        new_to_do = 'стоит'
                elif self.do == 'смерть':

                    if self.blockcount <= 9:
                        self.image = self.mirror_frames[self.cur_frame]
                        self.cur_frame = (self.cur_frame + 1) % len(self.frames)
                        self.blockcount += 1
                        self.xvel = 0

                    if self.blockcount == 9:
                        self.blockcount = 0
                        self.rect = pygame.Rect(0, 0, 0, 0)
                        self.kill()
                        lose()
                else:
                    self.blockcount = 0
                    self.image = self.mirror_frames[self.cur_frame]
                    self.cur_frame = (self.cur_frame + 1) % len(self.frames)
        self.x = self.rect.x
        self.y = self.rect.y
        self.framecount += 1

    def collide(self, xvel, yvel, platforms):
        global new_to_do, highscore
        for p in platforms:
            if pygame.sprite.collide_rect(self, p):
                if xvel > 0:
                    self.rect.right = p.rect.left
                if xvel < 0:
                    self.rect.left = p.rect.right
                if yvel > 0:
                    self.rect.bottom = p.rect.top
                    self.onGround = True
                    self.yvel = 0
                if yvel < 0:
                    self.rect.top = p.rect.bottom
                    self.yvel = 0
        for e in enemies:
            if pygame.sprite.collide_rect(self, e):
                if e.do == 'бьёт':
                    if self.do not in ['урон', 'бьёт']:
                        self.hp -= e.damage
                        new_to_do = 'урон'
                        self.xvel = 0
                if e.hp <= 0:
                    e.enemy_to_do = 'смерть'
                    highscore += 100
            if self.hp <= 0:
                new_to_do = 'смерть'



class Swordman(pygame.sprite.Sprite):
    def __init__(self, x, y, pers='мечник', do='стоит'):
        super().__init__(all_sprites)
        self.yvel = 0
        self.onGround = False
        self.xvel = 0
        self.hp = 150
        self.damage = 30
        self.startX = x
        self.startY = y
        self.cur_frame = 0
        self.pers = pers
        self.x = x
        self.do = do
        self.y = y
        self.frames = []
        self.mirror_frames = []
        self.isleft = False
        self.cut_sheet(self.pers, do)
        self.framecount = 0
        self.blockcount = 0

    def cut_sheet(self, pers, do):
        self.frames = [load_image(pers, do, i, 50, 70, False) for i in
                       range(1, len([name for name in os.listdir(f'data/{pers}/{do}')]) + 1)]
        self.mirror_frames = [load_image(pers, do, i, 50, 70, True) for i in
                              range(1, len([name for name in os.listdir(f'data\{pers}\{do}')]) + 1)]
        self.rect = pygame.Rect(self.x, self.y, self.frames[0].get_width(), self.frames[0].get_height())

        if not self.isleft:
            self.cur_frame = 0
            self.image = self.frames[self.cur_frame]
        else:
            self.cur_frame = 0
            self.image = self.mirror_frames[self.cur_frame]

    def update(self, left, right, up, platforms, new_do):
        global new_to_do



        if self.do != new_do:
            self.do = new_do
            self.cut_sheet(self.pers, new_do)
        if left:
            self.xvel = -MOVE_SPEED
            self.isleft = True
        if right:
            self.xvel = MOVE_SPEED
            self.isleft = False
        if not (left or right) or self.do in ['стоит', 'бьёт']:
            self.xvel = 0
        if up:
            if self.onGround:
                self.yvel = -JUMP

        if not self.onGround:
            self.yvel += GRAVITY

        self.onGround = False
        self.rect.y += self.yvel
        self.collide(0, self.yvel, platforms, enemies)

        self.rect.x += self.xvel
        self.collide(self.xvel, 0, platforms, enemies)

        if self.framecount % 10 == 0:
            if not self.isleft:
                if self.do == 'блок':

                    if self.blockcount < 4:
                        self.image = self.frames[self.cur_frame]
                        self.cur_frame = (self.cur_frame + 1) % len(self.frames)
                        self.blockcount += 1
                    if self.blockcount >= 4:
                        self.cur_frame = self.cur_frame
                elif self.do == 'разблок':
                    if self.blockcount < 4:
                        self.image = self.frames[self.cur_frame]
                        self.cur_frame = (self.cur_frame + 1) % len(self.frames)
                        self.blockcount += 1
                    if self.blockcount == 4:
                        self.blockcount = 0
                        new_to_do = 'стоит'

                elif self.do == 'бьёт':

                    if self.blockcount <= 7:
                        self.image = self.frames[self.cur_frame]
                        self.cur_frame = (self.cur_frame + 1) % len(self.frames)
                        self.blockcount += 1

                    if self.blockcount == 7:
                        self.blockcount = 0
                        new_to_do = 'стоит'
                elif self.do == 'урон':

                    if self.blockcount <= 7:
                        self.image = self.frames[self.cur_frame]
                        self.cur_frame = (self.cur_frame + 1) % len(self.frames)
                        self.blockcount += 1

                    if self.blockcount == 7:
                        self.blockcount = 0
                        new_to_do = 'стоит'
                elif self.do == 'смерть':

                    if self.blockcount <= 7:
                        self.image = self.frames[self.cur_frame]
                        self.cur_frame = (self.cur_frame + 1) % len(self.frames)
                        self.blockcount += 1
                        self.xvel = 0

                    if self.blockcount == 7:
                        self.blockcount = 0
                        self.rect = pygame.Rect(0, 0, 0, 0)
                        self.kill()
                        lose()
                else:
                    self.blockcount = 0

                    self.image = self.frames[self.cur_frame]
                    self.cur_frame = (self.cur_frame + 1) % len(self.frames)
            else:
                if self.do == 'блок':
                    if self.blockcount < 4:
                        self.image = self.mirror_frames[self.cur_frame]
                        self.cur_frame = (self.cur_frame + 1) % len(self.frames)
                        self.blockcount += 1
                    if self.blockcount >= 4:
                        self.cur_frame = self.cur_frame

                elif self.do == 'разблок':
                    if self.blockcount < 4:
                        self.image = self.mirror_frames[self.cur_frame]
                        self.cur_frame = (self.cur_frame + 1) % len(self.frames)
                        self.blockcount += 1

                    if self.blockcount == 4:
                        self.blockcount = 0

                        new_to_do = 'стоит'
                elif self.do == 'смерть':

                    if self.blockcount <= 7:
                        self.image = self.mirror_frames[self.cur_frame]
                        self.cur_frame = (self.cur_frame + 1) % len(self.frames)
                        self.blockcount += 1
                        self.xvel = 0

                    if self.blockcount == 7:
                        self.blockcount = 0
                        self.rect = pygame.Rect(0, 0, 0, 0)
                        self.kill()
                        lose()

                elif self.do == 'бьёт':

                    if self.blockcount <= 7:
                        self.image = self.mirror_frames[self.cur_frame]
                        self.cur_frame = (self.cur_frame + 1) % len(self.frames)
                        self.blockcount += 1

                    if self.blockcount == 7:
                        self.blockcount = 0
                        new_to_do = 'стоит'
                elif self.do == 'урон':

                    if self.blockcount <= 7:
                        self.image = self.mirror_frames[self.cur_frame]
                        self.cur_frame = (self.cur_frame + 1) % len(self.frames)
                        self.blockcount += 1

                    if self.blockcount == 7:
                        self.blockcount = 0
                        new_to_do = 'стоит'
                else:
                    self.blockcount = 0
                    self.image = self.mirror_frames[self.cur_frame]
                    self.cur_frame = (self.cur_frame + 1) % len(self.frames)
        self.x = self.rect.x
        self.y = self.rect.y
        self.framecount += 1

    def collide(self, xvel, yvel, platforms, enemies):
        global new_to_do, highscore
        for p in platforms:
            if pygame.sprite.collide_rect(self, p):
                if xvel > 0:
                    self.rect.right = p.rect.left
                if xvel < 0:
                    self.rect.left = p.rect.right
                if yvel > 0:
                    self.rect.bottom = p.rect.top
                    self.onGround = True
                    self.yvel = 0
                if yvel < 0:
                    self.rect.top = p.rect.bottom
                    self.yvel = 0
        for e in enemies:
            if pygame.sprite.collide_rect(self, e):
                if self.do == 'бьёт':
                    e.hp -= self.damage
                    e.enemy_to_do = 'урон'
                    e.xvel = 0
                    e.a += 1
                elif self.do == 'блок':
                    e.a += 1
                elif self.do == 'разблок':
                    e.a -= 1
                elif e.do == 'бьёт':
                    if self.do not in ['урон', 'бьёт']:
                        self.hp -= e.damage
                        new_to_do = 'урон'
                        self.xvel = 0
                if e.hp <= 0:
                    e.enemy_to_do = 'смерть'
                    highscore += 100
        if self.hp <= 0:
            new_to_do = 'смерть'




class Arrow(pygame.sprite.Sprite):
    def __init__(self, x, y, isleft, pers):
        super().__init__(arrow_sprites)
        self.x = x
        self.y = y
        if pers == 'лучник':
            self.image = pygame.image.load('data/лучник/стрела.png')
            self.damage = 30
        else:
            self.image = pygame.image.load('data/маг/шар.png')
            self.damage = 40
        self.rect = pygame.Rect(x, y, 22, 12)
        if isleft:
            self.xvel = -4
            self.image = pygame.transform.flip(self.image, 1, 0)
        else:
            self.xvel = 4

    def collide(self, xvel, platforms, enemies):
        global highscore
        for p in platforms:
            if pygame.sprite.collide_rect(self, p):
                arrow_sprites.remove(self)
        for e in enemies:
            if pygame.sprite.collide_rect(self, e):
                self.kill()
                e.hp -= self.damage
                e.enemy_to_do = 'урон'
                e.xvel = 0
            if e.hp <= 0:
                e.enemy_to_do = 'смерть'
                highscore += 100

    def update(self):
        self.rect.x += self.xvel
        self.collide(0, platforms, enemies)


class Portal(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__(portal_sprites)
        self.x = x
        self.y = y
        self.cur_frame = 0
        self.framecount = 0
        self.enabled = True

        self.rect = pygame.Rect(x, y, 52, 74)
        self.frames = [load_image('портал', '', i, 50, 70, False) for i in
                       range(1, len([name for name in os.listdir(f'data\портал')]) + 1)]
        self.image = self.frames[self.cur_frame]

    def collide(self, hero):
        if self.enabled:
            if pygame.sprite.collide_rect(self, hero):
                coords = [portal_sprites.sprites()[0].x, portal_sprites.sprites()[0].y]
                hero.x, hero.y = coords
                hero.cut_sheet(hero.pers, 'стоит')
                self.enabled = False

    def update(self):
        global hero, a
        if self.framecount % 7 == 0:
            self.image = self.frames[self.cur_frame]
            self.cur_frame = (self.cur_frame + 1) % len(self.frames)
        self.framecount += 1
        self.collide(hero)
        if not self.enabled:
            portal_sprites.remove(self)
            a = 9


class Final_Portal(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__(portal_sprites)
        self.x = x
        self.y = y
        self.cur_frame = 0
        self.framecount = 0
        self.rect = pygame.Rect(x, y, 52, 74)
        self.frames = [load_image('портал', '', i, 50, 70, False) for i in
                       range(1, len([name for name in os.listdir(f'data\портал')]) + 1)]
        self.image = self.frames[self.cur_frame]

    def collide(self, hero):
        global level, a, levels, spawn_coords, platforms, portal1, portal2, bgs, bgImg, is_portal

        if pygame.sprite.collide_rect(self, hero):
            spawn_coords.pop(0)
            coords = [*spawn_coords[0]]
            hero.x, hero.y = coords
            levels.pop(0)
            for i in platforms:
                i.kill()
            platforms = []

            hero.cut_sheet(hero.pers, 'стоит')
            level = levels[0]
            drawMap()
            is_portal = False
            bgs.pop(0)
            bgImg = pygame.image.load(bgs[0])

            screen.blit(bgImg, (0, 0))
            for i in portal_sprites:
                i.kill()
            a = 9
            if level == level2:
                portal2 = Portal(650, 216)
                portal1 = Portal(1000, 677)
                for i in enemy_sprites:
                    i.kill()
                coordinats_enemy = [[135, 121], [410, 109]]
                for i in range(2):
                    enemy_display = Enemy('зомби', coordinats_enemy[i][0], coordinats_enemy[i][1])
                    enemies.append(enemy_display)
                    enemy_sprites.add(enemy_display)
            if level == level3:
                for i in enemy_sprites:
                    i.kill()
                enemy_display = Boss(510, 386)
                enemies.append(enemy_display)
                enemy_sprites.add(enemy_display)


    def update(self):
        global hero, a
        if self.framecount % 7 == 0:
            self.image = self.frames[self.cur_frame]
            self.cur_frame = (self.cur_frame + 1) % len(self.frames)
        self.framecount += 1
        self.collide(hero)


class Enemy(pygame.sprite.Sprite):
    def __init__(self, pers, x, y, do='стоит'):
        super().__init__(enemy_sprites)
        self.enemy_to_do = 'стоит'
        self.frames = []
        self.cur_frame = 0
        self.hp = 120
        self.damage = 30
        self.pers = pers
        self.x = x
        self.do = do
        self.y = y
        self.mirror_frames = []
        self.isleft = False
        self.xvel = 0
        self.cut_sheet(self.pers, do)
        self.rect = self.rect.move(x, y)
        self.framecount = 0
        self.blockcount = 0
        self.a = 0
        self.start_x = x

    def cut_sheet(self, pers, do):
        self.frames = [load_image(pers, do, i, 50, 70, False) for i in
                       range(1, len([name for name in os.listdir(f'data\{pers}\{do}')]) + 1)]
        self.mirror_frames = [load_image(pers, do, i, 50, 70, True) for i in
                              range(1, len([name for name in os.listdir(f'data\{pers}\{do}')]) + 1)]
        self.rect = pygame.Rect(self.x, self.y, self.frames[0].get_width(), self.frames[0].get_height())
        if not self.isleft:
            self.cur_frame = 0
            self.image = self.frames[self.cur_frame]
        else:
            self.cur_frame = 0
            self.image = self.mirror_frames[self.cur_frame]

    def wait(self):
        self.enemy_to_do = "стоит"
        self.xvel = 0

    def the_pursuit(self):

        if self.do != 'урон' and self.do != 'смерть':

            if hero.rect.x - self.x > 10:
                self.xvel = MOVE_SPEED_enemy
                self.isleft = False
                self.enemy_to_do = 'идёт'
            elif hero.rect.x - self.x < 10:
                self.xvel = -MOVE_SPEED_enemy
                self.isleft = True
                self.enemy_to_do = 'идёт'
            else:
                self.wait()

    def random_life(self):
        if self.framecount % 100 == 0 and self.do != 'урон' and self.do != 'смерть':
            stop_or_go = random.randint(0, 1)
            if stop_or_go:
                left_or_right = random.randint(0, 1)
                rasst_from_start = self.x / 2 - self.start_x
                if rasst_from_start >= 15:
                    left_or_right = 0
                if rasst_from_start <= -15:
                    left_or_right = 1
                if left_or_right == 0:
                    self.xvel = -MOVE_SPEED_enemy
                    self.isleft = True
                    self.enemy_to_do = "идёт"
                elif left_or_right == 1:
                    self.xvel = MOVE_SPEED_enemy
                    self.isleft = False
                    self.enemy_to_do = "идёт"
            else:
                self.wait()

    def update(self):

        if self.do != self.enemy_to_do:
            self.do = self.enemy_to_do
            self.cut_sheet(self.pers, self.enemy_to_do)

        self.rect.x += self.xvel
        self.x = self.rect.x
        self.y = self.rect.y
        if hero.y == self.y:
            if 40 < abs(hero.rect.x - self.x) < 250:
                self.the_pursuit()
            elif abs(hero.rect.x - self.x) > 300:
                self.random_life()
            else:
                if self.a:
                    self.a -= 1
                    self.wait()
                else:
                    if abs(hero.rect.x - self.x) < 40:
                        self.enemy_to_do = 'бьёт'
                        self.xvel = 0
                    else:
                        self.the_pursuit()
        else:
            if self.a > 0:
                self.a -= 1
                self.wait()
            else:
                self.random_life()
        if self.framecount % 10 == 0:
            if not self.isleft:
                if self.do == 'урон':
                    if self.blockcount < 7:
                        self.xvel = 0
                        self.image = self.frames[self.cur_frame]
                        self.cur_frame = (self.cur_frame + 1) % len(self.frames)
                        self.blockcount += 1
                    if self.blockcount == 7:
                        self.blockcount = 0
                        self.enemy_to_do = 'стоит'
                elif self.do == 'смерть':

                    if self.blockcount <= 6:
                        self.image = self.frames[self.cur_frame]
                        self.cur_frame = (self.cur_frame + 1) % len(self.frames)
                        self.blockcount += 1

                    if self.blockcount == 6:
                        self.blockcount = 0
                        self.rect = pygame.Rect(0, 0, 0, 0)
                        self.kill()
                else:
                    self.image = self.frames[self.cur_frame]
                    self.cur_frame = (self.cur_frame + 1) % len(self.frames)
            else:
                if self.do == 'урон':
                    if self.blockcount < 7:
                        self.xvel = 0
                        self.image = self.mirror_frames[self.cur_frame]
                        self.cur_frame = (self.cur_frame + 1) % len(self.frames)
                        self.blockcount += 1
                    if self.blockcount == 7:
                        self.blockcount = 0
                        self.enemy_to_do = 'стоит'
                elif self.do == 'смерть':

                    if self.blockcount <= 6:
                        self.image = self.mirror_frames[self.cur_frame]
                        self.cur_frame = (self.cur_frame + 1) % len(self.frames)
                        self.blockcount += 1

                    if self.blockcount == 6:
                        self.blockcount = 0
                        self.rect = pygame.Rect(0, 0, 0, 0)
                        self.kill()
                else:
                    self.image = self.mirror_frames[self.cur_frame]
                    self.cur_frame = (self.cur_frame + 1) % len(self.frames)

        self.rect.x += self.xvel
        self.framecount += 1


class Boss(pygame.sprite.Sprite):
    def __init__(self, x, y, pers='босс', do='стоит'):
        super().__init__(enemy_sprites)
        self.frames = []
        self.cur_frame = 0
        self.pers = pers
        self.x = x
        self.hp = 180
        self.damage = 40
        self.do = do
        self.y = y
        self.mirror_frames = []
        self.isleft = False
        self.coordinats = [0, 0]
        self.cut_sheet(self.pers, do)
        self.framecount = 0
        self.enemy_to_do = 'стоит'
        self.blockcount = 0
        self.a = 0
        self.xvel = 0

    def cut_sheet(self, pers, do):
        self.frames = [load_image(pers, do, i, 50, 70, False) for i in
                       range(1, len([name for name in os.listdir(f'data\{pers}\{do}')]) + 1)]
        self.mirror_frames = [load_image(pers, do, i, 50, 70, True) for i in
                              range(1, len([name for name in os.listdir(f'data\{pers}\{do}')]) + 1)]
        self.rect = pygame.Rect(self.x, self.y, self.frames[0].get_width(), self.frames[0].get_height())
        self.cur_frame = 0
        if not self.isleft:
            self.image = self.frames[self.cur_frame]
        else:
            self.image = self.mirror_frames[self.cur_frame]

    def wait(self):
        self.enemy_to_do = "стоит"
        self.xvel = 0

    def the_pursuit(self):

        if self.do != 'урон' and self.do != 'смерть':

            if hero.rect.x - self.x > 10:
                self.xvel = MOVE_SPEED_enemy
                self.isleft = False
                self.enemy_to_do = 'идёт'
            elif hero.rect.x - self.x < 10:
                self.xvel = -MOVE_SPEED_enemy
                self.isleft = True
                self.enemy_to_do = 'идёт'
            else:
                self.wait()

    def random_life(self):
        if self.framecount % 100 == 0 and self.do != 'урон' and self.do != 'смерть':
            stop_or_go = random.randint(0, 1)
            if stop_or_go:
                left_or_right = random.randint(0, 1)
                rasst_from_start = self.x / 2 - self.start_x
                if rasst_from_start >= 15:
                    left_or_right = 0
                if rasst_from_start <= -15:
                    left_or_right = 1
                if left_or_right == 0:
                    self.xvel = -MOVE_SPEED_enemy
                    self.isleft = True
                    self.enemy_to_do = "идёт"
                elif left_or_right == 1:
                    self.xvel = MOVE_SPEED_enemy
                    self.isleft = False
                    self.enemy_to_do = "идёт"
            else:
                self.wait()

    def update(self):

        if self.do != self.enemy_to_do:
            self.do = self.enemy_to_do
            self.cut_sheet(self.pers, self.do)

        self.x = self.rect.x
        self.y = self.rect.y

        if hero.y == self.y:
            if 40 < abs(hero.rect.x - self.x) < 450:
                self.the_pursuit()
            elif abs(hero.rect.x - self.x) > 300:
                self.random_life()
            else:
                if self.a:
                    self.a -= 1
                    self.wait()
                else:
                    if abs(hero.rect.x - self.x) < 40:
                        self.enemy_to_do = 'бьёт'
                        self.xvel = 0

        if self.framecount % 10 == 0:
            if not self.isleft:
                if self.do == 'взлёт':
                    if self.blockcount < 4:
                        self.xvel = 0
                        self.image = self.frames[self.cur_frame]
                        self.cur_frame = (self.cur_frame + 1) % len(self.frames)
                        self.blockcount += 1
                    if self.blockcount == 4:
                        self.blockcount = 0
                        self.xvel = MOVE_SPEED_enemy
                        self.enemy_to_do = 'идёт'
                elif self.do == 'урон':
                    if self.blockcount < 6:
                        self.xvel = 0
                        self.image = self.frames[self.cur_frame]
                        self.cur_frame = (self.cur_frame + 1) % len(self.frames)
                        self.blockcount += 1
                    if self.blockcount == 6:
                        self.blockcount = 0
                        self.enemy_to_do = 'стоит'
                elif self.do == 'смерть':

                    if self.blockcount <= 8:
                        self.image = self.frames[self.cur_frame]
                        self.cur_frame = (self.cur_frame + 1) % len(self.frames)
                        self.blockcount += 1

                    if self.blockcount == 8:
                        self.blockcount = 0
                        self.rect = pygame.Rect(0, 0, 0, 0)
                        self.kill()

                else:
                    self.image = self.frames[self.cur_frame]
                    self.cur_frame = (self.cur_frame + 1) % len(self.frames)
            else:
                if self.do == 'взлёт':
                    if self.blockcount < 4:
                        self.image = self.mirror_frames[self.cur_frame]
                        self.cur_frame = (self.cur_frame + 1) % len(self.frames)
                        self.blockcount += 1
                        self.xvel = 0
                    if self.blockcount == 4:
                        self.blockcount = 0
                        self.enemy_to_do = 'идёт'
                        self.xvel = -MOVE_SPEED_enemy
                elif self.do == 'урон':
                    if self.blockcount < 6:
                        self.xvel = 0
                        self.image = self.mirror_frames[self.cur_frame]
                        self.cur_frame = (self.cur_frame + 1) % len(self.frames)
                        self.blockcount += 1
                    if self.blockcount == 6:
                        self.blockcount = 0
                        self.enemy_to_do = 'стоит'
                elif self.do == 'смерть':

                    if self.blockcount <= 8:
                        self.image = self.mirror_frames[self.cur_frame]
                        self.cur_frame = (self.cur_frame + 1) % len(self.frames)
                        self.blockcount += 1

                    if self.blockcount == 8:
                        self.blockcount = 0
                        self.kill()
                else:
                    self.image = self.mirror_frames[self.cur_frame]
                    self.cur_frame = (self.cur_frame + 1) % len(self.frames)
        self.rect.x += self.xvel
        self.framecount += 1


if __name__ == '__main__':
    pygame.init()
    pygame.display.set_caption('pygame')
    size = width, height = 1280, 768
    screen = pygame.display.set_mode(size)
    running = True
    arrow_sprites = pygame.sprite.Group()
    portal_sprites = pygame.sprite.Group()

    a = 0
    is_portal = False
    highscore = 0
    all_sprites = pygame.sprite.Group()
    platforms = []
    enemies = []

    bgImg = pygame.image.load(bgs[0])
    screen.blit(bgImg, (0, 0))



    

    fps = 60
    clock = pygame.time.Clock()

    levels = [level1, level2, level3]
    level = level1
    left, right, up = False, False, False
    spawn_coords = [[50, 540], [10, 300], [50, 300]]

    portal2 = Portal(650, 70)
    portal1 = Portal(40, 260)
    coordinats_enemy = [[430, 37], [110, 133], [370, 193]]
    for i in range(3):
        enemy_display = Enemy('зомби', coordinats_enemy[i][0], coordinats_enemy[i][1])
        enemies.append(enemy_display)
        enemy_sprites.add(enemy_display)





    b = ''
    with open('heroname.txt', 'r', encoding='utf-8') as f:
        b = f.read()
    if b == 'лучник':
        hero = Archer(*spawn_coords[0])
    elif b == 'маг':
        hero = Mage(*spawn_coords[0])
    elif b == 'мечник':
        hero = Swordman(*spawn_coords[0])
    all_sprites.add(hero)


    drawMap()



    while running:
        if a == 0:
            for e in pygame.event.get():
                if e.type == pygame.QUIT:
                    running = False
                    break
                if e.type == pygame.KEYDOWN:
                    if e.key == pygame.K_LEFT or e.key == pygame.K_a:
                        left = True
                        new_to_do = 'идёт'
                    if e.key == pygame.K_RIGHT or e.key == pygame.K_d:
                        right = True
                        new_to_do = 'идёт'
                    if e.key == pygame.K_UP or e.key == pygame.K_w:
                        up = True
                    if e.key == pygame.K_e:
                        if hero.pers == 'мечник':
                            new_to_do = 'блок'
                            hero.blockcount = 0
                        elif hero.pers == 'лучник':
                            new_to_do = 'тыкает'
                if e.type == pygame.MOUSEBUTTONDOWN:
                    new_to_do = 'бьёт'
                if e.type == pygame.KEYUP:
                    if e.key == pygame.K_RIGHT or e.key == pygame.K_d:
                        right = False
                        new_to_do = 'стоит'
                    if e.key == pygame.K_LEFT or e.key == pygame.K_a:
                        left = False
                        new_to_do = 'стоит'
                    if e.key == pygame.K_UP or e.key == pygame.K_w:
                        up = False
                    if e.key == pygame.K_e:
                        if hero.pers == 'мечник':
                            new_to_do = 'разблок'
                            hero.blockcount = 0

        elif a == 9:
            a -= 1
            new_to_do = 'стоит'
            hero.xvel, hero.yvel = 0, 0
            hero.up = False
            hero.onGround = True
        else:
            a -= 1
        screen.blit(bgImg, (0, 0))

        hero.update(left, right, up, platforms, new_to_do)

        enemy_sprites.draw(screen)
        enemy_sprites.update()
        all_sprites.draw(screen)
        arrow_sprites.draw(screen)
        arrow_sprites.update()
        portal_sprites.draw(screen)
        portal_sprites.update()
        if enemy_sprites.__len__() != 0:
            is_portal = False
        if enemy_sprites.__len__() == 0 and not is_portal:
            final = Final_Portal(800, 600)
            portal_sprites.add(final)
            is_portal = True
            if level == level3:
                win()
        clock.tick(fps)

        

        pygame.display.flip()

    pygame.quit()