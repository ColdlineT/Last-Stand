import pygame as pg
from shop_state import ShopState
from player import Player
from player import EnemyGenerator
from player import ObjectManager
from player import Bullet
import settings
import ui

def collide_circle(e1, e2):
    dx, dy = e1.x - e2.x, e1.y - e2.y
    return dx ** 2 + dy ** 2 < (e1.radius + e2.radius) ** 2

class GameState:
    
    def __init__(self, gdata):
        self.gdata = gdata
        gdata.player = Player(gdata)
        gdata.bullets = ObjectManager()
        gdata.enemies = ObjectManager()
        gdata.enemygen = EnemyGenerator(gdata)
        gdata.time = 0
        gdata.quit = bool(0)
        gdata.shop = None
        Bullet.piercing = bool(0)

        self.shop_prompt = gdata.fonts["tiny"].render("Press Space to open Shop",\
            True, settings.WHITE)
        self.shop_ptl = (settings.WIN_CENTER[0] - self.shop_prompt.get_width() // 2,\
            settings.WIN_SIZE[1] - self.shop_prompt.get_height() - 20)
        
    def start_up(self):
        pass

    def update(self, dt):
        if self.gdata.quit:
            self.gdata.smechine.remove()
        
        self.gdata.player.update(dt)
        self.gdata.enemygen.update(dt)
        self.gdata.bullets.update(dt)
        self.gdata.enemies.update(dt)
        self.gdata.time += dt

        for bullet in self.gdata.bullets.objects:
            for enemy in self.gdata.enemies.objects:
                if collide_circle(bullet, enemy):
                    bullet.collide(enemy)

        for enemy in self.gdata.enemies.objects:
            if collide_circle(enemy, self.gdata.player):
                enemy.collide_player()

    def handle_event(self, event):
        self.gdata.player.handle_event(event)
        if event.type == pg.KEYDOWN and event.key == pg.K_SPACE:
            GameState.show_shop_prompt = False
            if self.gdata.player.health >= 0:
                self.gdata.smechine.add(ShopState(self.gdata), False)
            
    def draw(self, screen):
        screen.fill(settings.BLACK)
        self.gdata.bullets.draw(screen)
        self.gdata.enemies.draw(screen)
        self.gdata.player.draw(screen)
        self.draw_ui(screen, self.gdata.player.health, self.gdata.player.max_health,\
            self.gdata.player.money)

    def draw_ui(self, surface, hp, mhp, money):
        font = self.gdata.fonts["small"]
        hptext = font.render(str(hp) + " / " + str(mhp), True, settings.WHITE)
        moneytext = font.render("$ " + str(money), True, settings.WHITE)
        time = font.render(str(self.gdata.time // 1000) + " secs", True, settings.WHITE)
        
        rect = pg.Rect(settings.WIN_SIZE[0] - 10, 10, 0, 0)
        surface.blit(hptext, rect.move(-hptext.get_width(), 0).topleft)
        rect.move_ip(0, 10 + hptext.get_height())
        
        surface.blit(moneytext, rect.move(-moneytext.get_width(), 0).topleft)
        # rect.move_ip(0, 10 + moneytext.get_height())
        time_tl = settings.WIN_CENTER[0] - time.get_width() // 2, 10
        surface.blit(time, time_tl)
        if GameState.show_shop_prompt:
            surface.blit(self.shop_prompt, self.shop_ptl)

    def clean_up(self):
        pass

GameState.show_shop_prompt = bool(1)