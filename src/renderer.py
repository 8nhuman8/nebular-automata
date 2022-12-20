from argparse import ArgumentParser, ArgumentTypeError, BooleanOptionalAction, Namespace
from json import load
from pathlib import Path

import cv2
import ffmpeg
import numpy as np
from PIL import Image

from constants import *
from nebula import Nebula
from utils import *


def parse_cl_arguments() -> Namespace:
    parser = ArgumentParser()

    group_required = parser.add_argument_group('Required options')
    group_required.add_argument('width', type=int, help=HELP_WIDTH)
    group_required.add_argument('height', type=int, help=HELP_HEIGHT)

    group_basic = parser.add_argument_group('Basic options')
    group_basic.add_argument('-sp', '--start-point', metavar=('Y', 'X'), nargs=2, type=int, help=HELP_START_POINT)
    group_basic.add_argument('-p', '--probability', metavar='FLOAT', type=float, default=0.51, help=HELP_PROBABILTY)
    group_basic.add_argument('-mc', '--max-count', metavar='INT', type=int, help=HELP_MAX_COUNT)
    group_basic.add_argument('-minp', '--min-percent', metavar='FLOAT', type=float, help=HELP_MIN_PERCENT)
    group_basic.add_argument('-maxp', '--max-percent', metavar='FLOAT', type=float, help=HELP_MAX_PERCENT)

    group_multicolor = parser.add_argument_group('Coloring options')
    group_multicolor.add_argument('-rc', '--random-colors', action='store_true', help=HELP_RANDOM_COLORS)
    group_multicolor.add_argument('-rbg', '--random-background', action='store_true', help=HELP_RANDOM_BACKGROUND)
    group_multicolor.add_argument('-cn', '--colors-number', metavar='INT', type=int, default=3, help=HELP_COLORS_NUMBER)

    group_additional = parser.add_argument_group('Additional options')
    group_additional.add_argument('-o', '--opaque', action='store_true', help=HELP_OPAQUE)
    group_additional.add_argument('-fi', '--fade-in', action='store_true', help=HELP_FADE_IN)
    group_additional.add_argument('-s', '--seed', metavar='INT', type=float, help=HELP_SEED)
    group_additional.add_argument('-t', '--torus', action=BooleanOptionalAction, help=HELP_TORUS)

    group_image = parser.add_argument_group('Image options')
    group_image.add_argument('-si', '--save-image', action='store_true', help=HELP_SAVE_IMAGE)
    group_image.add_argument('-pi', '--path-image', metavar='PATH', type=str, help=HELP_PATH_IMAGE)
    group_image.add_argument('-dsi', '--dont-show-image', action='store_true', help=HELP_DONT_SHOW_IMAGE)

    group_video = parser.add_argument_group('Video options')
    group_video.add_argument('-sv', '--save-video', action='store_true', help=HELP_SAVE_VIDEO)
    group_video.add_argument('-pv', '--path-video', metavar='PATH', type=str, help=HELP_PATH_VIDEO)
    group_video.add_argument('-vs', '--video-size', metavar='INT', type=int, default=8, help=HELP_VIDEO_SIZE)

    gif_video = parser.add_argument_group('GIF options')
    gif_video.add_argument('-sg', '--save-gif', action='store_true', help=HELP_SAVE_GIF)
    gif_video.add_argument('-pg', '--path-gif', metavar='PATH', type=str, help=HELP_PATH_GIF)

    return parser.parse_args()


def validate_input(args: Namespace) -> Namespace:
    if args.width <= 0 or args.height <= 0:
        raise ArgumentTypeError('width, height ∈ N')

    size = Vector(args.height, args.width)

    if args.max_count is None:
        args.max_count = (size.y * size.x) // 2
    elif args.max_count <= 0:
        raise ArgumentTypeError('max_count ∈ N')

    if args.colors_number <= 0:
        raise ArgumentTypeError('colors_number ∈ N')
    if args.video_size <= 0:
        raise ArgumentTypeError('video_size ∈ N')

    if not 0 <= args.probability <= 1:
        raise ArgumentTypeError('probability ∈ [0, 1]')
    if args.min_percent is not None:
        if not 0 <= args.min_percent <= 1:
            raise ArgumentTypeError('min_percent ∈ [0, 1]')
    if args.max_percent is not None:
        if not 0 <= args.max_percent <= 1:
            raise ArgumentTypeError('max_percent ∈ [0, 1]')

    if args.start_point is None:
        args.start_point = Vector(size.y // 2, size.x // 2)
    else:
        args.start_point = Vector(args.start_point[0] - 1, args.start_point[1] - 1)
    if not (1 <= args.start_point.y + 1 <= size.y and 1 <= args.start_point.x + 1 <= size.x):
        raise ArgumentTypeError('start_point.y ∈ [1, height], start_point.x ∈ [1, width]')

    return args


@benchmark
def render(args: Namespace) -> None:
    args = validate_input(args)

    size = Vector(args.height, args.width)
    colors, color_bg, directions = import_config()

    nebula = Nebula(
        size,
        args.max_count,
        args.probability,
        args.start_point,
        directions,
        args.seed,
        args.torus
    )
    nebula.develop(args.min_percent, args.max_percent)
    generations_number = nebula.generation

    if args.random_colors:
        colors = random_colors(args.colors_number)
    if args.random_background:
        color_bg = random_color()
    if args.opaque:
        for color in colors:
            color.a = 255
        color_bg.a = 255

    gradient = polylinear_gradient(colors, generations_number)

    out_name = f'{args.width}x{args.height}_{args.probability}_{unique_code()}'
    if args.path_image:
        image_path = out_path(args.path_image, out_name, '.png')
    else:
        image_path = out_path(OUTPUT_FILES_PATH, out_name, '.png')
    if args.path_video:
        video_path = out_path(args.path_video, out_name, '.mp4').as_posix()
    else:
        video_path = out_path(OUTPUT_FILES_PATH, out_name, '.mp4').as_posix()
    if args.path_gif:
        gif_path = out_path(args.path_gif, out_name, '.gif')
    else:
        gif_path = out_path(OUTPUT_FILES_PATH, out_name, '.gif')

    if args.save_video:
        fourcc = cv2.VideoWriter_fourcc(*'avc1')
        video = cv2.VideoWriter(TEMP_VIDEO_PATH, fourcc, 144, size[::-1])

    frame = np.full((size.y, size.x, 4), np.array(color_bg), dtype=np.uint8)
    if args.save_gif:
        frames = [frame.copy()]

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

        coordinates = tuple(np.transpose(generation))
        frame[coordinates] = np.array(fill_color)

        if args.save_video:
            video.write(cv2.cvtColor(frame, cv2.COLOR_RGBA2BGRA))
        if args.save_gif:
            frames.append(frame.copy())

    image = Image.fromarray(frame, mode='RGBA')

    if not args.dont_show_image:
        image.show()

    if args.save_image:
        image.save(image_path, 'PNG')
    if args.save_video:
        video.release()
        compress_video(TEMP_VIDEO_PATH, video_path, args.video_size)
        Path.unlink(TEMP_VIDEO_PATH)
    if args.save_gif:
        images = [Image.fromarray(frame) for frame in frames]
        images[0].save(gif_path, 'GIF', save_all=True, append_images=images[1:], duration=40, loop=0)


def import_config() -> tuple[list[Color], Color, list[Vector]]:
    with open(CONFIG_PATH) as json_file:
        config = load(json_file)

    colors = [Color(*color) for color in config['colors']]
    color_bg = Color(*config['color_background'])

    directions = direction_to_vector.copy()
    allowed_reproduction_directions = config['allowed_reproduction_directions']

    for direction, allowed in allowed_reproduction_directions.items():
        if not allowed:
            directions.pop(direction)

    return colors, color_bg, list(directions.values())


def out_path(path: str, name: str, ext: str) -> Path:
    return Path(path) / (name + ext)


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


if __name__ == '__main__':
    cl_argumentss = parse_cl_arguments()
    render(cl_argumentss)
