import pygame as pg
from player import ShockwaveBullet
from player import Bullet
from collections import deque
import settings
import time

def center(dest_surf, src_surf):
    return (dest_surf.get_width() - src_surf.get_width()) // 2, \
        (dest_surf.get_height() - src_surf.get_height()) // 2

def rgba(color, alpha):
    return color[0], color[1], color[2], alpha

class Score:
    
    def __init__(self):
        self.scores = deque([None] * 5)
        self.hs = None

    def add(self, score):
        scr = (score, time.strftime("%m/%d/%y"), time.strftime("%H:%M:%S"))
        if self.hs == None or score > self.hs[0]:
            self.hs = scr
        self.scores.appendleft(scr)
        self.scores.pop()

class Button:

    def __init__(self, topleft, size, on_click, text, font):
        self.rect = pg.Rect(topleft, size)
        self.on_click = on_click
        self.text = text
        self.font = font
        self.image = pg.Surface(size, pg.SRCALPHA)
        
        self.mhover = bool(0)
        self.mdown = bool(0)
        self.btnid = None
        
        self.id = Button.nid
        Button.nid += 1

        self.redraw()

    def redraw(self):
        self.image.fill(rgba(settings.BLACK, 255))
        if self.mhover:
            text_color = settings.BLACK
            self.image.fill(rgba(settings.WHITE, 255))
        else:
            text_color = settings.WHITE
        pg.draw.rect(self.image, settings.WHITE, self.image.get_rect(), 3)
        text = self.font.render(self.text, True, text_color)
        self.image.blit(text, center(self.image, text))

    def draw(self, surf):
        surf.blit(self.image, self.rect.topleft)

    def contains(self, mpos):
        return self.rect.collidepoint(mpos)

    def on_mouse_enter(self, mpos):
        self.mhover = bool(1)
        self.redraw()

    def on_mouse_exit(self, mpos):
        self.mhover = bool(0)
        self.redraw()

    def on_mouse_down(self, mpos):
        self.mdown = bool(1)
        self.redraw()

    def on_mouse_up(self, mpos):
        self.mdown = bool(0)
        self.redraw()

Button.nid = 0


class ShopItem:

    def __init__(self, gdata, text, cost):
        self.gdata = gdata
        self.rect = pg.Rect((0, 0), ShopItem.size)
        self.text = self.gdata.fonts["small"].render(text, True, settings.WHITE)
        self.cost = cost
        self.btn = Button(ShopItem.btn_tl, ShopItem.btn_size, self.on_buy, \
            "$" + str(cost), self.gdata.fonts["small"])

    def move(self, dx, dy):
        self.rect.move_ip(dx, dy)
        self.btn.rect.move_ip(dx, dy)

    def draw(self, screen):
        pg.draw.rect(screen, settings.WHITE, self.rect, 3)
        text_tl = self.rect.width - self.text.get_width() - self.btn.rect.width - 20,\
            self.rect.height - self.text.get_height()
        text_tl = self.rect.left + text_tl[0] // 2, self.rect.top + text_tl[1] //2
        screen.blit(self.text, text_tl)
        self.btn.draw(screen)
    
    def on_buy(self, mpos):
        pass

ShopItem.size = 500, 100
ShopItem.btn_size = 125, 60
ShopItem.btn_tl = (ShopItem.size[0] - ShopItem.btn_size[0] - 20,\
    (ShopItem.size[1] - ShopItem.btn_size[1]) // 2)

class ReloadBoost(ShopItem):

    def __init__(self, gdata):
        super().__init__(gdata, "Reload Faster", 150)

    def on_buy(self, mpos):
        if self.gdata.player.money >= self.cost:
            self.gdata.player.money -= self.cost
            self.gdata.player.set_reload_time(
                int(0.45 * self.gdata.player.reload_time)
            )
            self.cost *= 2
            self.btn.text = "$" + str(self.cost)
            self.btn.redraw()

class TurnBoost(ShopItem):
    def __init__(self, gdata):
        self.boost = 2
        super().__init__(gdata, "Turn Faster", 150)

    def on_buy(self, mpos):
        if self.gdata.player.money >= self.cost:
            self.gdata.player.money -= self.cost
            self.gdata.player.avel = self.gdata.player.avel + self.boost
            self.boost += 1.5
            self.cost *= 2
            self.btn.text = "$" + str(self.cost)
            self.btn.redraw()
        
class SpreadShot(ShopItem):
    def __init__(self, gdata):
        self.bought = False
        super().__init__(gdata, "Shotgun", 600)

    def on_buy(self, mpos):
        if self.gdata.player.money >= self.cost and not self.bought:
            self.gdata.player.money -= self.cost
            self.gdata.player.spread_shot = True
            self.btn.text = "----"
            self.bought = True
            self.btn.redraw()

class Shockwave(ShopItem):
    def __init__(self, gdata):
        super().__init__(gdata, "Bomb", 800)

    def on_buy(self, mpos):
        if self.gdata.player.money >= self.cost:
            self.gdata.player.money -= self.cost
            self.gdata.bullets.add(ShockwaveBullet(self.gdata, settings.WIN_CENTER))
            self.cost *= 1.5
            self.btn.text = "$" + str(self.cost)
            self.btn.redraw()
            
class Piercing(ShopItem):
    def __init__(self, gdata):
        self.bought = False
        super().__init__(gdata, "Piercing Shot", 3000)

    def on_buy(self, mpos):
        if self.gdata.player.money >= self.cost and not self.bought:
            self.gdata.player.money -= self.cost
            Bullet.piercing = True
            self.btn.text = "----"
            self.bought = True
            self.btn.redraw()

class Shop:

    def __init__(self, gdata, topleft):
        self.gdata = gdata
        self.vgap = 10
        self.rect = pg.Rect(topleft, Shop.size)
        self.item_rect = self.rect.move(10, 10)
        self.items = []

    def start_up(self):
        for item in self.items:
            self.gdata.mmanager.add(item.btn)

    def add_item(self, item):
        self.items.append(item)
        item.move(self.item_rect.left, self.item_rect.top)
        self.item_rect.move_ip(0, ShopItem.size[1] + self.vgap)
        self.gdata.mmanager.add(item.btn)

    def draw(self, screen):
        pg.draw.rect(screen, settings.BLACK, self.rect)
        for item in self.items:
            item.draw(screen)
        pg.draw.rect(screen, settings.WHITE, self.rect, 3)
    
    def clean_up(self):
        for item in self.items:
            self.gdata.mmanager.remove(item.btn)
    

Shop.size = ShopItem.size[0] + 20, (ShopItem.size[1] + 10) * 7