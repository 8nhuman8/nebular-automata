from random import uniform, getrandbits, randint
from json import load

from telegram import Bot
from argparse import ArgumentParser

from renderer import parse_args, render_image
from constants import TELEGRAM_IMAGES_SAVE_PATH, BOT_CONFIG_PATH
from utils import random_color


def parse_config_args(config: dict) -> list:
    args = []
    for key, value in config['args'].items():
        if key == '--reproduce-chance':
            args.append(key)
            if value['start'] is not None:
                args.append(str(uniform(value['start'], value['end'])))
            elif value['value']:
                args.append(str(value['value']))
            else:
                args.append(str(uniform(0.5, 1)))
        elif 'percent' in key:
            if value['start'] is not None:
                args.append(key)
                args.append(str(uniform(value['start'], value['end'])))
            elif value['value']:
                args.append(key)
                args.append(str(value['value']))
        elif key == '--starting-point':
            args.append(key)
            if value['random']:
                args.append(str(randint(1, int(config['width']))))
                args.append(str(randint(1, int(config['height']))))
            elif value['valueX'] and not value['valueY']:
                args.append(str(value['valueX']))
                args.append(str(randint(1, int(config['height']))))
            elif not value['valueX'] and value['valueY']:
                args.append(str(randint(1, int(config['width']))))
                args.append(str(value['valueY']))
            else:
                args.append(str(value['valueX']))
                args.append(str(value['valueY']))
        elif key == '--color-background':
            if value['random']:
                args.append(key)
                # cc - color component
                for cc in random_color():
                    args.append(str(cc))
            elif value['value']:
                args.append(key)
                # cc - color component
                for cc in value['value']:
                    args.append(str(cc))
        elif key == '--max-count' or key == '--colors-number':
            if value['start'] is not None:
                args.append(key)
                args.append(str(randint(value['start'], value['end'])))
            elif value['value']:
                args.append(key)
                args.append(str(value['value']))
        elif type(value) is dict:
            if value['random']:
                if bool(getrandbits(1)):
                    args.append(key)
            elif value['value']:
                args.append(key)
    args.append('--dont-show-image')
    return args


def generate_caption(args_dict: dict, colors: list) -> str:
    caption = f'width: {args_dict["width"]}\n'
    caption += f'height: {args_dict["height"]}\n'
    caption += f'reproduce chance: {args_dict["reproduce_chance"]}\n'
    caption += f'starting point: ({args_dict["starting_point"][0]}, {args_dict["starting_point"][1]})\n'
    for i in range(len(colors)):
        caption += f'accent color {i + 1}: rgba({", ".join(map(str, colors[i]))})\n'
    caption += f'background color: rgba({", ".join(map(str, list(args_dict["color_background"])))})\n'
    caption += f'fade in: {args_dict["fade_in"]}\n'
    return caption


def send_image(config: dict, image_path: str, caption: str) -> None:
    bot = Bot(config['token'])
    if config['use_caption']:
        bot.send_photo(config['chat_id'], open(image_path, 'rb'), caption=caption)
    else:
        bot.send_photo(config['chat_id'], open(image_path, 'rb'))


def send_random_image(config: dict, scheduled: bool = False) -> None:
    args = parse_config_args(config)
    args.insert(0, config['width'])
    args.insert(1, config['height'])

    image_path, args_dict, colors = render_image(parse_args(args), msg_send=True)
    caption = generate_caption(args_dict, colors)

    send_image(config, image_path, caption)

    if scheduled:
        args.pop(0)
        args.pop(0)


def send_specific_image(config: dict) -> None:
    image_path, args_dict, colors = render_image(parse_args(), msg_send=True)
    caption = generate_caption(args_dict, colors)
    send_image(config, image_path, caption)


if __name__ == '__main__':
    with open(BOT_CONFIG_PATH, 'r') as json_file:
        config = load(json_file)

    if config['use_config_args']:
        send_random_image(config)
    else:
        send_specific_image(config)
