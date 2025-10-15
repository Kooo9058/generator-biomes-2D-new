# Introduction

Hello everyone! I was inspired to write this article by the YouTube channel author [PeaAshMeter](https://www.youtube.com/@peaashmeter). In his video, the author demonstrates a simple 2D world generator based on a basic cellular automaton rule. What is a cellular automaton? What types of cellular automata exist? I will try to answer these and many other questions.

I decided to write the project in Python, but since I am not an expert in this field, any comments, suggestions for improving the code or the project are welcome!

![1](https://github.com/Kooo9058/generator-biomes-2D-new/blob/tools/res/1.jpg)


## 1. What is a Cellular Automaton?

A cellular automaton is a set of cells that can be represented as a matrix with 
x
x rows and 
y
y columns. The intersection of 
x
x and 
y
y gives the coordinates of the current cell. Each cell can have different states. The simplest cellular automata can only have two states: filled (1) or empty (0).




For each cell, a neighborhood is defined — the cells surrounding the current one. The radius of this neighborhood can vary in different automata, as can the rules about which neighbors to consider (for example, only the left and right neighbors, or only the top and bottom neighbors).

This neighborhood is needed so that the state of the current cell can be updated based on the states of its neighbors at each iteration. The state changes according to specific rules. For example, if the current cell is empty (0), but there are 3 or more filled (1) neighbors in its neighborhood, then the current cell becomes filled (1).

![2](https://github.com/Kooo9058/generator-biomes-2D-new/blob/tools/res/2.png)


One step of a cellular automaton involves going through all the cells and, based on the current state of each cell and its neighborhood, determining the new state the cell will have in the next step. Before starting the automaton, the initial state of the cells is defined, which can be set deliberately or randomly. A set of such simple rules can create astonishing animations — here is one such example.

![3](https://github.com/Kooo9058/generator-biomes-2D-new/blob/tools/res/3.gif)

## 2. Chaotic Distribution as the Initial State

For this project, we will use PyGame — why exactly PyGame will be explained at the end of the article, but for now, let's accept it as a given. We will sketch the basic structure of a PyGame application. In the initialization of the App class, we define the window resolution, a timer for frame updates, and the Biomes class, which will contain all the logic for working with biomes. In the run method, we will handle button listeners and display the FPS counter.

We also need to create a settings file, where we will store constants for the project. Using this file, we can easily change project settings, such as the frame rate limit or the base window resolution.

```python
class App:
    def __init__(self):
        self.screen = pg.display.set_mode(settings.RES)
        self.clock = pg.time.Clock()
        self.biomes = bm.Biomes(app=self, pg=pg)

    def run(self):
        while True:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    pg.quit()
                elif event.type == pg.KEYDOWN:
                    if event.key == pg.K_SPACE:
                        self.biomes.main_render_biomes()

            self.clock.tick(settings.FPS)
            pg.display.set_caption(f'FPS: {self.clock.get_fps()}')


if __name__ == '__main__':
    app = App()
    app.run()

```

Now that the basic class is ready, let's move on to rendering frames. The first frame will display a chaotic distribution of land and sea. For this, we will use a matrix that will be filled randomly. To fill such a matrix, we need biome types, so we cannot do without an enum, where we will define the main biomes we will work with.

We will have a total of five biomes: land, sea, sand, shore, and forest.

```python
class BiomesType(Enum):
    SEA = 0
    LAND = 1
    SAND = 2
    SEA_SHORE = 3
    WOODS = 4
```

Now let's create a method that will initialize the matrix with a random distribution of land and sea, with a 50% probability for each. It’s also worth noting that the number of columns and rows will be 300. Thus, with a resolution of 600 by 600 pixels, each “biome pixel” will be 2 by 2 real pixels in size. This needs to be taken into account when rendering the actual pixels, since their position will be offset by the size of the “biome pixel.”

```python 
    def create_start_matrix(self):
        rows, cols = settings.Rows, settings.Columns
        matrix = [[BiomesType.SEA if random.randint(1,2)==1 else BiomesType.LAND
                   for _ in range(cols)] for _ in range(rows)]
        for i in range(rows):
            for j in range(cols):
                self.paint_pixel_element(matrix[i][j], i, j)
        self.pg.display.update()
        return matrix



```

Now a few words about rendering. After initializing each element of the matrix, we immediately draw it on the canvas. This is handled by the paint_pixel_element method, which takes the type of the current biome and its coordinates. Based on the biome type, it sets the color and draws the element, taking into account the actual pixel size and its offset.

```python 
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

```

After creating the matrix and rendering each element, we need to call the display.update() method to refresh the current canvas, and we will see the random distribution.

![4](https://github.com/Kooo9058/generator-biomes-2D-new/blob/tools/res/4.jpg)

## 3. Order from Chaos

To create organized groups of cells that resemble islands, we need to apply one of the cellular automaton rules. In this project, we will use the "Day and Night" rule (B3678/S34678). It is important to note that the new state of the entire matrix after applying the rule is called a generation. With each generation, the random distribution becomes more structured, so the number of generations can vary.

Now, let's create the first layer. For this, we need to iterate through the generated matrix and count the neighbors for each cell, taking care to include the corners to avoid going out of matrix bounds. If the current cell is land and the number of neighboring sea cells is 3, 6, 7, or 8, we change the current cell to sea, and vice versa for sea cells. The neighbor radius is considered to be 1 cell. This can be illustrated as follows.

![5](https://github.com/Kooo9058/generator-biomes-2D-new/blob/tools/res/5.jpg)

```python 
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

```

After approximately 200 generations, we can observe that our noise now resembles an archipelago of islands. I think this result is quite satisfactory, so we can move on to working on the next layer.

![6](https://github.com/Kooo9058/generator-biomes-2D-new/blob/tools/res/6.jpg)

## 4. Beach and Shallow Water

The next step is to create a sandy shore around each island. Essentially, we just need to outline each island, which is quite straightforward. For each cell, we check the following condition: if the current cell is land and it is adjacent to both sea and land cells, then we change it to sand.

![7](https://github.com/Kooo9058/generator-biomes-2D-new/blob/tools/res/7.jpg)

However, it should be noted that a simple sandy outline around the islands doesn’t look very natural, so we need to add a random effect for transforming land into sand. We will use the old rule for shaping land, but modify it: if the current cell has more than 5 neighboring sand cells, then with a 2% probability we will change the current cell to sand. After 100 generations, we get the following result.

![8](https://github.com/Kooo9058/generator-biomes-2D-new/blob/tools/res/8.jpg)

The formation of shallow water follows the same principle, the only difference being that now we check if the cell is between sand and sea. We outline the contour in the same way, and then add a 2% random distribution.

![9](https://github.com/Kooo9058/generator-biomes-2D-new/blob/tools/res/9.jpg)

As a result, after 100 generations, we obtain the shallow water.

![10](https://github.com/Kooo9058/generator-biomes-2D-new/blob/tools/res/10.jpg)
## 5. Forest

The final layer will be a dense forest. First, we need to create a random distribution, which we will then organize using the same “Day and Night” rule (B3678/S34678). So, the process of creating the forest is similar to the first layer (land and sea). The main difference is that the distribution will be confined to the islands, meaning it will only occur on land cells.

![11](https://github.com/Kooo9058/generator-biomes-2D-new/blob/tools/res/11.jpg)

Fewer generations are required to render the forest, approximately 30. This is because, due to the boundary conditions, the number of cells available for the forest is much smaller, so fewer generations are needed for clustering.

![12](https://github.com/Kooo9058/generator-biomes-2D-new/blob/tools/res/12.jpg)


![generator_biomes](https://github.com/Kooo9058/generator-biomes-2D-new/blob/main/res/generator_biomes.gif)
