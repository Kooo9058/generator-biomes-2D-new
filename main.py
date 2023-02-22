import pygame as pg
import settings
import biome as bm


class App:
    def __init__(self):
        self.screen = pg.display.set_mode(settings.RES)
        self.clock = pg.time.Clock()
        self.biomes = bm.Biomes(app=self, pg=pg)

    def run(self):
        while True:
            pg.display.update()
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    pg.quit()
                elif event.type == pg.KEYDOWN:
                    if event.key == pg.K_SPACE:
                        self.biomes.main_render_biomes()

            self.clock.tick(settings.TIMER)
            pg.display.set_caption(f'FPS: {self.clock.get_fps()}')


if __name__ == '__main__':
    app = App()
    app.run()
