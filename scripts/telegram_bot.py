from telegram import Bot
from argparse import ArgumentParser

from random import uniform, getrandbits
from json import load

from renderer import parse_args, render_image
from constants import TELEGRAM_IMAGES_SAVE_PATH, BOT_CONFIG_PATH


def parse_config_args(config: dict) -> list:
    args = []
    for key, value in config['args'].items():
        if key == '--reproduce-chance':
            if value['start'] is not None:
                args.append(key)
                args.append(str(uniform(value['start'], value['end'])))
            elif value['value']:
                args.append(key)
                args.append(str(value['value']))
            else:
                args.append(key)
                args.append(str(uniform(0.5, 1)))
        elif 'percent' in key:
            if value['start'] is not None:
                args.append(key)
                args.append(str(uniform(value['start'], value['end'])))
            elif value['value']:
                args.append(key)
                args.append(str(value['value']))
        elif type(value) is list:
            args.append(key)
            for i in range(4):
                args.append(str(value[i]))
        elif type(value) is int:
            args.append(key)
            args.append(str(value))
        elif type(value) is dict:
            if value['random']:
                if bool(getrandbits(1)):
                    args.append(key)
            else:
                if value['value']:
                    args.append(key)
    args.append('--dont-show-image')
    return args


def generate_caption(args_dict: dict, colors: list) -> str:
    caption = f'width: {args_dict["width"]}\n'
    caption += f'height: {args_dict["height"]}\n'
    caption += f'reproduce chance: {args_dict["reproduce_chance"]}\n'
    for i in range(len(colors)):
        caption += f'accent color {i + 1}: rgba({", ".join(map(str, colors[i]))})\n'
    caption += f'background color: rgba({", ".join(map(str, list(args_dict["color_background"])))})\n'
    caption += f'fade in: {args_dict["fade_in"]}\n'
    return caption


def send_random_image(config: dict, scheduled: bool = False) -> None:
    args = parse_config_args(config)
    args.insert(0, config['width'])
    args.insert(1, config['height'])

    image_path, args_dict, colors = render_image(parse_args(args), msg_send=True)
    caption = generate_caption(args_dict, colors)

    bot = Bot(config['token'])
    bot.send_photo(config['chat_id'], open(image_path, 'rb'), caption=caption)

    if scheduled:
        args.pop(0)
        args.pop(0)


def send_specific_image(config: dict) -> None:
    image_path, args_dict, colors = render_image(parse_args(), msg_send=True)
    caption = generate_caption(args_dict, colors)

    bot = Bot(config['token'])
    bot.send_photo(config['chat_id'], open(image_path, 'rb'), caption=caption)


if __name__ == '__main__':
    config = None
    with open(BOT_CONFIG_PATH, 'r') as json_file:
        config = load(json_file)

    if config['use_config_args']:
        send_random_image(config)
    else:
        send_specific_image(config)
