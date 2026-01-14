from pgzero.actor import Actor
from pgzero.rect import Rect

class Coin:
    def __init__(self, pos):
        self.frames = ["coin_00", "coin_01", "coin_02", "coin_03", 
                       "coin_04", "coin_05", "coin_06", "coin_07", 
                       "coin_08", "coin_09", "coin_10", "coin_11"]
        self.actor = Actor(self.frames[0], pos=pos)

        self.hitbox = Rect(0, 0, 16, 16)
        self.hitbox.center = self.actor.center

        self.frame = 0
        self.timer = 0
        self.collected = False

    def update(self):
        self.timer += 1
        if self.timer >= 10:
            self.frame = self.frame + 1
            if self.frame >= len(self.frames):
                self.frame = 0
            self.actor.image = self.frames[self.frame]
            self.timer = 0

        self.hitbox.center = self.actor.center

    def draw(self):
        if not self.collected:
            self.actor.draw()