import time
import settings
import random
from biomes_type import BiomesType


class Biomes:
    matrix = [], []

    def __init__(self, app, pg):
        self.app = app
        self.pg = pg
        self.matrix = self.create_start_matrix()

    def main_render_biomes(self):
        start = time.gmtime().tm_sec
        self.set_layout_lands_and_sea()
        self.set_layout_sands()
        self.set_layout_sea_shore()
        self.set_layout_woods()
        end = time.gmtime().tm_sec
        print(f'Render Time is {end - start}')

    def set_layout_lands_and_sea(self):
        self.set_start_random_lands_and_sea()
        self.next_lands_sea_count()

    def set_start_random_lands_and_sea(self):
        self.matrix = self.create_start_matrix()
        for x in range(len(self.matrix)):
            for y in range(len(self.matrix[x])):
                self.paint_pixel_element(self.matrix[x][y], x, y)
        self.pg.display.update()

    def next_lands_sea_count(self):
        for r in range(settings.COUNTS_ALGORITHMS):
            self.next_generation(BiomesType.LAND, BiomesType.SEA, rules=[3, 6, 7, 8])
            self.next_generation(BiomesType.SEA, BiomesType.LAND, rules=[3, 6, 7, 8])

    def count_neighbors(self, x, y, biome_type):
        count = 0
        rows = len(self.matrix)
        cols = len(self.matrix[0])
        for dx in [-1, 0, 1]:
            for dy in [-1, 0, 1]:
                if dx == 0 and dy == 0:
                    continue
                nx, ny = x + dx, y + dy
                if 0 <= nx < rows and 0 <= ny < cols:
                    if self.matrix[nx][ny] == biome_type:
                        count += 1
        return count

    def next_generation(self, target_biome, new_biome, rules):
        rows = len(self.matrix)
        cols = len(self.matrix[0])
        for x in range(rows):
            for y in range(cols):
                neighbors = self.count_neighbors(x, y, new_biome)
                if self.matrix[x][y] == target_biome and neighbors in rules:
                    self.matrix[x][y] = new_biome
                    self.paint_pixel_element(new_biome, x, y)




    # def next_generation_lands(self):
    #     for x in range(len(self.matrix)):
    #         for y in range(len(self.matrix[x])):
    #             counter_sea = 0
    #             counter_land = 0
    #
    #             if (x - 1) >= 0:
    #                 if self.matrix[x - 1][y] == BiomesType.SEA:
    #                     counter_sea += 1
    #                 else:
    #                     counter_land += 1
    #
    #             if (y - 1) >= 0:
    #                 if self.matrix[x][y - 1] == BiomesType.SEA:
    #                     counter_sea += 1
    #                 else:
    #                     counter_land += 1
    #
    #             if (x + 1) <= 99:
    #                 if self.matrix[x + 1][y] == BiomesType.SEA:
    #                     counter_sea += 1
    #                 else:
    #                     counter_land += 1
    #
    #             if (y + 1) <= 99:
    #                 if self.matrix[x][y + 1] == BiomesType.SEA:
    #                     counter_sea += 1
    #                 else:
    #                     counter_land += 1
    #
    #             if (y - 1) >= 0 and (x + 1) <= 99:
    #                 if self.matrix[x + 1][y - 1] == BiomesType.SEA:
    #                     counter_sea += 1
    #                 else:
    #                     counter_land += 1
    #
    #             if (y + 1) <= 99 and (x + 1) <= 99:
    #                 if self.matrix[x + 1][y + 1] == BiomesType.SEA:
    #                     counter_sea += 1
    #                 else:
    #                     counter_land += 1
    #
    #             if (y - 1) >= 0 and (x - 1) >= 0:
    #                 if self.matrix[x - 1][y - 1] == BiomesType.SEA:
    #                     counter_sea += 1
    #                 else:
    #                     counter_land += 1
    #
    #             if (y + 1) <= 99 and (x - 1) >= 0:
    #                 if self.matrix[x - 1][y + 1] == BiomesType.SEA:
    #                     counter_sea += 1
    #                 else:
    #                     counter_land += 1
    #
    #             if self.matrix[x][y] == BiomesType.LAND:
    #                 if counter_sea == 3 or counter_sea == 6 \
    #                         or counter_sea == 7 or counter_sea == 8:
    #                     self.matrix[x][y] = BiomesType.SEA
    #                     self.paint_pixel_element(self.matrix[x][y], x, y)
    #
    #             if self.matrix[x][y] == BiomesType.SEA:
    #                 if counter_land == 3 or counter_land == 6 \
    #                         or counter_land == 7 or counter_land == 8:
    #                     self.matrix[x][y] = BiomesType.LAND
    #                     self.paint_pixel_element(self.matrix[x][y], x, y)
    #     self.pg.display.update()

    def set_layout_sands(self):
        self.start_border_sands()
        for i in range(settings.COUNTS_ALGORITHMS_SANDS):
            self.next_sands_gen()

    def start_border_sands(self):
        for x in range(len(self.matrix)):
            for y in range(len(self.matrix[x])):
                counter_sea = 0

                if (x - 1) >= 0:
                    if self.matrix[x - 1][y] == BiomesType.SEA:
                        counter_sea += 1

                if (y - 1) >= 0:
                    if self.matrix[x][y - 1] == BiomesType.SEA:
                        counter_sea += 1

                if (x + 1) <= 99:
                    if self.matrix[x + 1][y] == BiomesType.SEA:
                        counter_sea += 1

                if (y + 1) <= 99:
                    if self.matrix[x][y + 1] == BiomesType.SEA:
                        counter_sea += 1

                if (y - 1) >= 0 and (x + 1) <= 99:
                    if self.matrix[x + 1][y - 1] == BiomesType.SEA:
                        counter_sea += 1

                if (y + 1) <= 99 and (x + 1) <= 99:
                    if self.matrix[x + 1][y + 1] == BiomesType.SEA:
                        counter_sea += 1

                if (y - 1) >= 0 and (x - 1) >= 0:
                    if self.matrix[x - 1][y - 1] == BiomesType.SEA:
                        counter_sea += 1

                if (y + 1) <= 99 and (x - 1) >= 0:
                    if self.matrix[x - 1][y + 1] == BiomesType.SEA:
                        counter_sea += 1

                if self.matrix[x][y] == BiomesType.LAND:
                    if counter_sea >= 1:
                        self.matrix[x][y] = BiomesType.SAND
                        self.paint_pixel_element(self.matrix[x][y], x, y)
        self.pg.display.update()

    def next_sands_gen(self):
        for x in range(len(self.matrix)):
            for y in range(len(self.matrix[x])):
                counter_sands = 0

                if (x - 1) >= 0:
                    if self.matrix[x - 1][y] == BiomesType.SAND:
                        counter_sands += 1

                if (y - 1) >= 0:
                    if self.matrix[x][y - 1] == BiomesType.SAND:
                        counter_sands += 1

                if (x + 1) <= 99:
                    if self.matrix[x + 1][y] == BiomesType.SAND:
                        counter_sands += 1

                if (y + 1) <= 99:
                    if self.matrix[x][y + 1] == BiomesType.SAND:
                        counter_sands += 1

                if (y - 1) >= 0 and (x + 1) <= 99:
                    if self.matrix[x + 1][y - 1] == BiomesType.SAND:
                        counter_sands += 1

                if (y + 1) <= 99 and (x + 1) <= 99:
                    if self.matrix[x + 1][y + 1] == BiomesType.SAND:
                        counter_sands += 1

                if (y - 1) >= 0 and (x - 1) >= 0:
                    if self.matrix[x - 1][y - 1] == BiomesType.SEA:
                        counter_sands += 1

                if (y + 1) <= 99 and (x - 1) >= 0:
                    if self.matrix[x - 1][y + 1] == BiomesType.SAND:
                        counter_sands += 1

                if self.matrix[x][y] == BiomesType.SEA:
                    if counter_sands >= 5:
                        r = random.randint(0, 50)
                        if r == 1:
                            self.matrix[x][y] = BiomesType.SAND
                            self.paint_pixel_element(self.matrix[x][y], x, y)
        self.pg.display.update()

    def paint_pixel_element(self, biome, x, y):
        if biome == BiomesType.LAND:
            color = settings.COLOR_LAND
        elif biome == BiomesType.SEA:
            color = settings.COLOR_SEA
        elif biome == BiomesType.SAND:
            color = settings.COLOR_SAND
        elif biome == BiomesType.SEA_SHORE:
            color = settings.COLOR_SEA_SHORE
        elif biome == BiomesType.WOODS:
            color = settings.COLOR_WOODS
        self.pg.draw.rect(self.app.screen, color,
                          (x * settings.basicX, y * settings.basicY, settings.basicX, settings.basicY))

    def start_border_sea_shore(self):
        for x in range(len(self.matrix)):
            for y in range(len(self.matrix[x])):
                counter_sands = 0

                if (x - 1) >= 0:
                    if self.matrix[x - 1][y] == BiomesType.SAND:
                        counter_sands += 1

                if (y - 1) >= 0:
                    if self.matrix[x][y - 1] == BiomesType.SAND:
                        counter_sands += 1

                if (x + 1) <= 99:
                    if self.matrix[x + 1][y] == BiomesType.SAND:
                        counter_sands += 1

                if (y + 1) <= 99:
                    if self.matrix[x][y + 1] == BiomesType.SAND:
                        counter_sands += 1

                if (y - 1) >= 0 and (x + 1) <= 99:
                    if self.matrix[x + 1][y - 1] == BiomesType.SAND:
                        counter_sands += 1

                if (y + 1) <= 99 and (x + 1) <= 99:
                    if self.matrix[x + 1][y + 1] == BiomesType.SAND:
                        counter_sands += 1

                if (y - 1) >= 0 and (x - 1) >= 0:
                    if self.matrix[x - 1][y - 1] == BiomesType.SAND:
                        counter_sands += 1

                if (y + 1) <= 99 and (x - 1) >= 0:
                    if self.matrix[x - 1][y + 1] == BiomesType.SAND:
                        counter_sands += 1

                if self.matrix[x][y] == BiomesType.SEA:
                    if counter_sands >= 1:
                        self.matrix[x][y] = BiomesType.SEA_SHORE
                        self.paint_pixel_element(self.matrix[x][y], x, y)
        self.pg.display.update()

    def next_sea_shore_gen(self):
        for x in range(len(self.matrix)):
            for y in range(len(self.matrix[x])):
                counter_sea_shore = 0

                if (x - 1) >= 0:
                    if self.matrix[x - 1][y] == BiomesType.SEA_SHORE:
                        counter_sea_shore += 1

                if (y - 1) >= 0:
                    if self.matrix[x][y - 1] == BiomesType.SEA_SHORE:
                        counter_sea_shore += 1

                if (x + 1) <= 99:
                    if self.matrix[x + 1][y] == BiomesType.SEA_SHORE:
                        counter_sea_shore += 1

                if (y + 1) <= 99:
                    if self.matrix[x][y + 1] == BiomesType.SEA_SHORE:
                        counter_sea_shore += 1

                if (y - 1) >= 0 and (x + 1) <= 99:
                    if self.matrix[x + 1][y - 1] == BiomesType.SEA_SHORE:
                        counter_sea_shore += 1

                if (y + 1) <= 99 and (x + 1) <= 99:
                    if self.matrix[x + 1][y + 1] == BiomesType.SEA_SHORE:
                        counter_sea_shore += 1

                if (y - 1) >= 0 and (x - 1) >= 0:
                    if self.matrix[x - 1][y - 1] == BiomesType.SEA_SHORE:
                        counter_sea_shore += 1

                if (y + 1) <= 99 and (x - 1) >= 0:
                    if self.matrix[x - 1][y + 1] == BiomesType.SEA_SHORE:
                        counter_sea_shore += 1

                if self.matrix[x][y] == BiomesType.SEA:
                    if counter_sea_shore >= 4:
                        r = random.randint(0, 30)
                        if r == 1:
                            self.matrix[x][y] = BiomesType.SEA_SHORE
                            self.paint_pixel_element(self.matrix[x][y], x, y)
        self.pg.display.update()

    def set_layout_sea_shore(self):
        self.start_border_sea_shore()
        for i in range(50):
            self.next_sea_shore_gen()

    def start_random_woods(self):
        for x in range(len(self.matrix)):
            for y in range(len(self.matrix[x])):
                if self.matrix[x][y] == BiomesType.LAND:
                    r = random.randint(1, 2)
                    if r == 1:
                        self.matrix[x][y] = BiomesType.WOODS
                        self.paint_pixel_element(self.matrix[x][y], x, y)

    def next_woods_gen(self):
        for x in range(len(self.matrix)):
            for y in range(len(self.matrix[x])):
                counter_land = 0
                counter_woods = 0

                if (x - 1) >= 0:
                    if self.matrix[x - 1][y] == BiomesType.LAND:
                        counter_land += 1
                    else:
                        counter_woods += 1

                if (y - 1) >= 0:
                    if self.matrix[x][y - 1] == BiomesType.LAND:
                        counter_land += 1
                    else:
                        counter_woods += 1

                if (x + 1) <= 99:
                    if self.matrix[x + 1][y] == BiomesType.LAND:
                        counter_land += 1
                    else:
                        counter_woods += 1

                if (y + 1) <= 99:
                    if self.matrix[x][y + 1] == BiomesType.LAND:
                        counter_land += 1
                    else:
                        counter_woods += 1

                if (y - 1) >= 0 and (x + 1) <= 99:
                    if self.matrix[x + 1][y - 1] == BiomesType.LAND:
                        counter_land += 1
                    else:
                        counter_woods += 1

                if (y + 1) <= 99 and (x + 1) <= 99:
                    if self.matrix[x + 1][y + 1] == BiomesType.LAND:
                        counter_land += 1
                    else:
                        counter_woods += 1

                if (y - 1) >= 0 and (x - 1) >= 0:
                    if self.matrix[x - 1][y - 1] == BiomesType.LAND:
                        counter_land += 1
                    else:
                        counter_woods += 1

                if (y + 1) <= 99 and (x - 1) >= 0:
                    if self.matrix[x - 1][y + 1] == BiomesType.LAND:
                        counter_land += 1
                    else:
                        counter_woods += 1

                if self.matrix[x][y] == BiomesType.LAND:
                    if counter_woods == 3 or counter_woods == 6 \
                            or counter_woods == 7 or counter_woods == 8:
                        self.matrix[x][y] = BiomesType.WOODS
                        self.paint_pixel_element(self.matrix[x][y], x, y)

                if self.matrix[x][y] == BiomesType.WOODS:
                    if counter_land == 3 or counter_land == 6 \
                            or counter_land == 7 or counter_land == 8:
                        self.matrix[x][y] = BiomesType.LAND
                        self.paint_pixel_element(self.matrix[x][y], x, y)
        self.pg.display.update()

    def set_layout_woods(self):
        self.start_random_woods()
        for _ in range(20):
            self.next_woods_gen()

    def create_start_matrix(self):
        rows = settings.Rows
        cols = settings.Columns
        matrix = [[0] * cols for _ in range(rows)]

        for i in range(rows):
            for j in range(cols):
                r = random.randint(1, 2)
                matrix[i][j] = BiomesType.SEA if (r == 1) else BiomesType.LAND
                self.paint_pixel_element(matrix[i][j], i, j)
        self.pg.display.update()

        return matrix
