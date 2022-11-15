from argparse import ArgumentParser, ArgumentTypeError, Namespace
from json import load
from os import remove

import cv2
import ffmpeg
import numpy as np
from PIL import Image

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

    if not 0 <= args.probability <= 1:
        raise ArgumentTypeError('probability ∈ [0, 1]')
    if args.min_percent is not None:
        if not 0 <= args.min_percent <= 1:
            raise ArgumentTypeError('min_percent ∈ [0, 1]')
    if args.max_percent is not None:
        if not 0 <= args.max_percent <= 1:
            raise ArgumentTypeError('max_percent ∈ [0, 1]')

    if args.start_point is None:
        args.start_point = Vector(size.x // 2, size.y // 2)
    else:
        args.start_point = Vector(args.start_point[0] - 1, args.start_point[1] - 1)
    if not (1 <= args.start_point.x + 1 <= size.x and 1 <= args.start_point.y + 1 <= size.y):
        raise ArgumentTypeError('start_point.x ∈ [1, width], start_point.y ∈ [1, height]')

    return args


def color_palette() -> tuple[list[Color], Color]:
    with open(COLORS_CONFIG_PATH, 'r') as json_file:
        colors_dict = load(json_file)

    colors = [Color(*color) for color in list(colors_dict['colors'].values())]
    color_bg = Color(*colors_dict['color_bg'])

    return colors, color_bg


def compress_video(video_path: str, output_path: str, target_size: int) -> None:
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


def arg_parse() -> Namespace:
    parser = ArgumentParser(description=DESCRIPTION)

    group_required = parser.add_argument_group('Required options')
    group_required.add_argument('width', type=int, help='The width of the image.')
    group_required.add_argument('height', type=int, help='The height of the image.')

    group_basic = parser.add_argument_group('Basic options')
    group_basic.add_argument('-sp', '--start-point', metavar=('X', 'Y'),
                             nargs=2, type=int, help=HELP_START_POINT)
    group_basic.add_argument('-pr', '--probability', metavar='FLOAT',
                             type=float, default=0.51, help=HELP_PROBABILTY)
    group_basic.add_argument('-mc', '--max-count', metavar='INT', type=int,
                             help=HELP_MAX_COUNT)

    group_multicolor = parser.add_argument_group('Multicoloring options')
    group_multicolor.add_argument('-rc', '--random-colors', action='store_true',
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

    return parser.parse_args()


@benchmark
def render(args: Namespace) -> None:
    args = validate_input(args)
    size = Vector(args.width, args.height)

    nebula = Nebula(
        size,
        args.max_count,
        args.probability,
        args.start_point,
        args.quadratic
    )
    nebula.develop(args.min_percent, args.max_percent)
    generations_number = nebula.generation

    colors, color_bg = color_palette()
    if args.random_colors:
        colors = random_colors(args.colors_number)
    if args.random_background:
        color_bg = random_color()
    if args.opaque:
        for color in colors:
            color.a = 255

    gradient = polylinear_gradient(colors, generations_number)

    out_name = f'{size.x}x{size.y}_{args.probability}_{unique_code()}'
    #temp_video_path = OUTPUT_PATH + 'temp_' + out_name + VIDEO_FORMAT
    #video_path = OUTPUT_PATH + out_name + VIDEO_FORMAT

    #fourcc = cv2.VideoWriter_fourcc(*VIDEO_CODEC)
    #video = cv2.VideoWriter(temp_video_path, fourcc, VIDEO_FRAMERATE, size)
    frame = np.full((size.x, size.y, 4), np.array(color_bg), dtype=np.uint8)

    for i, generation in enumerate(nebula.generations, start=1):
        if len(gradient) == 1:
            alpha = round((1 - i / generations_number) * 255)
            if args.fade_in:
                alpha = round(i / generations_number * 255)
            if args.opaque:
                alpha = 255

            fill_color = gradient[0]
            fill_color.a = alpha
        else:
            fill_color = gradient[i - 1]

        coordinates = np.transpose(generation)
        frame[tuple(coordinates)] = np.array(fill_color)
        #video.write(cv2.cvtColor(frame, cv2.COLOR_RGBA2BGRA))

    image = Image.fromarray(frame, mode='RGBA')

    if args.save:
        if args.path:
            image.save(args.path + out_name + IMAGE_FORMAT, IMAGE_FORMAT[1:])
        else:
            image.save(OUTPUT_PATH + out_name + IMAGE_FORMAT, IMAGE_FORMAT[1:])

    if not args.dont_show_image:
        image.show()

    #video.release()
    #compress_video(temp_video_path, video_path, TARGET_VIDEO_MB_SIZE)
    #remove(temp_video_path)


if __name__ == '__main__':
    args = arg_parse()
    render(args)
