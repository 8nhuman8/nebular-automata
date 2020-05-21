# Nebular automata
A program for visualizing an interesting mathematical idea.

## Idea
>The original idea was found [here](https://vk.com/math_dosug?w=wall-149993556_46382), and the author is this [person](https://vk.com/id504076319).

Let a square be surrounded on each side by a new square of the same size with a chance of **q**. Newly formed squares reproduce other squares and so on, to infinity.  
We will limit the growth of the population by setting a certain maximum allowable number of squares, upon reaching which the program will be completed.

As you probably noticed when looking at the images below, the edges of the shapes are more duller then its centre and, conversely, the center of the shape is duller than its edges on in some images. The fact is that with each generation, squares are created more white or more 'colored' specifically so that the process of structure development is visualized.

## Remarks
With **q** tending to **1**, the structure becomes more and more like a *rhombus*, that is not really surprising.  
If the **q** is less than **0.5**, then the structure is *unlikely to grow*.  
If **q** approximately equal to **0.5**, the structure is *complete chaos*.  
With **q** approximately equal to **0.6**, the structure resembles a *circle*.  
If **q** is in **\[0.7, 1)**, the the structure looks like a *convex rhombus*.  
If **q** is equals to **1**, the structure becomes a *rhombus*.

## Usage
1. Upgrade required packages with `pip install -r requirements.txt --upgrade` (if you don't have one, it will be automatically installed).
2. Open the folder with the scripts.
3. Check out all the command-line parameters.
4. Run the `main.py` with `python main.py --help` and read the description with all the parameters.
5. Run the `main.py` again with the parameters you need.
6. Enjoy the beauty.

## Command-line arguments description
```
usage: main.py [-h] [-rc FLOAT] [-mc INT] [-ca1 R G B A] [-cb R G B A] [-m]
               [-ca2 R G B A] [-fp FLOAT] [-fi] [-s] [-p PATH]
               width height

Creates a beautiful nebula. Percentages show the duration of further program
execution in ideal conditions! In fact, probability can take its toll.

optional arguments:
  -h, --help            show this help message and exit

Required options:
  width                 The width of the image.
  height                The height of the image.

Basic options:
  -rc FLOAT, --reproduce-chance FLOAT
                        The chance the square can produce other squares.
  -mc INT, --max-count INT
                        The maximum number of squares in the image. By
                        default, this is half of all pixels in the future
                        image.
  -ca1 R G B A, --color-accent1 R G B A
                        The first or (primary if multicolor mode is not
                        enabled) color of squares. Color components must be
                        specified between 0 and 255. The The default color is
                        aqua
  -cb R G B A, --color-background R G B A
                        The background color. Color components must be
                        specified between 0 and 255. The default color is
                        white.

Multicoloring options:
  -m, --multicolor      Enables multicolor mode.
  -ca2 R G B A, --color-accent2 R G B A
                        The second color of squares if multicolor mode is
                        enabled. Color components must be specified between 0
                        and 255. The The default color is (r, g, b): (255, 29,
                        119, 255).

Additional options:
  -fp FLOAT, --find-percent FLOAT
                        The program will work until a nebula is filled with a
                        certain percentage.
  -fi, --fade-in        The original color is white. The color of each new
                        generation will fade into the specified color.

Saving options:
  -s, --save            The generated image will be saved in the root if no
                        path is specified.
  -p PATH, --path PATH  The path by which the generated image will be saved.
                        Write the path without quotes, separating the
                        directories with the usual single slash.
```

## Gallery (images created by this program)
![](gallery/1.png)
![](gallery/2.png)
![](gallery/3.png)
![](gallery/4.png)
![](gallery/5.png)
![](gallery/6.png)
![](gallery/7.png)
![](gallery/8.png)

## License
[Nebular automata](https://github.com/8nhuman8/nebular-automata) specific code is distributed under [MIT License](LICENSE).

Copyright (c) 2020 Artyom Bezmenov
