# pgzero
import random

cell = Actor('блокккк')

WIDTH = 600
HEIGHT = 800

TITLE = "Energy Wars"  # Заголовок окна игры
FPS = 60  # Количество кадров в секунду

# объекты
char = Actor('главный герой2', (575, 455))
leg = Actor('ноги')
fon = Actor('фон')
enemy_tree1 = Actor('д заражёное 1')
enemy_tree2 = Actor('д заражёное 2')
enemy_shrum1 = Actor('г заражёый 1')
enemy_shrum2 = Actor('г заражёый 2')
enemy_bee = Actor('п заражёная 12')
mistore = Actor('предмет з')
iron = Actor('предмет ж')
wires = Actor('предмет п')
glas = Actor('предмет с')
syringe = Actor('оружие нчк')
gan1 = Actor('оружие мк')
gan2 = Actor('оружие бк')
sword = Actor('оружие блк')
sayler = Actor('торговец', (340, 455))
buttun = Actor('кнопка', (300, 400))
buttun_inventory = Actor('кнопка', (550, 50))
# переменые
mode = 'menu'

# таблицы
list0 = [[1, 1, 1, 1, 1, 1, 1],
         [1, 1, 1, 1, 1, 1, 1],
         [1, 0, 0, 0, 0, 0, 1],
         [0, 0, 0, 0, 0, 0, 0],
         [0, 0, 0, 0, 0, 0, 0],
         [1, 1, 1, 1, 1, 1, 1],
         [1, 1, 1, 1, 1, 1, 1]]

list1 = [[1, 1, 1, 1, 1, 1, 1],
         [1, 1, 1, 1, 1, 1, 1],
         [0, 0, 0, 0, 0, 0, 0],
         [0, 0, 0, 0, 0, 0, 0],
         [0, 0, 1, 1, 0, 0, 0],
         [1, 1, 1, 1, 1, 1, 1],
         [1, 1, 1, 1, 1, 1, 1]]


# отрисовка  карты
def map_draw():
    for i in range(len(list0)):
        for j in range(len(list0[0])):
            if list0[i][j] == 1:
                cell.left = cell.width * j
                cell.top = cell.height * i
                cell.draw()


def map_draw1():
    for i in range(len(list1)):
        for j in range(len(list1[0])):
            if list1[i][j] == 1:
                cell.left = cell.width * j
                cell.top = cell.height * i
                cell.draw()


def draw():
    if mode == 'start':
        fon.draw()
        map_draw()
        char.draw()
        sayler.draw()
        leg.draw()
        buttun_inventory.draw()
        screen.draw.text("инвентарь", center=(530, 50), color='white', fontsize=20)
    if mode == "menu":
        fon.draw()
        buttun.draw()
        screen.draw.text("играть", center=(300, 420), color='white', fontsize=20)


def update(dt):
    old_x = char.x
    old_y = char.y
    leg.x = char.x + 5
    leg.y = char.y + 30
    if keyboard.d and char.x <= 590:
        char.x += 5
        leg.x += 5
    if keyboard.a and char.x >= 10:
        char.x -= 5
        leg.x -= 5
    cell_index = char.collidelist(list0)
    if cell_index != -1:
        char.x = old_x
        char.y = old_y


def on_key_down(key):
    if keyboard.w:
        char.y -= 80
        leg.y -= 80
        animate(char, tween='bounce_end', duration=4, y=455)