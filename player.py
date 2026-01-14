from pgzero.actor import Actor
from pgzero.rect import Rect
from settings import GRAVITY, JUMP_FORCE, PLAYER_SPEED


class Player:
    def __init__(self, pos):
        self.idle_right = [
            "player_idle_right_0", "player_idle_right_1",
            "player_idle_right_2", "player_idle_right_3",
        ]
        self.idle_left = [
            "player_idle_left_0", "player_idle_left_1",
            "player_idle_left_2", "player_idle_left_3",
        ]
        self.walk_right = [
            "player_walk_right_00", "player_walk_right_01",
            "player_walk_right_02", "player_walk_right_03",
            "player_walk_right_04", "player_walk_right_05",
            "player_walk_right_06", "player_walk_right_07",
            "player_walk_right_08", "player_walk_right_09",
            "player_walk_right_10", "player_walk_right_11",
            "player_walk_right_12", "player_walk_right_13",
            "player_walk_right_14", "player_walk_right_15",
        ]
        self.walk_left = [
            "player_walk_left_00", "player_walk_left_01",
            "player_walk_left_02", "player_walk_left_03",
            "player_walk_left_04", "player_walk_left_05",
            "player_walk_left_06", "player_walk_left_07",
            "player_walk_left_08", "player_walk_left_09",
            "player_walk_left_10", "player_walk_left_11",
            "player_walk_left_12", "player_walk_left_13",
            "player_walk_left_14", "player_walk_left_15",
        ]

        self.actor = Actor(self.idle_right[0], pos=pos)

        self.hitbox = Rect(0, 0, 16, 32)
        self.hitbox.center = self.actor.center
        self.prev_rect = self.hitbox.copy()

        self.vy = 0
        self.on_ground = False

        self.direction = "right"
        self.facing = "right"

        self.frame = 0
        self.anim_timer = 0


    def update_hitbox(self):
        self.hitbox.center = self.actor.center

    def animate(self):
        if self.direction == "right":
            frames = self.walk_right
        elif self.direction == "left":
            frames = self.walk_left
        else:
            frames = self.idle_right if self.facing == "right" else self.idle_left

        if self.frame >= len(frames):
            self.frame = 0

        self.actor.image = frames[self.frame]

        self.anim_timer += 1
        if self.anim_timer >= 10:
            self.frame += 1
            if self.frame >= len(frames):
                self.frame = 0
            self.anim_timer = 0

    def move(self, keyboard):
        self.prev_rect = self.hitbox.copy()
        jumped = False
        moving = False

        if keyboard.A:
            self.actor.x -= PLAYER_SPEED
            self.direction = "left"
            self.facing = "left"
            moving = True

        elif keyboard.D:
            self.actor.x += PLAYER_SPEED
            self.direction = "right"
            self.facing = "right"
            moving = True

        if not moving:
            self.direction = "idle_left" if self.facing == "left" else "idle_right"

        if keyboard.space and self.on_ground:
            self.vy = JUMP_FORCE
            self.on_ground = False
            jumped = True

        self.animate()
        self.update_hitbox()
        return jumped

    def apply_gravity(self, platforms):

        self.vy += GRAVITY
        dy = self.vy

        steps = int(abs(dy))
        step_dir = 1 if dy > 0 else -1

        for _ in range(steps):
            self.actor.y += step_dir
            self.update_hitbox()

            for p in platforms:
                if self.hitbox.colliderect(p):
                    if step_dir > 0:
                        self.actor.bottom = p.top
                        self.on_ground = True
                    else:
                        self.actor.top = p.bottom

                    self.vy = 0
                    self.update_hitbox()
                    return  
        remainder = dy - (steps * step_dir)
        if remainder != 0:
            self.actor.y += remainder
            self.update_hitbox()

    def check_platforms(self, platforms):
        self.on_ground = False

        for p in platforms:
            if self.hitbox.colliderect(p):

                if self.vy > 0 and self.hitbox.bottom <= p.top + 10:
                    self.actor.bottom = p.top
                    self.vy = 0
                    self.on_ground = True

                elif self.vy < 0 and self.hitbox.top >= p.bottom - 10:
                    self.actor.top = p.bottom
                    self.vy = 0

                self.update_hitbox()

    def limit_map(self, width, height):
        if self.actor.left < 0:
            self.actor.left = 0

        if self.actor.right > width:
            self.actor.right = width

        if self.actor.top > height:
            return True

        self.update_hitbox()
        return False
    
    def check_walls(self, platforms):
        for p in platforms:
            if self.hitbox.colliderect(p):

                if self.prev_rect.right <= p.left:
                    self.actor.right = p.left

                elif self.prev_rect.left >= p.right:
                    self.actor.left = p.right

                self.update_hitbox()

    def draw(self):
        self.actor.scale = 2
        self.actor.draw()