import pygame as pg
import settings
import ui

class ShopState:
    
    def __init__(self, gdata):
        self.gdata = gdata
        if not self.gdata.shop:
            shop_tl = (settings.WIN_SIZE[0] - ui.Shop.size[0]) // 2,\
            (settings.WIN_SIZE[1] - ui.Shop.size[1]) // 2
            self.gdata.shop = ui.Shop(self.gdata, shop_tl)
            self.gdata.shop.add_item(ui.ReloadBoost(self.gdata))
            self.gdata.shop.add_item(ui.TurnBoost(self.gdata))
            self.gdata.shop.add_item(ui.SpreadShot(self.gdata))
            self.gdata.shop.add_item(ui.Shockwave(self.gdata))
            self.gdata.shop.add_item(ui.Piercing(self.gdata))

        btn_size = 200, 75
        quit_tl = settings.WIN_SIZE[0] - btn_size[0] - 20,\
            settings.WIN_SIZE[1] -btn_size[1] - 20
        self.quit_btn = ui.Button(quit_tl, btn_size, self.on_quit, "Quit",\
            self.gdata.fonts["Large"])
        
        self.shop_prompt = gdata.fonts["tiny"].render("Press Space to Resume",\
            True, settings.WHITE)
        self.shop_ptl = (settings.WIN_CENTER[0] - self.shop_prompt.get_width() // 2,\
            settings.WIN_SIZE[1] - self.shop_prompt.get_height() - 20)

    def start_up(self):
        self.gdata.shop.start_up()
        self.gdata.mmanager.add(self.quit_btn)

    def on_quit(self, mpos):
        self.gdata.quit = bool(1)
        self.gdata.smechine.remove()

    def update(self, dt):
        self.gdata.mmanager.update()

    def handle_event(self, event):
        self.gdata.mmanager.handle_event(event)
        if event.type == pg.KEYDOWN and event.key == pg.K_SPACE:
            self.gdata.smechine.remove()

    def draw(self, screen):
        screen.fill(settings.BLACK)
        self.gdata.bullets.draw(screen)
        self.gdata.enemies.draw(screen)
        self.gdata.player.draw(screen)
        self.draw_ui(screen, self.gdata.player.health, self.gdata.player.max_health,\
            self.gdata.player.money)
        self.gdata.shop.draw(screen)
        self.quit_btn.draw(screen)

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
        surface.blit(self.shop_prompt, self.shop_ptl)

    def clean_up(self):
        self.gdata.shop.clean_up()
        self.gdata.mmanager.remove(self.quit_btn)