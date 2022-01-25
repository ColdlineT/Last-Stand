import pygame as pg
import settings
import ui

class GameOverState:
    
    def __init__(self, gdata):
        self.gdata = gdata
        height = 220
        top = settings.WIN_CENTER[1] - height // 2
        rect = pg.Rect(-10, top - 160, settings.WIN_SIZE[0] + 20, height)

        btn_size = 80, 50
        btn_left = (settings.WIN_SIZE[0] - btn_size[0]) // 2
        btn_top = rect.top + rect.height // 2
        
        self.ok_btn = ui.Button((btn_left, btn_top), btn_size, self.on_ok, "Ok",\
            self.gdata.fonts["Large"])

        self.text = self.gdata.fonts["Large"].render(f"Bruh, Only {self.gdata.time // 1000}  seconds", True, settings.WHITE)
        text_left = (settings.WIN_SIZE[0] - self.text.get_width()) // 2
        text_top = rect.height // 4 - self.text.get_height() // 2 + rect.top
        self.text_tl = text_left, text_top

    def on_ok(self):
        self.gdata.smechine.remove()

    def start_up(self):
        self.gdata.score.add(self.gdata.time // 1000)
        self.gdata.mmanager.add(self.ok_btn)

    def update(self):
        self.gdata.mmanager.update()

    def handle_event(self, event):
        self.gdata.mmanager.handle_event(event)

    def draw(self, screen):
        screen.fill(settings.BLACK)
        self.gdata.bullets.draw(screen)
        self.gdata.enemies.draw(screen)
        self.gdata.player.draw(screen)
        screen.blit(self.text, self.text_tl)
        self.ok_btn.draw(screen)

    def clean_up(self):
        self.gdata.mmanager.remove(self.ok_btn)