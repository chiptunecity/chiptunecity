"""
Tiaki Studios present
Chiptune City Release 1.0.0
"""
import os

os.environ["PYGAME_HIDE_SUPPORT_PROMPT"] = "1"

try:
    import pgzero
    import pygame
    import pgzrun
    from pygame import mixer
    from platformer import *
except:
    print("Error code: 0x0A")

TILE_SIZE = 18
ROWS = 30
COLS = 20
default_level = 1
wins = 0
platforms = None
obstacles = None
mushrooms = None
WIDTH = 540
HEIGHT = 360
TITLE = "ChipTune City"
collectedshrooms = 0

over = False
win = False
deaths = 0
gravity = 1
jump_velocity = -10
speed = 3
allow_skip = False
start = False
tp = False
pause = False
# Build world
def create_world(level):
    global platforms, obstacles, mushrooms, default_level
    platforms = build(f"levels/{level}platformer_platforms.csv", TILE_SIZE)
    obstacles = build(f"levels/{level}platformer_obstacles.csv", TILE_SIZE)
    mushrooms = build(f"levels/{level}platformer_mushrooms.csv", TILE_SIZE)


create_world(1)

# Initialize player
player = Actor("p_right")
background = Actor("menubg")
player.bottomleft = (0, (HEIGHT - TILE_SIZE) * 0.6)
player.velocity_x = speed
player.velocity_y = speed - 3
player.jumping = False
player.alive = True


def draw():
    global over, collectedshrooms, deaths, win, tp, start
    background.draw()
    screen.draw.text("CHIPTUNE CITY", center=(WIDTH//2, HEIGHT//2-60), fontsize=32, fontname="8bit")
    screen.draw.text("Press C to start", center=(WIDTH//2, HEIGHT//2+50), fontsize=16, fontname="8bit")
    screen.draw.text("Tiaki Studios\nChiptune City 1.1.0", bottomleft=(0, HEIGHT), fontsize=8, fontname='8bit')
    if start:

        screen.clear()
        screen.fill("skyblue")
        for platform in platforms:
            platform.draw()
        for obstacle in obstacles:
            obstacle.draw()
        for mushroom in mushrooms:
            mushroom.draw()
        if not over:
            player.draw()
    if over:
        player.bottomleft = (0, HEIGHT - TILE_SIZE)
        deaths += 1
        player.visible = False
        # screen.draw.text("YOU DIED!", center=(WIDTH//2, HEIGHT//2-60), fontsize=32, fontname="8bit", color='black')
        # screen.draw.text("Press R to respawn", center=(WIDTH//2, HEIGHT//2+60), fontsize=16, fontname="8bit", color='black ')
        over = False
    if win:
        global default_level
        default_level += 1
        create_world(default_level)
        player.bottomleft = (0, HEIGHT - TILE_SIZE)
        win = False
    if pause:
        start = False
        screen.fill("black")
        screen.draw.text("Game Paused\n\n\n\nPress C to resume", center=(WIDTH // 2, HEIGHT // 2 - 60), fontsize=24, fontname="8bit",color='white')






def update():
    global over, win, collectedshrooms
    if (keyboard.LEFT or keyboard.A) and player.midleft[0] > 0:
        player.x -= player.velocity_x
        player.image = "p_left"
        if player.collidelist(platforms) != -1:
            object = platforms[player.collidelist(platforms)]
            player.x = object.x + (object.width / 2 + player.width / 2)
    if (keyboard.RIGHT or keyboard.D) and player.midright[0] < WIDTH:
        player.x += player.velocity_x
        player.image = "p_right"
        if player.collidelist(platforms) != -1:
            object = platforms[player.collidelist(platforms)]
            player.x = object.x - (object.width / 2 + player.width / 2)
    player.y += player.velocity_y
    player.velocity_y += gravity
    if player.collidelist(platforms) != -1:
        object = platforms[player.collidelist(platforms)]
        if player.velocity_y >= 0:
            player.y = object.y - (object.height / 2 + player.height / 2)
            player.jumping = False
        else:
            player.y = object.y + (object.height / 2 + player.height / 2)
        player.velocity_y = 0
    if player.collidelist(obstacles) != -1:
        player.alive = False
        over = True
        player.bottomleft = (0, TILE_SIZE)
    for mushroom in mushrooms:
        if player.colliderect(mushroom):
            mushrooms.remove(mushroom)
            collectedshrooms += 1
    if len(mushrooms) == 0:
        win = True


def on_key_down(key):
    global allow_skip, win, gravity, start, over, tp, pause
    if (key == keys.UP or key == keys.W or key == keys.SPACE) and not player.jumping:
        player.velocity_y = jump_velocity
        player.jumping = True
    elif key == keys.M:
        mixer.quit()
    elif key == keys.S and allow_skip:
        win = True
    elif key == keys.E:
        print('Chiptune City: How to play')
        print('\nUse the arrow keys to Move and Jump')
        print('Press F for a longer time on air')
    elif key == keys.ESCAPE:
        pause = True
    elif key == keys.F:
        gravity = 0.6
    elif key == keys.C:
        start = True
        pause = False
    elif key == keys.R:
        over=False




def on_key_up(key):
    global gravity
    if key == keys.F:
        gravity = 1



pgzrun.go()
