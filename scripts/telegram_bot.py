from telegram import Bot
from argparse import ArgumentParser

from random import uniform, randint
from json import load

from renderer import parse_args, render_image
from constants import TELEGRAM_IMAGES_SAVE_PATH, CONFIG_PATH


def get_random_args() -> list:
    args = f'-r --min-percent {0.5}'
    return args.split()


def generate_caption(args_dict: dict) -> str:
    # f-string don't work with dict for some reason
    caption = 'width: ' + str(args_dict['width']) + '\n'
    caption += 'height: ' + str(args_dict['height']) + '\n'
    caption += 'reproduce chance: ' + str(args_dict['reproduce_chance']) + '\n'
    caption += 'accent color 1: (' + ', '.join(map(str, list(args_dict['color_accent1']))) + ')\n'
    caption += 'accent color 2: (' + ', '.join(map(str, list(args_dict['color_accent2']))) + ')\n'
    caption += 'color_background: (' + ', '.join(map(str, list(args_dict['color_background']))) + ')\n'
    caption += 'multicolor: ' + str(args_dict['multicolor']) + '\n'
    caption += 'fade in: ' + str(args_dict['fade_in']) + '\n'
    return caption


def send_random_image(config: dict, args: list) -> None:
    args.insert(0, config['width'])
    args.insert(1, config['height'])

    image_path, args_dict = render_image(parse_args(args), msg_send=True)
    caption = generate_caption(args_dict)

    bot = Bot(config['token'])
    bot.send_photo(config['chat_id'], open(image_path, 'rb'), caption=caption)


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
