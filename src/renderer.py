from argparse import ArgumentParser, Namespace
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


def config_colors() -> list[utils.Color]:
    with open(c.COLORS_CONFIG_PATH, 'r') as json_file:
        colors_dict = load(json_file)
    return [utils.Color(*color) for color in list(colors_dict.values())]


def draw_pixels(
    image: Image.Image,
    squares: list[utils.Square],
    args: Namespace,
    max_gen: int,
    gradient: list[utils.Color]
) -> Image.Image:
    draw = ImageDraw.Draw(image)

    for square in squares:
        coord = [square.x, square.y]
        gen = square.gen

        if len(gradient) == 1:
            alpha = round((1 - gen / max_gen) * 255)
            if args.fade_in:
                alpha = round(gen / max_gen * 255)
            if args.opaque:
                alpha = 255

            fill_color = gradient[0]
            fill_color.a = alpha
        else:
            fill_color = gradient[gen - 1]

        draw.point(coord, fill=astuple(fill_color))

    return image


def compress_video(video_path: str, output_path: str, target_size: int):
    probe = ffmpeg.probe(video_path)
    duration = float(probe['format']['duration'])
    video_bitrate = (target_size * 1024 * 8) / (1.073741824 * duration)
    (
        ffmpeg
        .input(video_path)
        .output(output_path, **{'c:v': 'libx264', 'b:v': video_bitrate, 'f': 'mp4'})
        .overwrite_output()
        .global_args('-loglevel', 'error')
        .run()
    )


def parse_args(args: Sequence[str] | None = None) -> Namespace:
    parser = ArgumentParser(description=c.DESCRIPTION)

    group_required = parser.add_argument_group('Required options')
    group_required.add_argument('width', type=int, help='The width of the image.')
    group_required.add_argument('height', type=int, help='The height of the image.')

    group_basic = parser.add_argument_group('Basic options')
    group_basic.add_argument('-sp', '--starting-point', metavar=('X', 'Y'),
                             nargs=2, type=int, help=c.HELP_STARTING_POINT)
    group_basic.add_argument('-rc', '--reproduce-chance', metavar='FLOAT',
                             type=float, default=0.51, help=c.HELP_REPRODUCE_CHANCE)
    group_basic.add_argument('-mc', '--max-count', metavar='INT', type=int,
                             help=c.HELP_MAX_COUNT)
    group_basic.add_argument('-cb', '--color-background', metavar=('R', 'G', 'B', 'A'),
                             nargs=4, type=int, default=(255, 255, 255, 255),
                             help=c.HELP_COLOR_BACKGROUND)

    group_multicolor = parser.add_argument_group('Multicoloring options')
    group_multicolor.add_argument('-r', '--random-colors', action='store_true',
                                  help=c.HELP_RANDOM_COLORS)
    group_multicolor.add_argument('-cn', '--colors-number', metavar='INT',
                                  type=int, default=3, help=c.HELP_COLORS_NUMBER)
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
    group_system.add_argument('-s', '--save', action='store_true', help=c.HELP_SAVE)
    group_system.add_argument('-p', '--path', metavar='PATH', type=str, help=c.HELP_PATH)
    group_system.add_argument('-dsi', '--dont-show-image', action='store_false',
                              help=c.HELP_DONT_SHOW_IMAGE)

    if args is None:
        return parser.parse_args()
    else:
        return parser.parse_args(args)


@utils.benchmark
def render_image(args: Namespace):
    args = validate_input(args)
    size = utils.Vector(args.width, args.height)

    nebula = Nebula(
        size,
        args.max_count,
        args.reproduce_chance,
        args.starting_point,
        args.quadratic
    )
    nebula.develop(args.min_percent, args.max_percent)
    max_gen = nebula.current_generation

    color_background = tuple(args.color_background)
    colors = config_colors()
    if args.random_colors:
        colors = utils.random_colors(args.colors_number)
    if args.opaque:
        for color in colors:
            color.a = 255

    gradient = utils.gradient(nebula.current_generation, colors)

    print(c.NOTIFICATION_MSG_BEFORE_RENDERING)

    image = Image.new('RGBA', size)
    image.paste(color_background, [0, 0, size.x, size.y])
    image = draw_pixels(image, reduce(iconcat, nebula.population, []), args, max_gen, gradient)

    image_name = f'{size.x}x{size.y}_{args.reproduce_chance}_{utils.generate_filename()}.png'

    if args.save:
        if args.path:
            image.save(args.path + image_name, 'PNG', optimize=True, quality=1)
        else:
            image.save(image_name, 'PNG', optimize=True, quality=1)

    if args.dont_show_image:
        image.show()

    image = Image.new('RGBA', size)
    image.paste(color_background, [0, 0, size.x, size.y])
    image = draw_pixels(image, nebula.population[0], args, max_gen, gradient)
    images = [image]

    for gen_index, generation in enumerate(nebula.population[1:]):
        current_image = draw_pixels(images[gen_index].copy(), generation, args, max_gen, gradient)
        images.append(current_image)

    fourcc = cv2.VideoWriter_fourcc(*'avc1')
    video = cv2.VideoWriter('videos/temp_video.mp4', fourcc, 60, size)
    for image in images:
        video.write(cv2.cvtColor(array(image), cv2.COLOR_RGBA2BGRA))
    video.release()
    compress_video('videos/temp_video.mp4', 'videos/video.mp4', 8 * 1000)
    remove('videos/temp_video.mp4')
    #images[0].save(f'gif.gif', 'GIF', minimize=True, save_all=True, append_images=images[1:], duration=50, loop=0)


if __name__ == '__main__':
    args = parse_args()
    render_image(args)
