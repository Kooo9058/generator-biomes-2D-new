
# A simple biomes on the map.

![1](https://github.com/Kooo9058/generator-biomes-2D-new/blob/main/res/1.jpg)

## How to use?
It's simple. Just build the project and press the space button on your keyboard.

To run the project, there is a Makefile.
Simply execute:

```
make install
```
and then:

```
make run
```
[More info](https://github.com/Kooo9058/generator-biomes-2D-new/blob/main/Makefile)
## How it works?

The project is based on the ["day and night" algorithm](https://ru.wikipedia.org/wiki/День_и_ночь_(клеточный_автомат)). The whole trick is that I apply it for each layer separately. In addition, I use event probability, which allows you to achieve a chaotic distribution of biomes, as it happens in real life.  

I explain in more detail how this works [here](https://github.com/Kooo9058/generator-biomes-2D-new/blob/main/HowIt'sWork.md).

## Custom chaos!
You can add more chaos with the settings. To do this, you can use the settings file. For example, you can change the number of biomes, or their size.

## P.S.
This project was inspired by [the author of this channel](https://github.com/peaashmeter).
After I wanted to repeat his idea.