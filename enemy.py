from pgzero.actor import Actor
from settings import GRAVITY

class Enemy:
    def __init__(self, pos, min_x, max_x):
        self.walk_right = ["enemy_right_0", "enemy_right_1", "enemy_right_2", "enemy_right_3"]
        self.walk_left = ["enemy_left_0", "enemy_left_1", "enemy_left_2", "enemy_left_3"]

        self.actor = Actor(self.walk_right[0], pos=pos)

        self.min_x = min_x
        self.max_x = max_x

        self.vel_y = 0
        self.on_ground = False

        self.frame = 0
        self.anim_timer = 0
        self.direction = "right"

        self.speed = 1

        self.hitbox = self.actor._rect

    def animate(self):
        if self.direction == "right":
            self.actor.image = self.walk_right[self.frame]
        elif self.direction == "left":
            self.actor.image = self.walk_left[self.frame]

        self.anim_timer += 1
        if self.anim_timer >= 10:
            self.frame = self.frame + 1
            if self.frame >= len(self.walk_right):
                self.frame = 0
            self.anim_timer = 0

    def update(self):
        self.actor.x += self.speed

        if self.actor.left <= self.min_x:
            self.actor.left = self.min_x
            self.speed = abs(self.speed)
            self.direction = "right"

        elif self.actor.right >= self.max_x:
            self.actor.right = self.max_x
            self.speed = -abs(self.speed)
            self.direction = "left"

        self.hitbox.topleft = self.actor.topleft
        self.animate()

    def apply_gravity(self):
        self.vel_y += GRAVITY
        self.actor.y += self.vel_y
        self.hitbox.topleft = self.actor.topleft

    def check_platforms(self, platforms):
        self.on_ground = False
        for p in platforms:
            if self.hitbox.colliderect(p) and self.vel_y > 0:
                self.actor.bottom = p.top
                self.vel_y = 0
                self.on_ground = True
                self.hitbox.topleft = self.actor.topleft

    def draw(self):
        self.actor.scale = 2
        self.actor.draw()