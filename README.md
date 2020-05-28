# Nebular Automata
A program for visualizing an interesting mathematical idea.

## Table of contents
- [Idea](#idea)
- [Some remarks](#some-remarks)
- [Usage](#usage)
  + [Installation](#installation)
  + [Usage of renderer](#usage-of-renderer-rendererpy)
  + [Usage of Telegram bot](#usage-of-telegram-bot-telegram_botpy)
  + [Some remarks on usage of Telegram bot](#some-remarks-on-usage-of-telegram-bot)
  + [Usage of scheduler](#usage-of-scheduler-schedulerpy)
- [Command-line arguments description](#command-line-arguments-description)
- [License](#license)
- [Gallery](#gallery-images-created-by-this-program)

## Idea
>The original idea was found [here](https://vk.com/math_dosug?w=wall-149993556_46382), and the author is this [person](https://vk.com/id504076319).

Let a square be surrounded on each side by a new square of the same size with a chance of **q**. Newly formed squares reproduce other squares and so on, to infinity.  
We will limit the growth of the population by setting a certain maximum allowable number of squares, upon reaching which the program will be completed.

As you probably noticed when looking at the images [below](#gallery-images-created-by-this-program), the edges of the shapes have a different color, into which the initial color smoothly flows. This was done not only to illustrate the process of structure development, but also for greater saturation and prettiness of images.

## Some remarks
With **q** tending to **1**, the structure becomes more and more like a *rhombus*, that is not really surprising.  
If the **q** is less than **0.5**, then the structure is *unlikely to grow*.  
If **q** approximately equal to **0.5**, the structure is *complete chaos*.  
With **q** approximately equal to **0.6**, the structure resembles a *circle*.  
If **q** is in **\[0.7, 1)**, the the structure looks like a *convex rhombus*.  
If **q** is equals to **1**, the structure becomes a *rhombus*.

In fact, we can also generate squares if we surround each square not only on each side, but also on each corner. Therefore, I added an additional `--quadratic` parameter to generate squares.

## Usage

### Installation
Upgrade required packages with `pip install -r requirements.txt --upgrade` (if you don't have one, it will be automatically installed).

### Usage of renderer ([`renderer.py`](scripts/renderer.py))
1. Check out all the command-line parameters [below](#command-line-arguments-description).
2. Then you can specify the colors you need in the [`colors_config.json`](configs/colors_config.json).  
   You can use only one color if you want, like this:
   ```json
   {
     "1": [255, 0, 0, 255]
   }
   ```
3. Run the `renderer.py` with `python scripts/renderer.py [parameters you need]`.
4. Enjoy the beauty.

### Usage of Telegram bot ([`telegram_bot.py`](scripts/telegram_bot.py))
1. Check out all the command-line parameters [below](#command-line-arguments-description).
2. Add all the required information to the [`bot_config.json`](configs/bot_config.json):

    1) Add your Telegram bot `token`.
    2) Add `chat_id` of your channel or chat. You can get it quickly by following my [gist](https://gist.github.com/8nhuman8/25f98c5e4b33d47a54cd510da221f309).
    3) Also set the image size.
    4) After that, you can choose to use arguments from the [`bot_config.json`](configs/bot_config.json) or enter them in the console. The difference is that using the [`bot_config.json`](configs/bot_config.json), you can specify random values of various arguments.
    5) If you chose not to use the [`bot_config.json`](configs/bot_config.json), go to step 3. If not, read on.
    6) After that, you can set the values for different parameters in the `"args"` section:
       * For `--reproduce-chance`, `--min-percent`, `--max-percent`, `--max-count` and `--colors-number` arguments, you can specify either a specific value or an interval by specifying the `"start"` and `"end"` values. If you chose the second option, the value will be determined randomly and will lie in the interval:  
         **start <= value <= end**  
         If you don't want to use these parameters, then fill them with `null` values. If you fill `--reproduce-chance` parameter with `null` values, then by default it will be randomly determined in the range from **0.5** to **1**, including the final values.
       * `--color-background` argument isn't used by default. The default background color is white, but if you want to set your own, enter the value as RGBA like this:
         ```json
         "--color-background": {
             "value": [255, 128, 64, 255],
             "random": false
         }
         ```
         If you want a random background color, then fill it like this:
         ```json
         "--color-background": {
             "value": null,
             "random": true
         }
         ```
       * `--opaque`, `--random-colors`, `--fade-in` and `--quadratic` parameters are flag parameters. Their JSON represantion consists of two values: `"value"` and `"random"`:

         If you want to use some of these parameters, then just set the `"value"` to `true`, and `"random"` to `false` like this:
         ```json
         "--quadratic": {
             "value": true,
             "random": false
         }

         ```
         If you don't want to use some of these parameters, then just set both values to `false` like this:
         ```json
         "--fade-in": {
             "value": false,
             "random": false
         }

         ```
         If you want to get the value randomly, then specify it like this:
         ```json
         "--opaque": {
             "value": null,
             "random": true
         }
         ```

3.  * if you made `"use_config_args": true` in [`bot_config.json`](configs/bot_config.json): Run the [`telegram_bot.py`](scripts/telegram_bot.py) with `python scripts/telegram_bot.py`.
    * if you made `"use_config_args": false` in [`bot_config.json`](configs/bot_config.json): Run the [`telegram_bot.py`](scripts/telegram_bot.py) with `python scripts/telegram_bot.py [parameters you need]`.

### Some remarks on usage of Telegram bot
Most likely you will need a VPN to use the Telegram bot if you live in a country where Telegram is forbidden.  
I recommend using this [VPN](https://windscribe.com).

If you made `"use_config_args": false` in [`bot_config.json`](configs/bot_config.json), you don't have to write `--save` and `--path PATH` parameters, because all generated images are automatically saved in ['telegram_images'](telegram_images/) folder.  
But if you want to use another folder, then create it and change the `TELEGRAM_IMAGES_SAVE_PATH` constant variable in [`constants.py`](scripts/constants.py).

You can disable `"use_caption"` option in [`bot_config.json`](configs/bot_config.json) to remove the attachment of text to the message with the image:
```json
"use_caption": false
```

### Usage of scheduler ([`scheduler.py`](scripts/scheduler.py))
1. Check out all the command-line parameters [below](#command-line-arguments-description).
2. Add all the necessary information to the [`scheduler_config.json`](configs/scheduler_config.json).

   You can also specify the starting date and ending dates for the schedule through the `"start_date"` and `"end_date"` parameters, respectively. They can be given as a date/datetime object or text (in the [ISO 8601](https://en.wikipedia.org/wiki/ISO_8601) format) like this:
   ```json
   "start_date": "2010-10-10 09:30:00",
   "end_time": "2014-06-15 11:00:00"
   ```

   If the start date is in the past, the trigger will not fire many times retroactively but instead calculates the next run time from the current time, based on the past start time.
3. Run the [`scheduler.py`](scripts/scheduler.py) with `python scripts/scheduler.py`.

## Command-line arguments description
```
usage: renderer.py [-h] [-rc FLOAT] [-mc INT] [-cb R G B A] [-r] [-cn INT]
                   [-o] [-minp FLOAT] [-maxp FLOAT] [-fi] [-q] [-s] [-p PATH]
                   [-dsi]
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
  -cb R G B A, --color-background R G B A
                        The background color. Color components must be
                        specified between 0 and 255. The default color is
                        white.

Multicoloring options:
  -r, --random-colors   Accent colors will be random.
  -cn INT, --colors-number INT
                        How many colors will be used. By default it is 3.Must
                        be used with '--random-colors' argument.
  -o, --opaque          All colors will be opaque.

Additional options:
  -minp FLOAT, --min-percent FLOAT
                        The program will work until nebula is filled with a
                        certain or greater percentage.
  -maxp FLOAT, --max-percent FLOAT
                        The program will work until a nebula is filled with a
                        certain percentage.
  -fi, --fade-in        The original color is white. The color of each new
                        generation will fade into the specified color.
  -q, --quadratic       Each square will be surrounded not only on each side,
                        but also on each corner.

System options:
  -s, --save            The generated image will be saved in the root if no
                        path is specified.
  -p PATH, --path PATH  The path by which the generated image will be saved.
                        Write the path without quotes, separating the
                        directories with the usual single slash.
  -dsi, --dont-show-image
                        Do not show image after execution.
```

## License
[Nebular automata](https://github.com/8nhuman8/nebular-automata) specific code is distributed under [MIT License](LICENSE).

Copyright (c) 2020 Artyom Bezmenov

## Gallery (images created by this program)
![image](https://drive.google.com/uc?export=view&id=1uHiTEOzHjKPS_fwKw05yp6G_B-WX-E9s)
![image](https://drive.google.com/uc?export=view&id=1fvZI5PkLAnNyNuqH0zwgaL-l3yGE9OxM)
![image](https://drive.google.com/uc?export=view&id=1wzVJ0a0NjcfPfVmDeJGFNm_kPFSKgCHJ)
![image](https://drive.google.com/uc?export=view&id=1U4M18HZInwcQbHyuN5oyRzblt6Ifm3NI)
![image](https://drive.google.com/uc?export=view&id=17vrGlyRD2-pmINee2eazcEZAMkF17qy7)
![image](https://drive.google.com/uc?export=view&id=1X5PmU0xByuFS7ggEp-B4OxC60KP8Pfar)
![image](https://drive.google.com/uc?export=view&id=1lBtR4y3Tt_a5HDAhZvpyB8guR6JOaLyv)
![image](https://drive.google.com/uc?export=view&id=1WLj6Edg2s8t0EfVNzoFrGEL-5TVJyu6B)
![image](https://drive.google.com/uc?export=view&id=1l3lJUd3R4BlDRuH0nYplGRER33r1TlaO)
![image](https://drive.google.com/uc?export=view&id=1OmfTEnE_D8fpYVNvCjGxYf2lsQ8xTv3Q)
![image](https://drive.google.com/uc?export=view&id=1l44iF1TMVQxt8sQypGAUPAyydajtevvJ)
![image](https://drive.google.com/uc?export=view&id=1dB6E71E7wE0104B9UqQXTvE1MgZEKE0_)
![image](https://drive.google.com/uc?export=view&id=1d1QgMGkfMXWmJNq9CsMznDzSxJ9kwQCJ)
![image](https://drive.google.com/uc?export=view&id=1gVJ8vbVrI3wiq4YUaTgrWB9KNPt43wKl)
![image](https://drive.google.com/uc?export=view&id=1uMQy0YlbTMKpV1bz1piVpowUQGJqKbNe)
