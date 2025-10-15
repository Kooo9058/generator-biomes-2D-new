import random
import time
from enum import Enum
import settings


class BiomesType(Enum):
    SEA = 0
    LAND = 1
    SAND = 2
    SEA_SHORE = 3
    WOODS = 4

class Biomes:
    def __init__(self, app, pg):
        self.app = app
        self.pg = pg
        self.matrix = self.create_start_matrix()

    def main_render_biomes(self):
        start = time.time()
        self.set_layout_lands_and_sea()
        self.set_layout_sands()
        self.set_layout_sea_shore()
        self.set_layout_woods()
        print(f'Render Time is {time.time() - start:.2f}s')

    # -------------------- LAND & SEA --------------------
    def set_layout_lands_and_sea(self):
        self.matrix = self.create_start_matrix()
        for _ in range(settings.COUNTS_ALGORITHMS):
            self.next_generation(BiomesType.LAND, BiomesType.SEA, [3,6,7,8])
            self.next_generation(BiomesType.SEA, BiomesType.LAND, [3,6,7,8])

    # -------------------- GENERIC --------------------
    def count_neighbors(self, x, y, biome_type):
        count = 0
        rows, cols = len(self.matrix), len(self.matrix[0])
        for dx in [-1,0,1]:
            for dy in [-1,0,1]:
                if dx == 0 and dy == 0:
                    continue
                nx, ny = x+dx, y+dy
                if 0 <= nx < rows and 0 <= ny < cols:
                    if self.matrix[nx][ny] == biome_type:
                        count += 1
        return count

    def next_generation(self, target_biome, new_biome, rules):
        rows, cols = len(self.matrix), len(self.matrix[0])
        for x in range(rows):
            for y in range(cols):
                neighbors = self.count_neighbors(x, y, new_biome)
                if self.matrix[x][y] == target_biome and neighbors in rules:
                    self.matrix[x][y] = new_biome
                    self.paint_pixel_element(new_biome, x, y)
        self.pg.display.update()

    # -------------------- SAND --------------------
    def set_layout_sands(self):
        self.start_border(BiomesType.LAND, BiomesType.SEA, BiomesType.SAND, 1)
        for _ in range(settings.COUNTS_ALGORITHMS_SANDS):
            self.next_sand_gen()

    def start_border(self, target, neighbor, new_biome, min_neighbors=1):
        rows, cols = len(self.matrix), len(self.matrix[0])
        for x in range(rows):
            for y in range(cols):
                if self.matrix[x][y] == target:
                    if self.count_neighbors(x, y, neighbor) >= min_neighbors:
                        self.matrix[x][y] = new_biome
                        self.paint_pixel_element(new_biome, x, y)
        self.pg.display.update()

    def next_sand_gen(self):
        rows, cols = len(self.matrix), len(self.matrix[0])
        for x in range(rows):
            for y in range(cols):
                if self.matrix[x][y] == BiomesType.SEA:
                    if self.count_neighbors(x, y, BiomesType.SAND) >= 5 and random.randint(1,50)==1:
                        self.matrix[x][y] = BiomesType.SAND
                        self.paint_pixel_element(BiomesType.SAND, x, y)
        self.pg.display.update()

    # -------------------- SEA SHORE --------------------
    def set_layout_sea_shore(self):
        self.start_border(BiomesType.SEA, BiomesType.SAND, BiomesType.SEA_SHORE, 1)
        for _ in range(50):
            self.next_sea_shore_gen()

    def next_sea_shore_gen(self):
        rows, cols = len(self.matrix), len(self.matrix[0])
        for x in range(rows):
            for y in range(cols):
                if self.matrix[x][y] == BiomesType.SEA:
                    if self.count_neighbors(x, y, BiomesType.SEA_SHORE) >= 4 and random.randint(1,30)==1:
                        self.matrix[x][y] = BiomesType.SEA_SHORE
                        self.paint_pixel_element(BiomesType.SEA_SHORE, x, y)
        self.pg.display.update()

    # -------------------- WOODS --------------------
    def set_layout_woods(self):
        self.start_random_woods()
        for _ in range(20):
            self.next_generation(BiomesType.LAND, BiomesType.WOODS, [3,6,7,8])
            self.next_generation(BiomesType.WOODS, BiomesType.LAND, [3,6,7,8])

    def start_random_woods(self):
        rows, cols = len(self.matrix), len(self.matrix[0])
        for x in range(rows):
            for y in range(cols):
                if self.matrix[x][y] == BiomesType.LAND and random.randint(1,2)==1:
                    self.matrix[x][y] = BiomesType.WOODS
                    self.paint_pixel_element(BiomesType.WOODS, x, y)

    # -------------------- UTILS --------------------
    def create_start_matrix(self):
        rows, cols = settings.Rows, settings.Columns
        matrix = [[BiomesType.SEA if random.randint(1,2)==1 else BiomesType.LAND
                   for _ in range(cols)] for _ in range(rows)]
        for i in range(rows):
            for j in range(cols):
                self.paint_pixel_element(matrix[i][j], i, j)
        self.pg.display.update()
        return matrix

    def paint_pixel_element(self, biome, x, y):
        color = {
            BiomesType.LAND: settings.COLOR_LAND,
            BiomesType.SEA: settings.COLOR_SEA,
            BiomesType.SAND: settings.COLOR_SAND,
            BiomesType.SEA_SHORE: settings.COLOR_SEA_SHORE,
            BiomesType.WOODS: settings.COLOR_WOODS
        }[biome]
        self.pg.draw.rect(self.app.screen, color,
                          (x*settings.basicX, y*settings.basicY, settings.basicX, settings.basicY))
