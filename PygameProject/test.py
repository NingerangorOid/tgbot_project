import pygame
import os
import sys

import pygame.sprite

pygame.init()
size = width, height = 800, 800
screen = pygame.display.set_mode(size)
pygame.display.set_caption('Чёрное в белое и наоборот')
clock = pygame.time.Clock()
all_sprites = pygame.sprite.Group()
sprite = pygame.sprite.Sprite()
pygame.mouse.set_visible(False)
coordinats = [0, 0]

class Character(pygame.sprite.Sprite):
    def __init__(self, name, frame_count_moving):#, frame_count_waiting, frame_count_hitting, frame_count_damage, frame_count_death):
        super.__init__()
        self.path = os.path.join('data', name)
        image = load_image("")
        self.frames_moving = [load_image(str(i)) for i in range(frame_count_moving)]
        print(self.frames_moving)
        #self.frame_count_hitting = frame_count_hitting
        #self.frame_count_damage = frame_count_damage
        #self.frame_count_death = frame_count_death
        #self.frame_count_waiting = frame_count_waiting

        def __init__(self):
            # НЕОБХОДИМО вызвать конструктор родительского класса Sprite.
            # Это очень важно!!!
            super().__init__(self)
            self.image = image
            self.rect = self.image.get_rect()
            print(self.rect)

        def update(self):
            self.rect = self.rect.move(0, -1)

def load_image(name, colorkey=None):
    fullname = os.path.join('data', name)
    # если файл не существует, то выходим
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()
    image = pygame.image.load(fullname)
    image1 = pygame.transform.scale(image, (40, 70))
    return image1


fps = 100
running = True
A = Character('герой мечник', 12)
while running:
    mage = load_image('mage.png')
    mage2 = load_image('swordman.png')
    skelet = load_image('enemy.png')
    screen.fill((255, 255, 255))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                coordinats[0] -= 10
            if event.key == pygame.K_RIGHT:
                coordinats[0] += 10
            if event.key == pygame.K_DOWN:
                coordinats[1] += 10
            if event.key == pygame.K_UP:
                coordinats[1] -= 10
    screen.blit(A, coordinats)
    screen.blit(mage, coordinats)
    screen.blit(mage2, (coordinats[0] + 100, coordinats[1]))
    screen.blit(skelet, (coordinats[0] + 200, coordinats[1]))

    pygame.display.flip()
    clock.tick(fps)
pygame.quit()