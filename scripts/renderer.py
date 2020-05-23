from PIL import Image, ImageDraw
from argparse import ArgumentParser, Namespace

from datetime import datetime
from time import sleep
from random import uniform, getrandbits

from nebula import Nebula
import utils
import constants as c


def parse_args(args: list = None) -> Namespace:
    parser = ArgumentParser(description=c.DESCRIPTION)

    group_required = parser.add_argument_group('Required options')
    group_required.add_argument('width', type=int, help='The width of the image.')
    group_required.add_argument('height', type=int, help='The height of the image.')

    group_basic = parser.add_argument_group('Basic options')
    group_basic.add_argument('-rc', '--reproduce-chance', metavar='FLOAT',
                             type=float, default=0.51, help=c.HELP_REPRODUCE_CHANCE)
    group_basic.add_argument('-mc', '--max-count', metavar='INT',
                             type=int, help=c.HELP_MAX_COUNT)
    group_basic.add_argument('-ca1', '--color-accent1', metavar=c.COLORS_METAVAR,
                             nargs=4, type=int, default=(0, 255, 255, 255),
                             help=c.HELP_COLOR_ACCENT1)
    group_basic.add_argument('-cb', '--color-background', metavar=c.COLORS_METAVAR,
                             nargs=4, type=int, default=(255, 255, 255, 255),
                             help=c.HELP_COLOR_BACKGROUND)
    group_basic.add_argument('-r', '--random', action='store_true',
                             help=c.HELP_RANDOM)

    group_multicolor = parser.add_argument_group('Multicoloring options')
    group_multicolor.add_argument('-m', '--multicolor', action='store_true',
                                  help=c.HELP_MULTICOLOR)
    group_multicolor.add_argument('-ca2', '--color-accent2', metavar=c.COLORS_METAVAR,
                                  nargs=4, type=int, default=(255, 29, 119, 255),
                                  help=c.HELP_COLOR_ACCENT2)

    group_additional = parser.add_argument_group('Additional options')
    group_additional.add_argument('--min-percent', metavar='FLOAT',
                                  type=float, help=c.HELP_MIN_PERCENT)
    group_additional.add_argument('--max-percent', metavar='FLOAT',
                                  type=float, help=c.HELP_MAX_PERCENT)
    group_additional.add_argument('-fi', '--fade-in', action='store_true',
                                  help=c.HELP_FADE_IN)

    group_system = parser.add_argument_group('System options')
    group_system.add_argument('-s', '--save', action='store_true',
                              help=c.HELP_SAVE)
    group_system.add_argument('-p', '--path', metavar='PATH',
                              type=str, help=c.HELP_PATH)
    group_system.add_argument('-si', '--show-image', action='store_true',
                              help=c.HELP_SHOW_IMAGE)

    if args is None:
        return parser.parse_args()
    else:
        return parser.parse_args(args)


def render_image(args: Namespace, msg_send: bool = False) -> None:
    size = utils.Vector(args.width, args.height)
    max_count = args.max_count
    if max_count is None:
        max_count = (size.x * size.y) // 2
    color_accent1 = utils.Color(*args.color_accent1)
    color_accent2 = utils.Color(*args.color_accent2)
    color_background = utils.Color(*args.color_background)

    if args.random:
        color_accent1 = utils.Color(*utils.get_random_color())
        color_accent2 = utils.Color(*utils.get_random_color())
        args.reproduce_chance = round(uniform(0.5, 1), 2)
        # bool(getrandbits(1)) -> random boolean value
        args.multicolor = bool(getrandbits(1))
        args.fade_in = bool(getrandbits(1))


    start_date = datetime.now()

    nebula = Nebula(size, max_count, args.reproduce_chance)
    nebula.develop(min_percent=args.min_percent, max_percent=args.max_percent)

    if args.multicolor:
        gradient = utils.get_gradient(nebula.current_generation, color_accent1, color_accent2)

    print(c.NOTIFICATION_MSG_BEFORE_RENDERING)
    sleep(1)

    image = Image.new('RGBA', (size.x, size.y))
    draw = ImageDraw.Draw(image)

    for x in range(size.x + 1):
        print(f'[{datetime.now().isoformat()}]', 'Image drawing:', '{:.5f}'.format(x / size.x * 100) + ' %', sep='\t')
        for y in range(size.y + 1):
            if nebula.squares[x][y]:
                if not args.multicolor:
                    max_gen = nebula.current_generation
                    gen = nebula.squares[x][y].gen

                    alpha = round((1 - gen / max_gen) * 255)
                    if args.fade_in:
                        alpha = round(gen / max_gen * 255)
                    color_accent = color_accent1._replace(a=alpha)

                    draw.point([x, y], color_accent)
                else:
                    gen = nebula.squares[x][y].gen - 1
                    draw.point([x, y], gradient[gen])
            else:
                draw.point([x, y], color_background)

    image_name = f'{size.x}x{size.y}_({nebula.count}#{max_count})_{args.reproduce_chance}_{utils.generate_filename()}.png'
    image_path = None
    if args.save or msg_send:
        if args.path:
            image.save(args.path + image_name, 'PNG')
            image_path = args.path + image_name
        elif msg_send:
            image.save(c.TELEGRAM_IMAGES_SAVE_PATH + c.TELERGAM_IMAGE_PREFIX + image_name, 'PNG')
            image_path = c.TELEGRAM_IMAGES_SAVE_PATH + c.TELERGAM_IMAGE_PREFIX + image_name
        else:
            image.save(image_name, 'PNG')
            image_path = image_name
    if args.show_image:
        image.show()

    utils.get_runtime(start_date)

    return image_path


if __name__ == '__main__':
    args = parse_args()
    render_image(args)
