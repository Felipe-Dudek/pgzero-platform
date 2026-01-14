# -*- coding: utf-8 -*-
import pgzrun
from settings import WIDTH, HEIGHT
from levels import LEVELS
from player import Player
from enemy import Enemy
from menu import Menu
from coin import Coin

WIDTH = WIDTH
HEIGHT = HEIGHT

GAME_OVER = "game_over"
MENU = "menu"
PLAYING = "playing"
WIN = "win"

MAX_LIVES = 3
lives = MAX_LIVES

score = 0
current_level = 0

state = MENU

sound_on = True
music_on = True
playing_music = False

menu = Menu()
player = Player((0, 0))
platforms = []
enemies = []
door = None
coin = None

def load_level():
    global player, platforms, enemies, door, coin

    level = LEVELS[current_level]

    player.actor.pos = level["start"]
    player.hitbox.center = player.actor.center
    platforms = level["platforms"]

    enemies.clear()
    for e in level["enemies"]:
        enemies.append(Enemy(e["pos"], e["min_x"], e["max_x"]))

    coin = Coin(level["coin"])
    door = level["door"]

def handle_music():
    global playing_music

    if music_on:
        if not music.is_playing("background_theme"):
            music.play("background_theme")
            music.set_volume(0.4)
        playing_music = True
    else:
        if playing_music:
            music.stop()
            playing_music = False

def lose_life():
    global lives, state
    lives -= 1

    if lives <= 0:
        state = GAME_OVER
    else:
        load_level()
        if sound_on:
            sounds.hurt.play()


def update_enemies():
    global score

    for e in enemies[:]:
        e.update()
        e.apply_gravity()
        e.check_platforms(platforms)

        if player.hitbox.colliderect(e.hitbox):
            if player.vy > 0 and player.hitbox.bottom < e.hitbox.centery:
                enemies.remove(e)
                player.vy = -6
                score += 100
                if sound_on:
                    sounds.hit.play()
            else:
                lose_life()
                score -= 50
                if sound_on:
                    sounds.hurt.play()


def update_coin():
    global score

    coin.update()
    if not coin.collected and player.hitbox.colliderect(coin.hitbox):
        coin.collected = True
        score += 50
        if sound_on:
            sounds.coin.play()

def try_advance_level():
    global current_level, state

    if player.hitbox.colliderect(door) and coin.collected:
        current_level += 1
        if current_level >= len(LEVELS):
            state = WIN
        else:
            load_level()
            if sound_on:
                sounds.level_up.play()


def update_playing():
    jumped = player.move(keyboard)

    if jumped and sound_on:
        sounds.jump.play()

    player.check_walls(platforms)

    player.apply_gravity(platforms)

    fell = player.limit_map(WIDTH, HEIGHT)
    if fell:
        lose_life()
        return

    update_enemies()
    try_advance_level()
    update_coin()

def update():
    global state

    handle_music()

    if state == PLAYING:
        update_playing()
        if sound_on and state == GAME_OVER:
            sounds.game_over.play()
            handle_music()

def draw_hud():
    screen.draw.text(
        f"Vidas: {lives}",
        topleft=(10, 10),
        fontsize=30,
        color="white"
    )
    screen.draw.text(
        f"Pontos: {score}",
        topleft=(10, 40),
        fontsize=30,
        color="yellow"
    )


def draw_menu():
    menu.draw(screen, sound_on, music_on)


def draw_game_over():
    screen.draw.text(
        "GAME OVER",
        center=(WIDTH // 2, HEIGHT // 2 - 40),
        fontsize=64,
        color="red"
    )
    screen.draw.text(
        "Clique para voltar ao menu",
        center=(WIDTH // 2, HEIGHT // 2 + 20),
        fontsize=32,
        color="white"
    )


def draw_win():
    screen.draw.text(
        "YOU WIN!",
        center=(WIDTH // 2, HEIGHT // 2 - 40),
        fontsize=64,
        color="green"
    )
    screen.draw.text(
        f"SCORE: {score}",
        center=(WIDTH // 2, HEIGHT // 2 + 10),
        fontsize=32,
        color="yellow"
    )
    screen.draw.text(
        "CLICK HERE TO BACK TO MENU",
        center=(WIDTH // 2, HEIGHT // 2 + 60),
        fontsize=28,
        color="white"
    )


def draw_playing():
    for p in platforms:
        screen.draw.filled_rect(p, (120, 120, 120))

    screen.draw.filled_rect(door, (150, 75, 0))

    for e in enemies:
        e.draw()

    player.draw()
    coin.draw()
    draw_hud()


def draw():
    screen.clear()
    screen.blit("background", (0, 0))

    if state == MENU:
        draw_menu()
    elif state == GAME_OVER:
        draw_game_over()
    elif state == WIN:
        draw_win()
    else:
        draw_playing()

def on_mouse_down(pos):
    global state, sound_on, music_on, playing_music, lives, current_level, score

    if state == MENU:
        action = menu.click(pos)

        if action == "start":
            lives = MAX_LIVES
            current_level = 0
            load_level()
            state = PLAYING

        if action == "music":
            music_on = not music_on

        elif action == "sound":
            sound_on = not sound_on
            playing_music = False

        elif action == "exit":
            quit()

    elif state == GAME_OVER:
        lives = MAX_LIVES
        current_level = 0
        state = MENU
        score = 0

    elif state == WIN:
        score = 0
        lives = MAX_LIVES
        current_level = 0
        state = MENU

pgzrun.go()