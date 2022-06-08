from json import load
from time import sleep
from typing import Any, Sequence
from datetime import datetime

from argparse import ArgumentParser, Namespace
from PIL import Image, ImageDraw

import constants as c
from nebula import Nebula
import utils


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


def config_colors() -> list[list[int]]:
    with open(c.COLORS_CONFIG_PATH, 'r') as json_file:
        colors_dict = load(json_file)
    return list(colors_dict.values())


@utils.benchmark
def render_image(args: Namespace, msg_send: bool = False) -> tuple[str | None, dict[str, Any], list[list[int]], utils.Vector]:
    size = utils.Vector(args.width, args.height)

    starting_point = args.starting_point
    if starting_point is not None:
        # For the user to use the coordinate indexing starting at one
        starting_point = utils.Vector(*[x - 1 for x in args.starting_point])

    color_background = tuple(args.color_background)

    nebula = Nebula(
        size,
        args.max_count,
        args.reproduce_chance,
        quadratic=args.quadratic,
        starting_point=starting_point
    )
    nebula.develop(min_percent=args.min_percent, max_percent=args.max_percent)

    colors = config_colors()

    if args.random_colors:
        colors = utils.random_colors(args.colors_number)
        gradient = utils.gradient(nebula.current_generation, colors)
    elif len(colors) > 1:
        gradient = utils.gradient(nebula.current_generation, colors)

    if args.opaque:
        for color in colors:
            color[3] = 255

    print(c.NOTIFICATION_MSG_BEFORE_RENDERING)
    sleep(1)

    image = Image.new('RGBA', (size.x, size.y))
    draw = ImageDraw.Draw(image)

    for x in range(size.x + 1):
        print(f'[{datetime.now().time()}]', 'Image drawing:', f'{x / size.x * 100 : .5f} %', sep='\t')
        for y in range(size.y + 1):
            if nebula.squares[x][y]:
                if len(colors) == 1:
                    max_gen = nebula.current_generation
                    gen = nebula.squares[x][y].gen

                    alpha = round((1 - gen / max_gen) * 255)
                    if args.fade_in:
                        alpha = round(gen / max_gen * 255)

                    colors[0][3] = alpha

                    draw.point([x, y], fill=tuple(colors[0]))
                else:
                    gen = nebula.squares[x][y].gen - 1
                    draw.point([x, y], fill=gradient[gen])
            else:
                draw.point([x, y], fill=color_background)

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
