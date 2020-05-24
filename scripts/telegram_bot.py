from telegram import Bot
from argparse import ArgumentParser

from random import uniform, randint
from json import load

from renderer import parse_args, render_image
from constants import TELEGRAM_IMAGES_SAVE_PATH, CONFIG_PATH


def get_random_args() -> list:
    args = f'-r -rc {uniform(0.498, 0.5)} -m -o --min-percent {0.5}'
    return args.split()


def generate_caption(args_dict: dict) -> str:
    caption = f'width: {args_dict["width"]}\n'
    caption += f'height: {args_dict["height"]}\n'
    caption += f'reproduce chance: {args_dict["reproduce_chance"]}\n'
    caption += f'accent color 1: rgba({", ".join(map(str, list(args_dict["color_accent1"])))})\n'
    caption += f'accent color 2: rgba({", ".join(map(str, list(args_dict["color_accent2"])))})\n'
    caption += f'background color: rgba({", ".join(map(str, list(args_dict["color_background"])))})\n'
    caption += f'multicolor: {args_dict["multicolor"]}\n'
    caption += f'fade in: {args_dict["fade_in"]}\n'
    return caption


def send_random_image(config: dict, args: list, scheduled: bool = False) -> None:
    args.insert(0, config['width'])
    args.insert(1, config['height'])

    image_path, args_dict = render_image(parse_args(args), msg_send=True)
    caption = generate_caption(args_dict)

    bot = Bot(config['token'])
    bot.send_photo(config['chat_id'], open(image_path, 'rb'), caption=caption)

    if scheduled:
        args.pop(0)
        args.pop(0)


def send_specific_image(config: dict) -> None:
    image_path, args_dict = render_image(parse_args(), msg_send=True)
    caption = generate_caption(args_dict)

    bot = Bot(config['token'])
    bot.send_photo(config['chat_id'], open(image_path, 'rb'), caption=caption)


if __name__ == '__main__':
    config = None
    with open(CONFIG_PATH, 'r') as json_file:
        config = load(json_file)

    if config['random']:
        send_random_image(config, get_random_args())
    else:
        send_specific_image(config)
