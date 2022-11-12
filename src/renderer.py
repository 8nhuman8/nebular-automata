from argparse import ArgumentParser, ArgumentTypeError, Namespace
from dataclasses import astuple
from functools import reduce
from json import load
from operator import iconcat
from os import remove
from typing import Sequence

import cv2
import ffmpeg
from numpy import array
from PIL import Image, ImageDraw

from constants import *
from nebula import Nebula
from utils import *


def validate_input(args: Namespace) -> Namespace:
    if args.width <= 1 or args.height <= 1:
        raise ArgumentTypeError('width, height ∈ [2..∞]')

    size = Vector(args.width, args.height)

    if args.max_count is None:
        args.max_count = (size.x * size.y) // 2
    elif args.max_count <= 0:
        raise ArgumentTypeError('max_count ∈ N')

    if args.colors_number <= 0:
        raise ArgumentTypeError('colors_number ∈ N')

    if not 0 <= args.reproduce_chance <= 1:
        raise ArgumentTypeError('reproduce_chance ∈ [0, 1]')
    if args.min_percent is not None:
        if not 0 <= args.min_percent <= 1:
            raise ArgumentTypeError('min_percent ∈ [0, 1]')
    if args.max_percent is not None:
        if not 0 <= args.max_percent <= 1:
            raise ArgumentTypeError('max_percent ∈ [0, 1]')

    if args.starting_point is None:
        args.starting_point = Vector(size.x // 2, size.y // 2)
    else:
        args.starting_point = Vector(args.starting_point[0] - 1, args.starting_point[1] - 1)
    if not (1 <= args.starting_point.x + 1 <= size.x and 1 <= args.starting_point.y + 1 <= size.y):
        raise ArgumentTypeError('starting_point.x ∈ [1, width], starting_point.y ∈ [1, height]')

    return args


def get_palette() -> tuple[list[Color], Color]:
    with open(COLORS_CONFIG_PATH, 'r') as json_file:
        colors_dict = load(json_file)

    colors = [Color(*color) for color in list(colors_dict['colors'].values())]
    color_bg = Color(*colors_dict['color_bg'])

    return colors, color_bg


def draw_image(
    image: Image.Image,
    squares: list[Square],
    args: Namespace,
    max_gen: int,
    grad: list[Color]
) -> Image.Image:
    draw = ImageDraw.Draw(image)

    for square in squares:
        coord = [square.x, square.y]
        gen = square.gen

        if len(grad) == 1:
            alpha = round((1 - gen / max_gen) * 255)
            if args.fade_in:
                alpha = round(gen / max_gen * 255)
            if args.opaque:
                alpha = 255

            fill_color = grad[0]
            fill_color.a = alpha
        else:
            fill_color = grad[gen - 1]

        draw.point(coord, fill=astuple(fill_color))

    return image


def compress_video(video_path: str, output_path: str, target_size: int):
    probe = ffmpeg.probe(video_path)
    duration = float(probe['format']['duration'])
    video_bitrate = (target_size * 1024 * 1024 * 8) / (duration * 1.073741824)
    (
        ffmpeg
        .input(video_path)
        .output(output_path, **{'c:v': 'libx264', 'b:v': video_bitrate, 'f': 'mp4'})
        .overwrite_output()
        .global_args('-loglevel', 'error')
        .run()
    )


def arg_parse(args: Sequence[str] | None = None) -> Namespace:
    parser = ArgumentParser(description=DESCRIPTION)

    group_required = parser.add_argument_group('Required options')
    group_required.add_argument('width', type=int, help='The width of the image.')
    group_required.add_argument('height', type=int, help='The height of the image.')

    group_basic = parser.add_argument_group('Basic options')
    group_basic.add_argument('-sp', '--starting-point', metavar=('X', 'Y'),
                             nargs=2, type=int, help=HELP_STARTING_POINT)
    group_basic.add_argument('-rc', '--reproduce-chance', metavar='FLOAT',
                             type=float, default=0.51, help=HELP_REPRODUCE_CHANCE)
    group_basic.add_argument('-mc', '--max-count', metavar='INT', type=int,
                             help=HELP_MAX_COUNT)

    group_multicolor = parser.add_argument_group('Multicoloring options')
    group_multicolor.add_argument('-r', '--random-colors', action='store_true',
                                  help=HELP_RANDOM_COLORS)
    group_multicolor.add_argument('-rbg', '--random-background', action='store_true',
                                  help=HELP_RANDOM_BACKGROUND)
    group_multicolor.add_argument('-cn', '--colors-number', metavar='INT',
                                  type=int, default=3, help=HELP_COLORS_NUMBER)
    group_multicolor.add_argument('-o', '--opaque', action='store_true',
                                  help=HELP_OPAQUE)

    group_additional = parser.add_argument_group('Additional options')
    group_additional.add_argument('-minp', '--min-percent', metavar='FLOAT',
                                  type=float, help=HELP_MIN_PERCENT)
    group_additional.add_argument('-maxp', '--max-percent', metavar='FLOAT',
                                  type=float, help=HELP_MAX_PERCENT)
    group_additional.add_argument('-fi', '--fade-in', action='store_true',
                                  help=HELP_FADE_IN)
    group_additional.add_argument('-q', '--quadratic', action='store_true',
                                  help=HELP_QUADRATIC)

    group_system = parser.add_argument_group('System options')
    group_system.add_argument('-s', '--save', action='store_true', help=HELP_SAVE)
    group_system.add_argument('-p', '--path', metavar='PATH', type=str, help=HELP_PATH)
    group_system.add_argument('-dsi', '--dont-show-image', action='store_true',
                              help=HELP_DONT_SHOW_IMAGE)

    if args is None:
        return parser.parse_args()
    else:
        return parser.parse_args(args)


@benchmark
def render_image(args: Namespace):
    args = validate_input(args)
    size = Vector(args.width, args.height)

    nebula = Nebula(
        size,
        args.max_count,
        args.reproduce_chance,
        args.starting_point,
        args.quadratic
    )
    nebula.develop(args.min_percent, args.max_percent)
    max_gen = nebula.current_generation

    colors, color_bg = get_palette()
    if args.random_colors:
        colors = random_colors(args.colors_number)
    if args.random_background:
        color_bg = random_color()
    if args.opaque:
        for color in colors:
            color.a = 255

    grad = gradient(nebula.current_generation, colors)

    print(NOTIFICATION_MSG_BEFORE_RENDERING)

    im = Image.new('RGBA', size)
    im.paste(astuple(color_bg), [0, 0, size.x, size.y])
    im = draw_image(im, reduce(iconcat, nebula.population, []), args, max_gen, grad)

    im_name = f'{size.x}x{size.y}_{args.reproduce_chance}_{generate_filename()}.png'

    if args.save:
        if args.path:
            im.save(args.path + im_name, 'PNG', optimize=True, quality=1)
        else:
            im.save(im_name, 'PNG', optimize=True, quality=1)

    if not args.dont_show_image:
        im.show()

    image = Image.new('RGBA', size)
    image.paste(astuple(color_bg), [0, 0, size.x, size.y])
    image = draw_image(image, nebula.population[0], args, max_gen, grad)
    images = [image]

    for gen_index, generation in enumerate(nebula.population[1:]):
        current_image = draw_image(images[gen_index].copy(), generation, args, max_gen, grad)
        images.append(current_image)

    fourcc = cv2.VideoWriter_fourcc(*'avc1')
    video = cv2.VideoWriter('videos/temp_video.mp4', fourcc, 60, size)
    for image in images:
        video.write(cv2.cvtColor(array(image), cv2.COLOR_RGBA2BGRA))
    video.release()

    fourcc = cv2.VideoWriter_fourcc(*'avc1')
    video = cv2.VideoWriter('videos/temp_video.mp4', fourcc, 60, size)
    for image in images:
        video.write(cv2.cvtColor(array(image), cv2.COLOR_RGBA2BGRA))
    video.release()
    compress_video('videos/temp_video.mp4', 'videos/video.mp4', 1)
    remove('videos/temp_video.mp4')
    # #images[0].save(f'gif.gif', 'GIF', minimize=True, save_all=True, append_images=images[1:], duration=50, loop=0)


if __name__ == '__main__':
    args = arg_parse()
    render_image(args)
