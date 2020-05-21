from PIL import Image, ImageDraw
from argparse import ArgumentParser

from datetime import datetime
from time import sleep

from nebula import Nebula
from utils import Vector, Color, generate_filename, get_runtime, get_gradient


if __name__ == '__main__':
    description = ('Creates a beautiful nebula. Percentages show the duration '
                   'of further program execution in ideal conditions! In fact, '
                   'probability can take its toll.')
    help_reproduce_chance = 'The chance the square can produce other squares.'
    help_max_count = ('The maximum number of squares in the image. By '
                      'default, this is half of all pixels in the future image.')
    help_color_accent1 = ('The first or (primary if multicolor mode is not enabled) '
                          'color of squares. Color components must be specified '
                          'between 0 and 255. The The default color is aqua')
    help_color_background = ('The background color. Color components must be '
                             'specified between 0 and 255. The default color is white.')
    help_multicolor = 'Enables multicolor mode.'
    help_color_accent2 = ('The second color of squares if multicolor mode is '
                          'enabled. Color components must be specified between 0 '
                          'and 255. The The default color is (r, g, b): (255, 29, 119, 255).')
    help_find_percent = ('The program will work until a nebula '
                         'is filled with a certain percentage.')
    help_fade_in = ('The original color is white. The color of each '
                    'new generation will fade into the specified color.')
    help_save = 'The generated image will be saved in the root if no path is specified.'
    help_path = ("The path by which the generated image will be saved. Write the path "
                 "without quotes, separating the directories with the usual single slash.")
    colors_metavar = ('R', 'G', 'B', 'A')


    parser = ArgumentParser(description=description)

    group_required = parser.add_argument_group('Required options')
    group_required.add_argument('width', type=int, help='The width of the image.')
    group_required.add_argument('height', type=int, help='The height of the image.')

    group_basic = parser.add_argument_group('Basic options')
    group_basic.add_argument('-rc', '--reproduce-chance', metavar='FLOAT',
                             type=float, default=0.5, help=help_reproduce_chance)
    group_basic.add_argument('-mc', '--max-count', metavar='INT',
                             type=int, help=help_max_count)
    group_basic.add_argument('-ca1', '--color-accent1', metavar=colors_metavar,
                             nargs=4, type=int, default=(0, 255, 255, 255),
                             help=help_color_accent1)
    group_basic.add_argument('-cb', '--color-background', metavar=colors_metavar,
                             nargs=4, type=int, default=(255, 255, 255, 255),
                             help=help_color_background)

    group_multicolor = parser.add_argument_group('Multicoloring options')
    group_multicolor.add_argument('-m', '--multicolor', action='store_true',
                                  help='Enables multicolor mode.')
    group_multicolor.add_argument('-ca2', '--color-accent2', metavar=colors_metavar,
                                  nargs=4, type=int, default=(255, 29, 119, 255),
                                  help=help_color_accent2)

    group_additional = parser.add_argument_group('Additional options')
    group_additional.add_argument('-fp', '--find-percent', metavar='FLOAT',
                                  type=float, help=help_find_percent)
    group_additional.add_argument('-fi', '--fade-in', action='store_true',
                                  help=help_fade_in)

    group_saving = parser.add_argument_group('Saving options')
    group_saving.add_argument('-s', '--save', action='store_true', help=help_save)
    group_saving.add_argument('-p', '--path', metavar='PATH', type=str, help=help_path)

    args = parser.parse_args()


    radius = Vector(args.width, args.height)
    max_count = args.max_count
    if max_count is None:
        max_count = (radius.x * radius.y) // 2
    color_accent1 = Color(*args.color_accent1)
    color_accent2 = Color(*args.color_accent2)
    color_background = Color(*args.color_background)


    start_date = datetime.now()

    nebula = Nebula(radius, max_count, args.reproduce_chance)
    nebula.develop(args.find_percent)

    if args.multicolor:
        gradient = get_gradient(nebula.current_generation, color_accent1, color_accent2)

    print('\nNow the data will be processed and converted to a graphical representation.\nIt can take some time.')
    sleep(1)

    image = Image.new('RGBA', (radius.x, radius.y))
    draw = ImageDraw.Draw(image)

    for x in range(radius.x + 1):
        print(f'[{datetime.now().isoformat()}]', 'Image drawing:', f'{round(x / radius.x * 100, 5)} %', sep='\t')
        for y in range(radius.y + 1):
            if nebula.squares[x][y]:
                if not args.multicolor:
                    max_gen = nebula.current_generation
                    gen = nebula.squares[x][y].gen

                    alpha = None
                    if args.fade_in:
                        alpha = round(gen / max_gen * 255)
                    else:
                        alpha = round((1 - gen / max_gen) * 255)
                    color_accent = color_accent1._replace(a=alpha)

                    draw.point([x, y], color_accent)
                else:
                    gen = nebula.squares[x][y].gen - 1
                    draw.point([x, y], gradient[gen])
            else:
                draw.point([x, y], color_background)

    image_name = f'{radius.x}x{radius.y}_({nebula.count}#{max_count})_{args.reproduce_chance}_{generate_filename()}.png'
    if args.save:
        if args.path:
            image.save(args.path + image_name, 'PNG')
        else:
            image.save(image_name, 'PNG')
    image.show()

    get_runtime(start_date)
