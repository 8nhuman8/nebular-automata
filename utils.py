from collections import namedtuple
from string import ascii_lowercase, ascii_uppercase, digits
from random import choice


Square = namedtuple('Square', ['x', 'y', 'gen'])
Vector = namedtuple('Vector', ['x', 'y'])
Color = namedtuple('Color', ['r', 'g', 'b', 'a'])


def generate_filename(size=18):
    chars = ascii_lowercase + ascii_uppercase + digits
    return ''.join(choice(chars) for _ in range(size))
