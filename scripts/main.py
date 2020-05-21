from PIL import Image, ImageDraw
from argparse import ArgumentParser

from datetime import datetime
from time import sleep

from nebula import Nebula
from utils import Vector, Color, generate_filename, get_runtime, get_gradient
import constants as c


if __name__ == '__main__':
    parser = ArgumentParser(description=c.DESCRIPTION)

    group_required = parser.add_argument_group('Required options')
    group_required.add_argument('width', type=int, help='The width of the image.')
    group_required.add_argument('height', type=int, help='The height of the image.')

    group_basic = parser.add_argument_group('Basic options')
    group_basic.add_argument('-rc', '--reproduce-chance', metavar='FLOAT',
                             type=float, default=0.5, help=c.HELP_REPRODUCE_CHANCE)
    group_basic.add_argument('-mc', '--max-count', metavar='INT',
                             type=int, help=c.HELP_MAX_COUNT)
    group_basic.add_argument('-ca1', '--color-accent1', metavar=c.COLORS_METAVAR,
                             nargs=4, type=int, default=(0, 255, 255, 255),
                             help=c.HELP_COLOR_ACCENT1)
    group_basic.add_argument('-cb', '--color-background', metavar=c.COLORS_METAVAR,
                             nargs=4, type=int, default=(255, 255, 255, 255),
                             help=c.HELP_COLOR_BACKGROUND)

    group_multicolor = parser.add_argument_group('Multicoloring options')
    group_multicolor.add_argument('-m', '--multicolor', action='store_true',
                                  help=c.HELP_MULTICOLOR)
    group_multicolor.add_argument('-ca2', '--color-accent2', metavar=c.COLORS_METAVAR,
                                  nargs=4, type=int, default=(255, 29, 119, 255),
                                  help=c.HELP_COLOR_ACCENT2)

    group_additional = parser.add_argument_group('Additional options')
    group_additional.add_argument('-fp', '--find-percent', metavar='FLOAT',
                                  type=float, help=c.HELP_FIND_PERCENT)
    group_additional.add_argument('-fi', '--fade-in', action='store_true',
                                  help=c.HELP_FADE_IN)

    group_saving = parser.add_argument_group('Saving options')
    group_saving.add_argument('-s', '--save', action='store_true', help=c.HELP_SAVE)
    group_saving.add_argument('-p', '--path', metavar='PATH', type=str, help=c.HELP_PATH)

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
