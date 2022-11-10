from json import load
from time import sleep
from typing import Any, Sequence
from datetime import datetime

from argparse import ArgumentParser, Namespace
from PIL import Image, ImageDraw

import constants as c
from nebula import Nebula
import utils


def validate_input(args: Namespace) -> Namespace:
    if args.width <= 0 or args.height <= 0:
        raise ValueError('Size components must be natural numbers.')

    size = utils.Vector(args.width, args.height)

    if args.max_count is None:
        args.max_count = (size.x * size.y) // 2
    elif args.max_count <= 0:
        raise ValueError('\'max_count\' value must be natural number.')

    if args.reproduce_chance <= 0:
        raise ValueError('\'reproduce_chance\' value must be in the interval (0, 1).')

    if args.starting_point is None:
        args.starting_point = utils.Vector(size.x // 2, size.y // 2)
    else:
        args.starting_point = utils.Vector(*[x - 1 for x in args.starting_point])

    if not (0 <= args.starting_point.x < size.x and 0 <= args.starting_point.y < size.y):
        raise ValueError('Starting point coordinate components (x or y) must be in the interval [1, size(x or y)].')

    return args


def config_colors() -> list[list[int]]:
    with open(c.COLORS_CONFIG_PATH, 'r') as json_file:
        colors_dict = load(json_file)
    return list(colors_dict.values())


def parse_args(args: Sequence[str] | None = None) -> Namespace:
    parser = ArgumentParser(description=c.DESCRIPTION)

    group_required = parser.add_argument_group('Required options')
    group_required.add_argument('width', type=int, help='The width of the image.')
    group_required.add_argument('height', type=int, help='The height of the image.')

    group_basic = parser.add_argument_group('Basic options')
    group_basic.add_argument('-sp', '--starting-point', metavar=('X', 'Y'),
                             nargs=2, type=int, help=c.HELP_STARTING_POINT)
    group_basic.add_argument('-rc', '--reproduce-chance', metavar='FLOAT',
                             type=float, default=0.51,
                             help=c.HELP_REPRODUCE_CHANCE)
    group_basic.add_argument('-mc', '--max-count', metavar='INT',
                             type=int, help=c.HELP_MAX_COUNT)
    group_basic.add_argument('-cb', '--color-background',
                             metavar=('R', 'G', 'B', 'A'), nargs=4, type=int,
                             default=(255, 255, 255, 255),
                             help=c.HELP_COLOR_BACKGROUND)

    group_multicolor = parser.add_argument_group('Multicoloring options')
    group_multicolor.add_argument('-r', '--random-colors', action='store_true',
                                  help=c.HELP_RANDOM_COLORS)
    group_multicolor.add_argument('-cn', '--colors-number', metavar='INT',
                                  type=int, default=3,
                                  help=c.HELP_COLORS_NUMBER)
    group_multicolor.add_argument('-o', '--opaque', action='store_true',
                                  help=c.HELP_OPAQUE)

    group_additional = parser.add_argument_group('Additional options')
    group_additional.add_argument('-minp', '--min-percent', metavar='FLOAT',
                                  type=float, help=c.HELP_MIN_PERCENT)
    group_additional.add_argument('-maxp', '--max-percent', metavar='FLOAT',
                                  type=float, help=c.HELP_MAX_PERCENT)
    group_additional.add_argument('-fi', '--fade-in', action='store_true',
                                  help=c.HELP_FADE_IN)
    group_additional.add_argument('-q', '--quadratic', action='store_true',
                                  help=c.HELP_QUADRATIC)

    group_system = parser.add_argument_group('System options')
    group_system.add_argument('-s', '--save', action='store_true',
                              help=c.HELP_SAVE)
    group_system.add_argument('-p', '--path', metavar='PATH',
                              type=str, help=c.HELP_PATH)
    group_system.add_argument('-dsi', '--dont-show-image', action='store_false',
                              help=c.HELP_DONT_SHOW_IMAGE)

    if args is None:
        return parser.parse_args()
    else:
        return parser.parse_args(args)


@utils.benchmark
def render_image(args: Namespace, msg_send: bool = False) -> tuple[str | None, dict[str, Any], list[list[int]], utils.Vector]:
    args = validate_input(args)
    size = utils.Vector(args.width, args.height)

    nebula = Nebula(
        size,
        args.max_count,
        args.reproduce_chance,
        args.starting_point,
        args.quadratic
    )
    nebula.develop(min_percent=args.min_percent, max_percent=args.max_percent)

    colors = config_colors()
    color_background = tuple(args.color_background)

    if args.random_colors:
        colors = utils.random_colors(args.colors_number)

    gradient = utils.gradient(nebula.current_generation, [utils.Color(*color) for color in colors])
    colors = [list(color) for color in list(colors)]

    if args.opaque:
        for color in colors:
            color[3] = 255

    print(c.NOTIFICATION_MSG_BEFORE_RENDERING)
    sleep(1)

    image = Image.new('RGBA', size)
    draw = ImageDraw.Draw(image)

    for x in range(size.x + 1):
        print(f'[{datetime.now().time()}]', 'Image drawing:', f'{x / size.x * 100 : .5f} %', sep='\t')
        for y in range(size.y + 1):
            square = nebula.squares[x][y]
            if square:
                if len(colors) == 1:
                    max_gen = nebula.current_generation
                    gen = square.gen

                    alpha = round((1 - gen / max_gen) * 255)
                    if args.fade_in:
                        alpha = round(gen / max_gen * 255)

                    colors[0][3] = alpha

                    draw.point([x, y], fill=tuple(colors[0]))
                else:
                    gen = square.gen - 1
                    draw.point([x, y], fill=gradient[gen])
            else:
                draw.point([x, y], fill=color_background)
    print()

    image_name = f'{size.x}x{size.y}_{args.reproduce_chance}_{utils.generate_filename()}.png'
    image_path = None

    if args.save or msg_send:
        if args.path:
            image.save(args.path + image_name, format='PNG', optimize=True, quality=1)
            image_path = args.path + image_name
        elif msg_send:
            image.save(c.TELEGRAM_IMAGES_SAVE_PATH + c.TELERGAM_IMAGE_PREFIX + image_name, 'PNG')
            image_path = c.TELEGRAM_IMAGES_SAVE_PATH + c.TELERGAM_IMAGE_PREFIX + image_name
        else:
            image.save(image_name, 'PNG')
            image_path = image_name

    if args.dont_show_image:
        image.show()

    return image_path, vars(args), colors, nebula.starting_point


if __name__ == '__main__':
    args = parse_args()
    render_image(args)
