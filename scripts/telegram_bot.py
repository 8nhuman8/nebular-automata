from telegram import Bot
from argparse import ArgumentParser

from random import uniform, randint
from json import load

from render import parse_args, render_image
from constants import TELEGRAM_IMAGES_SAVE_PATH, CONFIG_PATH


def get_random_args() -> list:
    args = f'-rc {round(uniform(0.5, 1), 2)} -m -ca1 '
    args += f'{randint(0, 255)} {randint(0, 255)} {randint(0, 255)} {randint(0, 255)} -ca2 '
    args += f'{randint(0, 255)} {randint(0, 255)} {randint(0, 255)} {randint(0, 255)} '
    args += f'-fp {0.85}'
    return args.split()


def send_random_image(cfg: dict, args: list) -> None:
    args.insert(0, cfg['width'])
    args.insert(1, cfg['height'])
    image_path = render_image(parse_args(args), msg_send=True)
    bot = Bot(cfg['token'])
    bot.send_photo(cfg['chat_id'], open(image_path, 'rb'))


def send_specific_image(cfg: dict) -> None:
    image_path = render_image(parse_args(), msg_send=True)
    bot = Bot(cfg['token'])
    bot.send_photo(cfg['chat_id'], open(image_path, 'rb'))


if __name__ == '__main__':
    cfg = None
    with open(CONFIG_PATH, 'r') as json_file:
        cfg = load(json_file)

    if cfg['random']:
        send_random_image(cfg, get_random_args())
    else:
        send_specific_image(cfg)
