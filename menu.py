from pgzero.rect import Rect
from settings import WIDTH

class Menu:
    def __init__(self):
        self.start = Rect((300, 160), (200, 50))
        self.music = Rect((300, 230), (200, 50))
        self.sound = Rect((300, 300), (200, 50))
        self.exit = Rect((300, 370), (200, 50))

    def draw(self, screen, sound_on, music_on):
        screen.draw.text("Space Adventure", center=(WIDTH//2, 80), fontsize=48)

        screen.draw.filled_rect(self.start, (50, 150, 50))
        screen.draw.text("START", center=self.start.center, fontsize=32)

        screen.draw.filled_rect(self.music, (50, 50, 150))
        txt = "MUSIC ON" if music_on else "MUSIC OFF"
        screen.draw.text(txt, center=self.music.center, fontsize=32)

        screen.draw.filled_rect(self.sound, (50, 50, 150))
        txt = "SOUND ON" if sound_on else "SOUND OFF"
        screen.draw.text(txt, center=self.sound.center, fontsize=32)

        screen.draw.filled_rect(self.exit, (150, 50, 50))
        screen.draw.text("EXIT", center=self.exit.center, fontsize=32)

    def click(self, pos):
        if self.start.collidepoint(pos):
            return "start"
        if self.music.collidepoint(pos):
            return "music"
        if self.sound.collidepoint(pos):
            return "sound"
        if self.exit.collidepoint(pos):
            return "exit"
        return None